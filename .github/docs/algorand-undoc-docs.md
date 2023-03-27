# Algorand - The Undocumented Docs

Dev Notes for Archival Node, Indexer Setup (and more)

## Archival Node FAQ

### [ ? ] How much space will I need?

See -> https://howbigisalgorand.com/

### [ ? ] How long will it take to stand up an Archival Node?

Depends on hardware. The biggest bottleneck is I/O speed. NVMe is by far the optimal HW for this purpose. If you plan to run both an Indexer and Archival Node, split their data directories on separate drives. Some representative hardware estimates (as of block # 18,400,000):

- Raspberry Pi 4 - Archival Node - 11 days

### [ ? ] My archival node started off wicked fast and now it is slow as molasses. (Usually around block 8M+) Why?

Reportedly this was due to an Italian company minting millions of Assets/NFTs, regardless Algorand began seeing much greater popularity around this point. Expect a long, hard slog after block 8M.

![Transaction History](https://media.discordapp.net/attachments/807825288666939482/926325259311919145/unknown.png "Transaction History")

### [ ? ] How do I figure out what relays I'm connecting to?

On Linux: `netstat -nap | grep algod` (port 4160 for MainNet)

### [ ? ] What are the `LookupSRV` errors in `node.log`?

Set `"EnableBlockServiceFallbackToArchiver": false` in your `$ALGORAND_DATA_DIR/config.json` to get rid of these

## Indexer FAQ

### [ ? ] Can the Indexer be set at a specific catchpoint to ignore prior blocks?

Not currently. If your use-cases differ, you may want to consider forking the Indexer or writing your own direct interface to `algod` and skipping the Indexer

### [ ? ] How long for the Indexer to fully catch up?

ETA currently unknown. Please pull-req if you have estimates.

## Participation Keys FAQ

### Some raw Ubuntu 20 Setup Notes (credit: xbox7887)

```
# variables
WALLET_ADDRESS=<ACCOUNT ADDRESS GOES HERE>
CATCHPOINT=$(curl -s https://algorand-catchpoints.s3.us-east-2.amazonaws.com/channel/mainnet/latest.catchpoint)
BLOCK_VALIDITY_PERIOD=3000000
KEY_DILUTION=$(echo "sqrt($BLOCK_VALIDITY_PERIOD)" | bc)
MIN_UALGO_FEE=1000

# constants
export ALGORAND_DATA=/var/lib/algorand

# prereqs
sudo apt-get update
sudo apt-get install -y gnupg2 curl software-properties-common qrencode
curl -O https://releases.algorand.com/key.pub
sudo apt-key add key.pub
sudo add-apt-repository "deb [arch=amd64] https://releases.algorand.com/deb/ stable main"
sudo apt-get update
sudo apt-get install -y algorand-devtools

# initial fast sync
goal node status -d $ALGORAND_DATA
goal node catchup $CATCHPOINT -d $ALGORAND_DATA
goal node status -d $ALGORAND_DATA -w 1000
# wait unti sync time equals zero, then CTRL+C to exit

# calculate block validity
VALID_BLOCK_START=$(goal node status -d $ALGORAND_DATA | grep -oP '(?<=Last committed block: ).*' )
VALID_BLOCK_END=$(($VALID_BLOCK_START+$BLOCK_VALIDITY_PERIOD))

# generate part key
sudo -u algorand -E goal account addpartkey -a $WALLET_ADDRESS --roundFirstValid=$VALID_BLOCK_START --roundLastValid=$VALID_BLOCK_END --keyDilution=$KEY_DILUTION
sudo -u algorand -E goal account listpartkeys
sudo -u algorand -E goal account partkeyinfo

# generate online txn
sudo -u algorand -E goal account changeonlinestatus --address=$WALLET_ADDRESS --fee=$MIN_UALGO_FEE --online=true --firstvalid=$VALID_BLOCK_START --lastvalid=$(($VALID_BLOCK_START+1000)) --txfile=online.txn

# transfer to offline computer
# sudo qrencode -8 -m 2 -t ansiutf8 -r online.txn

# sign them from a secure offline computer without local storage running a live cd
goal wallet new
goal account import
# enter mnemonic
goal clerk sign --infile="online.txn" --outfile="online.stxn"
goal clerk inspect online.stxn

# transfer back to the node

# raw send
sudo -u algorand -E goal clerk rawsend -f online.stxn
```
