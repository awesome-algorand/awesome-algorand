> This resource is auto indexed by AwesomeAlgo, all credits to php-algorand-sdk, for more details refer to https://github.com/ffsolutions/php-algorand-sdk

---

# PHP Algorand SDK 2.0 (algod, algokey, kmd, transactions and indexer)

A Pure PHP (no dependencies) library for interacting with the Algorand network.

All files in this directory will show you about the best pratices that you should do when implementing  **php-algorand-sdk** into your project.


## Requirements
- PHP 7.3 and above.
- Built-in libcurl support.
- Algorand node, algod, kmd, indexer or PureStake

## Frameworks Compatibility
This SDK was developed to support several PHP Frameworks, tested with:
- **Native Frameworks**
- **FFS**
- **Laravel**
- **Lumen**
- **Yii**
- **Codeigniter**
- **Symfony**


In the **sdk** folder you will find the setup suggestions.


## Quick start

For running this example, you need to install `php-algorand-sdk` library before, and start the node.
```
$ git clone https://github.com/ffsolutions/php-algorand-sdk
$ ./goal node start -d data
$ ./goal kmd start -d data
$ ./algorand-indexer daemon -h -d data
```


After cloning the repository, you need to include the `php-algorand-sdk`:
```php
require_once 'sdk/algorand.php';
require_once 'sdk/algokey.php';

#OR with namespace include

use App\Algorand\algorand;
use App\Algorand\transactions;
use App\Algorand\algokey;
use App\Algorand\b32;
use App\Algorand\msgpack;

```

For use the **algod**:
```php
# Node
$algorand = new Algorand("algod","{algod-token}","localhost",53898); //get the token key in data/algod.admin.token

# PureStake
$algorand = new Algorand("algod","{pure-stake-token}","mainnet-algorand.api.purestake.io/ps2",0,true); //External PureStake

$return=$algorand->get("v2","status");
print_r($return);

```
(see all avaliable functions in **algod.php**)


For use the **kmd**:
```php
#Node only
$algorand_kmd = new  Algorand("kmd","{kmd-token}","localhost",7833); //get the token key in data/kmd-{version}/kmd.token and port in data/kmd-{version}/kmd.net
$return=$algorand_kmd->get("versions");
print_r($return);
```
(see all avaliable functions in **kmd.php**)


For use the **indexer**:
```php
#Node
$algorand_indexer = new Algorand("indexer","{algorand-indexer-token}","localhost",8089);

#PureStake
$algorand_indexer = new Algorand("indexer","{pure-stake-token}","mainnet-algorand.api.purestake.io/idx2",0,true); //true for External PureStake

$return=$algorand_indexer->get("health");
print_r($return);
```
(see all avaliable functions in **indexer.php**)

For use the **algokey**:
```php
$algokey=new  algokey;

$key=$algokey->generate();
print_r($key);
```
(see all avaliable functions in **algokey.php**)

For use the **transactions**:
```php
$algorand_transactions = new  Algorand_transactions;
#Build and Sign a transaction, for details: https://developer.algorand.org/docs/features/transactions

#Payment Transaction (ALGO)

$transaction=array(
        "txn" => array(
                "type" => "pay", //Tx Type
                "fee" => 1000, //Fee
                "fv" => 27151092, //First Valid
                "gen" => "mainnet-v1.0", // GenesisID
                "gh" => "wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=", //Genesis Hash
                "lv" => 27152092, //Last Valid
                "note" => "Testes", //You note
                "snd" => "3DKZLYQJXSUAE7ZCFZN7ODZSOA6733PI5BFM4L7WI4S3K6KEVOOA6KDN2I", //Sender
                "rcv" => "IYVZLDFIF6KUMSDFVIKHPBT3FI5QVZJKJ6BPFSGIJDUJGUUASKNRA4HUHU", //Receiver
                "amt" => 1000, //Amount
            ),
);

```
(see all avaliable functions in **transactions.php**)

## Vídeo Tutorial

[![PHP Algorand SDK Vídeo Tutorial](https://img.youtube.com/vi/7ZoDY6av1-4/0.jpg)](https://www.youtube.com/watch?v=7ZoDY6av1-4)

https://www.youtube.com/watch?v=7ZoDY6av1-4


## Application Examples
See at examples folder.

https://github.com/ffsolutions/php-algorand-sdk/tree/main/examples

![Algorand Wallet PHP GUI](https://raw.githubusercontent.com/ffsolutions/php-algorand-sdk/main/examples/wallet-gui/preview.png "Algorand Wallet PHP GUI")
https://www.youtube.com/watch?v=Ju1f5MrwJKA

![Algorand Asset Manager PHP GUI](https://raw.githubusercontent.com/ffsolutions/php-algorand-sdk/main/examples/asset-manager-gui/preview.png)
https://www.youtube.com/watch?v=b__DhRzAex0

![Algorand Explorer PHP GUI](https://raw.githubusercontent.com/ffsolutions/php-algorand-sdk/main/examples/explorer-gui/preview.png)
https://www.youtube.com/watch?v=b__DhRzAex0


## Complete Guide

### Node setup (macOS and Linux)
Verified on macOS Monterey 12.5.1 and Ubuntu 22.04

For other cases, follow the instructions in Algorand's [developer resources](https://developer.algorand.org/docs/run-a-node/setup/install/) to install a node on your computer.

### Steps:
- 1- Installing Algorand Node
- 2- Installing Algorand Indexer
- 3- Installing and Using the **PHP Algorand SDK**



### For macOS and Linux:
Create a temporary folder to hold the install package and files:
```
$ mkdir ~/node
$ cd ~/node
```


Download the updater script:

#### macOS
```
$ curl https://raw.githubusercontent.com/algorand/go-algorand/rel/stable/cmd/updater/update.sh -O
```

#### Linux
```
$ wget https://raw.githubusercontent.com/algorand/go-algorand/rel/stable/cmd/updater/update.sh
```

Ensure that your system knows it's an executable file:
```
$ chmod 744 update.sh
```


Run the installer from within your node directory:
```
$ ./update.sh -i -c stable -p ~/node -d ~/node/data -n
```


Create and change the config.json
```
$ cp data/config.json.example data/config.json
$ chmod 777 data/config.json
$ cp data/kmd-v{version}/kmd_config.json.example data/kmd-v{version}/kmd_config.json
$ chmod 777 data/kmd-v{version}/kmd_config.json
$ vim data/config.json
```


Change the line, press I to enable edition, make changes, press ESC and type :w + [enter], :q + [enter] to finish.
```
"EndpointAddress": "127.0.0.1:0",  
to
"EndpointAddress": "127.0.0.1:53898",
```


Start Node:
```
./goal node start -d data
./goal kmd start -d data
./algorand-indexer daemon -P "host=127.0.0.1 port=5432 user={user} password={password} dbname=algorand sslmode=disable"  --no-algod
```


To see if the node is running:
```
$ htop
```
Press F10 to close the htop



### Sync Node Network using Fast Catchup
Fast Catchup is a new feature and will rapidly update a node using catchpoint snapshots. A new command on goal node is now available for catchup. The entire process should sync a node in minutes rather than hours or days.


### Get the catchpoint
```
$ wget -qO- https://algorand-catchpoints.s3.us-east-2.amazonaws.com/channel/mainnet/latest.catchpoint
```


Use the sync point captured above and paste into the catchup option
```
./goal node catchup 12400000#ZHHAYEVVUXHMDVIRFUFQLI7DUUMJAEDCJN7WPG6OD4DRBBIWK5UA -d data
```


Node Status:
``
./goal node status -d data
``
Results should show 5 Catchpoint status lines for Catchpoint, total accounts, accounts processed, total blocks , downloaded blocks.
Notice that the 5 Catchpoint status lines will disappear when completed, and then only a few more minutes are needed so sync from that point to the current block. ***Once there is a Sync Time of 0, the node is synced and if fully usable***.
```
Last committed block: 11494
Sync Time: 58.1s
Catchpoint: 12400000#ZHHAYEVVUXHMDVIRFUFQLI7DUUMJAEDCJN7WPG6OD4DRBBIWK5UA
Catchpoint total accounts: 9133629
Catchpoint accounts processed: 7786496
Catchpoint accounts verified: 0
Genesis ID: mainnet-v1.0
Genesis hash: wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=
```

## Installing the Algorand Indexer

For more details: https://developer.algorand.org/docs/run-a-node/setup/indexer/

## Installing and Using the Algorand PHP SDK
Get the node tokens and address:
```
$ cat data/algod.token
$ cat data/kmd-{version}/kmd.token
$ cat data/kmd-{version}/kmd.net
```


Clone Git Hub Project
```
$ git clone https://github.com/ffsolutions/php-algorand-sdk.git
```


After cloning the repository, you need to include the `php-algorand-sdk`:
```php
require_once 'sdk/algorand.php';
require_once 'sdk/algokey.php';
require_once 'sdk/transactions.php';

#OR with namespace include

use App\Algorand\algorand;
use App\Algorand\algokey;
use App\Algorand\transactions;
use App\Algorand\b32;
use App\Algorand\msgpack;
```

## For use the **Algokey**:

### Start the Algokey
```php
$algokey=new  algokey;
```

### Generate New Key/Account/Address
```php
$key=$algokey->generate();
print_r($key);
echo "Words to string: ".implode(" ",$key['words'])."\n";
```

### Words to Private Key and Public Key (Array)
```php
$words=explode(" ","connect produce defense output sibling idea oil siege decline dentist faint electric method notice style cook unlock rice confirm host tone test vehicle able keen"); //2OEZACD77WSR5C2HFEHO2BYHQEATOGFIUW3REGKOGNPPNYPPLROHDU2CQE
$privateKey=$algokey->WordsToPrivateKey($words); //Array
$privateKey_decoded=base64_decode($privateKey);
$publicKey=$algokey->publicKeyFromPrivateKey($privateKey);
$publicKey_decoded=$algokey->publicKeyFromPrivateKey($privateKey,false);
echo "Private Key: ".$privateKey."\n";
echo "Private Key decoded: ".$privateKey_decoded."\n";
echo "Public Key B32: ".$publicKey."\n";
echo "Public Key decoded: ".$publicKey_decoded."\n";
```

### Private Key to Words
```php
$privateKey="eenqctbZ48E5E8jHoc6jdhTGW/q6L3BP7l3gJnJ+P17TiZAIf/2lHotHKQ7tBweBATcYqKW3EhlOM1724e9cXA==";
$return_words=$algokey->privateKeyToWords($privateKey);
print_r($return_words);
echo "Words: ".implode(" ",$return_words)."\n";
```

### Sign Transaction with Algokey PHP
```php
$transaction=array(
        "txn" => array(
                "type" => "pay", //Tx Type
                "fee" => 1000, //Fee
                "fv" => 28237321, //First Valid
                "gen" => "mainnet-v1.0", // GenesisID
                "gh" => "wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=", //Genesis Hash
                "lv" => 28238321, //Last Valid
                "note" => "", //You note
                "snd" => "2QAXTOHQJQH6I4FM6RWUIISXKFJ2QA4NVWELMIJ5XAKZB4N4XIEX7F5KPU", //Sender
                "rcv" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //Receiver
                "amt" => 1003, //Amount
            ),
);

$transaction_raw=$algorand_transactions->encode($transaction);
$signature=$algokey->sign($transaction_raw,$privateKey);
```

### Broadcasts a raw transaction to the network.
```php
$transaction_raw_signed=$algorand_transactions->encode($transaction,true,$signature);

$algorand = new Algorand("algod","4820e6e45f339e0026eaa2b74c2aa7d8735cbcb2db0cf0444fb492892e1c09b7","localhost",53898);
$params['transaction']=$transaction_raw_signed;
print_r($params);
$return=$algorand->post("v2","transactions",$params);
print_r($return);
```

## For use the **Algod**:
Start the SDK
```php
#Node
$algorand = new  Algorand("algod",'{algod-token}',"localhost",53898); //get the token key in data/algod.token

#PureStake
$algorand = new Algorand("algod","{pure-stake-token}","mainnet-algorand.api.purestake.io/ps2",0,true); //true for External PureStake
```

### Get the versions
```php
$return=$algorand->get("versions");
```


### Gets the current node status.
```php
$return=$algorand->get("v2","status");
```


### Gets the node status after waiting for the given round.
```php
$return=$algorand->get("v2","status","wait-for-block-after",{block});
```

### Gets the genesis information.
```php
return=$algorand->get("genesis");
```

### Returns 200 (OK) if healthy.
```php
$return=$algorand->get("health");
```

### Return metrics about algod functioning.
```php
$return=$algorand->get("metrics");
```

### Gets the current swagger spec.
```php
$return=$algorand->get("swagger.json");
```

### Get account information and balances.
```php
$return=$algorand->get("v2","accounts","{address}","?exclude=none&?format=json"); //?exclude=none or all. When set to all will exclude asset holdings, &format=json or msgpack (opcional, default json)
```

### Get account information about a given app.
```php
$return=$algorand->get("v2","accounts","{address}","applications","{application-id}");
```

### Get account information about a given asset.
```php
$return=$algorand->get("v2","accounts","{address}","assets","{asset-id}");
```

### Get a list of unconfirmed transactions currently in the transaction pool by address.
```php
$return=$algorand->get("v2","accounts","{address}","transactions","pending","?format=json&max=2");
```

### Get application information.
```php
$return=$algorand->get("v2","applications","{application-id}");
```

### Get box information for a given application.
```php
$return=$algorand->get("v2","applications","{application-id}","box","?name=");
```

### Get all box names for a given application.
```php
$return=$algorand->get("v2","applications","{application-id}","boxes","?max=");
```

### Get asset information.
```php
$return=$algorand->get("v2","assets","{asset-id}");
```

### Get the block for the given round.
```php
$return=$algorand->get("v2","blocks","{block}");
```

### Get the block hash for the block on the given round.
```php
$return=$algorand->get("v2","blocks","{block}","hash");
```

### Gets a proof for a given light block header inside a state proof commitment
```php
$return=$algorand->get("v2","blocks","{block}","lightheader","proof");
```

### Get a proof for a transaction in a block.
```php
$return=$algorand->get("v2","blocks","{round}","transactions","{txid}","proof");
```

### Starts a catchpoint catchup. For the last catchpoint access: https://algorand-catchpoints.s3.us-east-2.amazonaws.com/channel/mainnet/latest.catchpoint
```php
$return=$algorand->post("v2","catchup","{catchpoint}");
```

### Aborts a catchpoint catchup.
```php
$return=$algorand->delete("v2","catchup","{catchpoint}");
```

### Get a LedgerStateDelta object for a given round
```php
$return=$algorand->get("v2","deltas","{round}");
```

### Get the current supply reported by the ledger.
```php
$return=$algorand->get("v2","ledger","supply");
```

### Returns the minimum sync round the ledger is keeping in cache.
```php
$return=$algorand->get("v2","ledger","sync");
```

### Removes minimum sync round restriction from the ledger.
```php
$return=$algorand->delete("v2","ledger","sync");
```

### Given a round, tells the ledger to keep that round in its cache.
```php
$return=$algorand->post("v2","ledger","sync","{round}");
```

### Add a participation key to the node
```php
$params['body']="{participationkey}";
$return=$algorand->post("v2","participation",$params);
```


### Return a list of participation keys
```php
$return=$algorand->get("v2","participation");
```

### Append state proof keys to a participation key
```php
$params['body']="{keymap}";
$return=$algorand->post("v2","participation","{participation-id}",$params);
```


### Get participation key info given a participation ID
```php
$return=$algorand->get("v2","participation","{participation-id}");
```

### Delete a given participation key by ID
```php
$return=$algorand->delete("v2","participation","{participation-id}");
```

### Special management endpoint to shutdown the node. Optionally provide a timeout parameter to indicate that the node should begin shutting down after a number of seconds.
```php
$params['params']=array("timeout" => 0);
$return=$algorand->post("v2","shutdown", $params);
```

### Get a state proof that covers a given round
```php
$return=$algorand->get("v2","stateproofs","{round}");
```

### Compile TEAL source code to binary, produce its hash
```php
$params['body']="";
$return=$algorand->post("v2","teal","compile",$params);
```

### Disassemble program bytes into the TEAL source code.
```php
$params['body']="";
$return=$algorand->post("v2","teal","disassemble",$params);
```

### Provide debugging information for a transaction (or group).
```php
$params['$params']=array(
                        "accounts" => array(), //Account
                        "apps" => array(), //Application
                        "latest-timestamp" => 0, //integer
                        "protocol-version" => "", //string
                        "round" => 0, //integer
                        "sources" => array(), //DryrunSource
                        "txns" => "", //string (json) > array
                   );
$return=$algorand->post("v2","teal","dryrun",$params);
```

### Broadcasts a raw transaction to the network.
```php
#Generate and Sign the transaction with cli or this sdk:
//CLI sample
#./goal clerk send -a 1000 -f {address_from} -t {address_to} -d data -o transactions/tran.txn
#./goal clerk sign --infile="trans/tran.txn" --outfile="trans/tran.stxn" -d data


$params['file']="transactions/tran.stxn";
$params['transaction']="";
$return=$algorand->post("v2","transactions",$params);

```

### Get parameters for constructing a new transaction
```php
$return=$algorand->get("v2","transactions","params");
```

### Get a list of unconfirmed transactions currently in the transaction pool.
```php
$return=$algorand->get("v2","transactions","pending","?format=json&max=2");
```

### Get a specific pending transaction.
```php
$return=$algorand->get("v2","transactions","pending","{txid}","?format=json");
```



For more details: https://developer.algorand.org/docs/reference/rest-apis/algod/v2/

## For use the **KMD**:
Start the SDK
```php
$algorand_kmd = new  Algorand("kmd","{kmd-token}","localhost",7833); //get the token key in data/kmd-{version}/kmd.token and port in data/kmd-{version}/kmd.net

$algorand_transactions = new  Algorand_transactions;
```

#### Get Versions
```php
$return=$algorand_kmd->get("versions");
```

#### Get swagger.json
```php
$return=$algorand_kmd->get("swagger.json");
```

#### Create Wallet
```php
$params['params']=array(
    "wallet_name" => "",
    "wallet_password" => "",
    "wallet_driver_name" => "sqlite",
);
$return=$algorand_kmd->post("v1","wallet",$params);
```

#### Wallet List
```php
$return=$algorand_kmd->get("v1","wallets");
```

#### Wallet Init
```php
$params['params']=array(
    "wallet_id" => "",
    "wallet_password" => "",
);
$return=$algorand_kmd->post("v1","wallet","init",$params);
$return_array=json_decode($return['response']);
$wallet_handle_token=$return_array->wallet_handle_token;
```


#### Wallet Info
```php
$params['params']=array(
    "wallet_handle_token" => $wallet_handle_token,
);
$return=$algorand_kmd->post("v1","wallet","info",$params);
```


#### Wallet Rename
```php
$params['params']=array(
    "wallet_id" => "",
    "wallet_name" => "",
    "wallet_password" => "",
);
$return=$algorand_kmd->post("v1","wallet","rename",$params);
```


#### Wallet Handle Token Release
```php
$params['params']=array(
    "wallet_handle_token" => $wallet_handle_token,
);
$return=$algorand_kmd->post("v1","wallet","release",$params);
```


#### Wallet Handle Token Renew
```php
$params['params']=array(
    "wallet_handle_token" => $wallet_handle_token,
);
$return=$algorand_kmd->post("v1","wallet","renew",$params);
```


#### Generate a key
```php
$params['params']=array(
    "display_mnemonic" => false,
    "wallet_handle_token" => $wallet_handle_token
);
$return=$algorand_kmd->post("v1","key",$params);
```


#### Delete a key
```php
$params['params']=array(
    "address" => "",
    "wallet_handle_token" => $wallet_handle_token,
    "wallet_password" => ""
);
$return=$algorand_kmd->delete("v1","key",$params);
```


#### Export a key
```php
$params['params']=array(
    "address" => "XI56XZXQ64QD7IO5UBRC2RBZP6TQHP5WEILLFMBTKPXRKK7343R3KZAWNQ",
    "wallet_password" => "testes",
    "wallet_handle_token" => $wallet_handle_token
);
$return=$algorand_kmd->post("v1","key","export",$params);

$export=json_decode($return['response']);

require_once 'sdk/algokey.php';
$algokey=new algokey;

$words=$algokey->privateKeyToWords($export->private_key);

print_r($words);
```


#### Import a key
```php
require_once 'sdk/algokey.php';

$algokey=new algokey;
$words="ripple trap smoke crop name donor sun actor wreck disease mushroom sweet because phrase involve sail umbrella control swing uncle card phrase human absent marble";
$words_array=explode(" ",$words);

$privatekey=$algokey->WordsToprivateKey($words_array);

$params['params']=array(
    "private_key" => $privatekey,
    "wallet_handle_token" => $wallet_handle_token
);
$return=$algorand_kmd->post("v1","key","import",$params);
```


#### List keys in wallet
```php
$params['params']=array(
    "wallet_handle_token" => $wallet_handle_token
);
$return=$algorand_kmd->post("v1","key","list",$params);
```


#### Master Key export
```php
$params['params']=array(
    "wallet_password" => "",
    "wallet_handle_token" => $wallet_handle_token
);
$return=$algorand_kmd->post("v1","master-key","export",$params);
```


#### Delete a multisig
```php
$params['params']=array(
    "address" => "",
    "wallet_handle_token" => $wallet_handle_token,
    "wallet_password" => ""
);
$return=$algorand_kmd->delete("v1","multisig",$params);
```


#### Export a multisig
```php
$params['params']=array(
    "address" => "",
    "wallet_handle_token" => $wallet_handle_token
);
$return=$algorand_kmd->post("v1","multisig","export",$params);
```


#### Import a multisig
```php
$params['params']=array(
    "multisig_version" => "1",
    "pks" => array(''),
    "threshold" => 1,
    "wallet_handle_token" => $wallet_handle_token
);
$return=$algorand_kmd->post("v1","multisig","import",$params);
```


#### List multisig in wallet
```php
$params['params']=array(
    "wallet_handle_token" => $wallet_handle_token
);
$return=$algorand_kmd->post("v1","multisig","list",$params);
```


#### Sign a multisig transaction
```php
$params['params']=array(
    "partial_multisig" => array(
                                "Subsigs" => array(
                                                    "Key" => array(),
                                                    "Sig" => array(),
                                ),
                                "Threshold" => 1,
                                "Version" => 1
                          ),
    "public_key" => array(''),
    "signer" => array(''),
    "transaction" => "",
    "wallet_handle_token" => $wallet_handle_token,
    "wallet_password" => ""
);
$return=$algorand_kmd->post("v1","multisig","sign",$params);
```


#### Sign a program for a multisig account
```php
$params['params']=array(
    "address" => "",
    "data" => "",
    "partial_multisig" => array(
                                "Subsigs" => array(
                                                    "Key" => array(),
                                                    "Sig" => array(),
                                ),
                                "Threshold" => 1,
                                "Version" => 1
                          ),
    "public_key" => array(''),
    "wallet_handle_token" => $wallet_handle_token,
    "wallet_password" => ""
);
$return=$algorand_kmd->post("v1","multisig","signprogram",$params);
```


#### Sign program
```php
$params['params']=array(
    "address" => "",
    "data" => "",
    "wallet_handle_token" => $wallet_handle_token,
    "wallet_password" => ""
);
$return=$algorand_kmd->post("v1","program","sign",$params);
```

## For use **Transactions**:

### To sign with Algokey load the Private Key
```php
$words=explode(" ","connect produce defense output sibling idea oil siege decline dentist faint electric method notice style cook unlock rice confirm host tone test vehicle able keen"); //2OEZACD77WSR5C2HFEHO2BYHQEATOGFIUW3REGKOGNPPNYPPLROHDU2CQE
$privateKey=$algokey->WordsToPrivateKey($words); //Array to load words
```

### To sign with KMD load the Wallet
```php
$algorand_kmd = new Algorand("kmd","{kmd-token}","localhost",7833); //get the token key in data/kmd-{version}/kmd.token and port in data/kmd-{version}/kmd.net

#Wallet Init  //Only if you will use the KMD.
$params['params']=array(
    "wallet_id" => "",
    "wallet_password" => "tests",
);
$return=$algorand_kmd->post("v1","wallet","init",$params);
$return_array=json_decode($return['response']);
$wallet_handle_token=$return_array->wallet_handle_token;
```


### Build and Sign a transaction
For details: https://developer.algorand.org/docs/features/transactions

**Types**:

**appl** = ApplicationCallTx allows creating, deleting, and interacting with an application

**cert** = CompactCertTx records a compact certificate

**keyreg** = KeyRegistrationTx indicates a transaction that registers participation keys

**acfg** = AssetConfigTx creates, re-configures, or destroys an asset

**axfer** = AssetTransferTx transfers assets between accounts (optionally closing)

**afrz** = AssetFreezeTx changes the freeze status of an asset

**pay** = PaymentTx indicates a payment transaction

### Build Transaction
#### Application Call Transaction
```php
$transaction=array(
        "txn" => array(
                "type" => "appl", //Tx Type
                "snd" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //Sender
                "fee" => 1000, //Fee
                "fv" => 13029982, //First Valid
                "lv" => 13023082, //Last Valid
                "gh" => "wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=", //Genesis Hash
                "apid" => "", //Application ID or empty if creating
                "apan" => "", //OnComplete
                "apat" => "", //Accounts
                "apap" => "", //Approval Program
                "apaa" => "", //App Arguments
                "apsu" => "", //Clear State Program
                "apfa" => "", //Foreign Apps
                "apas" => "", //Foreign Assets
                "apgs" => array( //GlobalStateSchema
                            "nui" => "", //Number Ints
                            "nbs" => "", //Number Byteslices
                        ),
                "apls" => array( //LocalStateSchema
                            "nui" => "", //Number Ints
                            "nbs" => "", //Number Byteslices
                        ),
            ),
);
```
#### Compact Certificate
```php
$transaction=array(
        "txn" => array(
                "type" => "cert", //Tx Type
                "snd" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //Sender
                "fee" => 1000, //Fee
                "fv" => 13029982, //First Valid
                "lv" => 13023082, //Last Valid
                "gh" => "wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=", //Genesis Hash
                "certrnd" => "", //Round
                "certtype" => "", //CompactCertType
                "cert" => "", //Cert
            ),
);
```

#### Register account online
```php
$transaction=array(
        "txn" => array(
                "type" => "keyreg", //Tx Type
                "selkey" => "X84ReKTmp+yfgmMCbbokVqeFFFrKQeFZKEXG89SXwm4=", //SelectionPK
                "fee" => 1000, //Fee
                "fv" => 13009389, //First Valid
                "gh" => "wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=", //Genesis Hash
                "lv" => 13009489, //Last Valid
                "votefst" => 13009489, //VoteFirst
                "votelst" => 13009589, //VoteLast
                "votekd" => 1730, //VoteKeyDilution
                "votekey" => "eXq34wzh2UIxCZaI1leALKyAvSz/+XOe0wqdHagM+bw=",
                "snd" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //Sender
            ),
);
```

#### Register account offline
```php
$transaction=array(
        "txn" => array(
                "type" => "keyreg", //Tx Type
                "fee" => 1000, //Fee
                "fv" => 13009389, //First Valid
                "gh" => "wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=", //Genesis Hash
                "lv" => 13009489, //Last Valid
                "snd" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //Sender
            ),
);
```

#### Close an Account
```php
$transaction=array(
        "txn" => array(
                "type" => "pay", //Tx Type
                "close" => "EW64GC6F24M7NDSC5R3ES4YUVE3ZXXNMARJHDCCCLIHZU6TBEOC7XRSBG4",
                "fee" => 1000, //Fee
                "fv" => 13009389, //First Valid
                "lv" => 13009489, //Last Valid
                "gen" => "mainnet-v1.0", // GenesisID
                "gh" => "wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=", //Genesis Hash
                "note" => "Testes", //You note
                "snd" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //Sender
                "rcv" => "EW64GC6F24M7NDSC5R3ES4YUVE3ZXXNMARJHDCCCLIHZU6TBEOC7XRSBG4", //Receiver
            ),
);
```

#### Create an Asset
```php
$transaction=array(
        "txn" => array(
                "type" => "acfg", //Tx Type
                "snd" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //Sender
                "fee" => 1000, //Fee
                "fv" => 13027977, //First Valid
                "lv" => 13028977, //Last Valid
                "gh" => "wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=", //Genesis Hash
                "apar" => array( //AssetParams
                        //"am" => "", //MetaDataHash
                        "an" => "MyToken", //AssetName
                        "au" => "https://mytoken.site", //URL
                        "c" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //ClawbackAddr
                        "dc" => 2, //Decimals
                        "f" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //FreezeAddr
                        "m" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //ManagerAddr
                        "r" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //ReserveAddr
                        "t" => 100000000000, //Total
                        "un" => "MTK", //UnitName
                    ),

            ),
);
```

#### Reconfigure an Asset
```php
$transaction=array(
        "txn" => array(
                "type" => "acfg", //Tx Type
                "snd" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //Sender
                "fee" => 1000, //Fee
                "fv" => 13027977, //First Valid
                "lv" => 13028977, //Last Valid
                "gh" => "wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=", //Genesis Hash
                "caid" => 185553584,
                "apar" => array( //AssetParams
                        "c" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //ClawbackAddr
                        "f" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //FreezeAddr
                        "m" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //ManagerAddr
                        "r" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //ReserveAddr
                    ),

            ),
);
```

#### Destroy an Asset
```php
$transaction=array(
        "txn" => array(
                "type" => "acfg", //Tx Type
                "snd" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //Sender
                "fee" => 1000, //Fee
                "fv" => 13027977, //First Valid
                "lv" => 13028977, //Last Valid
                "gh" => "wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=", //Genesis Hash
                "caid" => 185553584, //ConfigAsset ID
            ),
);
```

#### Opt-in to an Asset
```php
$transaction=array(
        "txn" => array(
                "type" => "axfer", //Tx Type
                "arcv" => "DOVA6TULHNY2DCS65LVT5QYLWZGM7WC2GISPRGNDWDUH3KUX56ZLQJW3AY", //AssetReceiver
                "snd" => "DOVA6TULHNY2DCS65LVT5QYLWZGM7WC2GISPRGNDWDUH3KUX56ZLQJW3AY", //Sender
                "fee" => 1000, //Fee
                "fv" => 13028464, //First Valid
                "lv" => 13028564, //Last Valid
                "gh" => "wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=", //Genesis Hash
                "xaid" => 185553584, //XferAsset ID
            ),
);
```

#### Revoke an Asset
```php
$transaction=array(
        "txn" => array(
                "aamt" => 100,
                "type" => "axfer", //Tx Type
                "arcv" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //AssetReceiver
                "asnd" => "DOVA6TULHNY2DCS65LVT5QYLWZGM7WC2GISPRGNDWDUH3KUX56ZLQJW3AY", //AssetSender
                "snd" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //Sender
                "fee" => 1000, //Fee
                "fv" => 13028982, //First Valid
                "lv" => 13029982, //Last Valid
                "gh" => "wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=", //Genesis Hash
                "xaid" => 185553584, //XferAsset ID
            ),
);
```

#### Freeze an Asset
```php
$transaction=array(
        "txn" => array(
                "afrz" => false,
                "type" => "afrz", //Tx Type
                "fadd" => "DOVA6TULHNY2DCS65LVT5QYLWZGM7WC2GISPRGNDWDUH3KUX56ZLQJW3AY", //FreezeAccount
                "snd" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //Sender
                "fee" => 1000, //Fee
                "fv" => 13029982, //First Valid
                "lv" => 13023082, //Last Valid
                "gh" => "wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=", //Genesis Hash
                "faid" => 185553584, //FreezeAsset
            ),
);
```

#### Transfer an Asset
```php
$transaction=array(
        "txn" => array(
                "aamt" => 100,
                "type" => "axfer", //Tx Type
                "arcv" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //AssetReceiver
                "snd" => "DOVA6TULHNY2DCS65LVT5QYLWZGM7WC2GISPRGNDWDUH3KUX56ZLQJW3AY", //Sender
                "fee" => 1000, //Fee
                "fv" => 13028982, //First Valid
                "lv" => 13029982, //Last Valid
                "gh" => "wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=", //Genesis Hash
                "xaid" => 185553584, //XferAsset ID
            ),
);
```

#### Payment Transaction (ALGO)
```php
$transaction=array(
        "txn" => array(
                "type" => "pay", //Tx Type
                "fee" => 1000, //Fee
                "fv" => 13009389, //First Valid
                "gen" => "mainnet-v1.0", // GenesisID
                "gh" => "wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=", //Genesis Hash
                "lv" => 13009489, //Last Valid
                "note" => "Testes", //You note
                "snd" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //Sender
                "rcv" => "IYVZLDFIF6KUMSDFVIKHPBT3FI5QVZJKJ6BPFSGIJDUJGUUASKNRA4HUHU", //Receiver
                "amt" => 1000, //Amount
            ),
);
```

### Sign Transaction
```php
$params['params']=array(
   "transaction" => $algorand_kmd->txn_encode($transaction),
   "wallet_handle_token" => $wallet_handle_token,
   "wallet_password" => "testes"
);

$return=$algorand_kmd->post("v1","transaction","sign",$params);
$r=json_decode($return['response']);
$txn=base64_decode($r->signed_transaction);
echo $txn;
```

#### Broadcasts a raw transaction to the network.
```php
$algorand = new Algorand_algod('{algod-token}',"localhost",53898);
$params['transaction']=$txn;
$return=$algorand->post("v2","transactions",$params);
$txId=$return['response']->txId;
echo "txId: $txId";
```

For more details: https://developer.algorand.org/docs/reference/rest-apis/kmd/

## Atomic Transfers
Create Transactions
```php
$transactions=array();

//Transaction 1
$transactions[]=array(
        "txn" => array(
                "type" => "pay", //Tx Type
                "fee" => 1000, //Fee
                "fv" => 28259644, //First Valid
                "gen" => "mainnet-v1.0", // GenesisID
                "gh" => "wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=", //Genesis Hash
                "lv" => 28260644, //Last Valid
                "note" => "Testes", //You note
                "snd" => "3DKZLYQJXSUAE7ZCFZN7ODZSOA6733PI5BFM4L7WI4S3K6KEVOOA6KDN2I", //Sender
                "rcv" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //Receiver
                "amt" => 102, //Amount
            ),
);

//Transaction 2
$transactions[]=array(
        "txn" => array(
                "type" => "pay", //Tx Type
                "fee" => 1000, //Fee
                "fv" => 28259644, //First Valid
                "gen" => "mainnet-v1.0", // GenesisID
                "gh" => "wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=", //Genesis Hash
                "lv" => 28260644, //Last Valid
                "note" => "Testes 2", //You note
                "snd" => "3DKZLYQJXSUAE7ZCFZN7ODZSOA6733PI5BFM4L7WI4S3K6KEVOOA6KDN2I", //Sender
                "rcv" => "DI65FPLNUXOJJR47FDTIB5TNNIA5G4EZFA44RZMRBE7AA4D453OYD2JCW4", //Receiver
                "amt" => 203, //Amount
            ),
);
```

Group Transactions
```php
$groupid=$algorand_transactions->groupid($transactions);

#Assigns Group ID
$transactions[0]['txn']['grp']=$groupid;
$transactions[1]['txn']['grp']=$groupid;
```

Sign Transactions with Algokey
```php
#Sign Transaction 1

$txn="";
$transaction_raw=$algorand_transactions->encode($transactions[0]);
$signature=$algokey->sign($transaction_raw,$privateKey);
$txn.=$algorand_transactions->encode($transactions[0],true,$signature);

#Sign Transaction 2
$transaction_raw=$algorand_transactions->encode($transactions[1]);
$signature=$algokey->sign($transaction_raw,$privateKey);
$txn.=$algorand_transactions->encode($transactions[1],true,$signature);

```

OR

Sign Transactions with KMD
```php
#Sign Transaction 1
$txn="";
$params['params']=array(
   "transaction" => $algorand_transactions->encode($transactions[0]),
   "wallet_handle_token" => $wallet_handle_token,
   "wallet_password" => "tests",
);

$return=$algorand_kmd->post("v1","transaction","sign",$params);
$r=json_decode($return['response']);
$txn.=base64_decode($r->signed_transaction);


#Sign Transaction 2
$params['params']=array(
   "transaction" => $algorand_transactions->encode($transactions[1]),
   "wallet_handle_token" => $wallet_handle_token,
   "wallet_password" => "tests",
);
$return=$algorand_kmd->post("v1","transaction","sign",$params);
$r=json_decode($return['response']);
$txn.=base64_decode($r->signed_transaction);;
```

Send Transaction Group
```php
#Broadcasts a raw atomic transaction to the network.
$algorand = new Algorand("algod","4820e6e45f339e0026eaa2b74c2aa7d8735cbcb2db0cf0444fb492892e1c09b7","localhost",53898);
$params['transaction']=$txn;
$return=$algorand->post("v2","transactions",$params);
$txId=$return['response']->txId;
echo "txId: $txId";
```

For more details: https://developer.algorand.org/docs/features/atomic_transfers/

## For use the **Indexer**:
Start the SDK
```php
$algorand_indexer = new Algorand("indexer","{algorand-indexer-token}","localhost",8089);
```


#### Get health, Returns 200 if healthy.
```php
$return=$algorand_indexer->get("health");
```


#### Search for accounts.
```php
$query=http_build_query(array(
    //"application-id" => 0, //integer
    //"asset-id" => 0, //integer
    //"auth-addr" => "", //string
    //"currency-greater-than" => 0, //integer
    //"currency-less-than" => 0, //integer
    "limit" => 100, //integer
    //"next" => "", //string - previous return {next-token}
    //"round" => 0, //integer
));
$return=$algorand_indexer->get("v2","accounts?".$query);
```


#### Lookup account information.
```php
$return=$algorand_indexer->get("v2","accounts","{account-id}");
```


#### Lookup account transactions.
```php
$query=http_build_query(array(
    //"application-id" => 0, //integer
    "asset-id" => 0, //integer
    "after-time" => "", //string (date-time)
    "before-time" => "", //string (date-time)
    "currency-greater-than" => 0, //integer
    "currency-less-than" => 0, //integer
    "limit" => 100, //integer
    //"max-round" => 0, //integer
    //"min-round" => 0, //integer
    //"next" => "", //string - previous return {next-token}
    "note-prefix" => "", //string
    "rekey-to" => false, //boolean
    //"round" => "", //integer
    "sig-type" => "sig", //enum (sig, msig, lsig)
    "tx-type" => "pay", //enum (pay, keyreg, acfg, axfer, afrz, appl)
    "txid" => "", //string
));

$return=$algorand_indexer->get("v2","accounts","{account-id}","transactions?".$query);
```


#### Search for applications
```php
$query=http_build_query(array(
    "application-id" => 0, //integer
    "limit" => 100, //integer
    //"next" => "", //string - previous return {next-token}
));
$return=$algorand_indexer->get("v2","applications?".$query);
```


#### Lookup application.
```php
$return=$algorand_indexer->get("v2","applications","{application-id}");
```


#### Search for assets.
```php
$query=http_build_query(array(
    //"asset-id" => 0, //integer
    //"creator" => 0, //integer
    "limit" => 100, //integer
    //"name" => "", //string
    //"next" => "", //string - previous return {next-token}
    //"unit" => "", //string
));
$return=$algorand_indexer->get("v2","assets?".$query);
```


#### Lookup asset information.
```php
$return=$algorand_indexer->get("v2","assets","{asset-id}");
```


#### Lookup the list of accounts who hold this asset
```php
$query=http_build_query(array(
    //"currency-greater-than" => 0, //integer
    //"currency-less-than" => 0, //integer
    "limit" => 100, //integer
    //"next" => "", //string - previous return {next-token}
    //"round" => "", //integer
));
$return=$algorand_indexer->get("v2","assets","{asset-id}","balances?".$query);
```


#### Lookup the list of accounts who hold this asset
```php
$query=http_build_query(array(
    "address" => "", //string
    "address-role" => "", //enum (sender, receiver, freeze-target)
    "after-time" => "", //string (date-time)
    "before-time" => "", //string (date-time)
    "currency-greater-than" => 0, //integer
    //"currency-less-than" => 0 //integer
    "exclude-close-to" => false, //boolean
    "limit" => 100, //integer
    "max-round" => 0, //integer
    "min-round" => 0, //integer
    //"next" => "", //string - previous return {next-token}
    "note-prefix" => "", //string
    "rekey-to" => false, //boolean
    //"round" => "", //integer
    "sig-type" => "sig", //enum (sig, msig, lsig)
    "tx-type" => "pay", //enum (pay, keyreg, acfg, axfer, afrz, appl)
    "txid" => "", //string
));
$return=$algorand_indexer->get("v2","assets","{asset-id}","transactions".$query);
```


#### Lookup block.
```php
$return=$algorand_indexer->get("v2","blocks","{round-number}");
```


#### Search for transactions.
```php
$query=http_build_query(array(
    "address" => "", //string
    "address-role" => "sender", //enum (sender, receiver, freeze-target)
    "after-time" => "", //string (date-time)
    "application-id" => 0, //integer
    "asset-id" => 0, //integer
    "before-time" => "", //string (date-time)
    "currency-greater-than" => 0, //integer
    "currency-less-than" => 0, //integer
    "exclude-close-to" => "false", //boolean
    "limit" => "100", //integer
    "min-round" => 2466647, //integer
    "max-round" => 2566647, //integer
    "next" => "", //string - previous return {next-token}
    "note-prefix" => "", //string
    "rekey-to" => false, //boolean
    //"round" => 2566247, //integer
    "sig-type" => "sig", //enum (sig, msig, lsig)
    "tx-type" => "pay", //enum (pay, keyreg, acfg, axfer, afrz, appl)
    "txid" => "", //string
));
```


#### Lookup a single transaction.
```php
$return=$algorand_indexer->get("v2","transactions","{txid}");
```


For more details: https://developer.algorand.org/docs/reference/rest-apis/indexer/



## Print the results
Full response with debug (json response)
```php
print_r($return);
```

Only response array
```php
print_r(json_decode($return['response']));
```

Only erros messages  array
```php
print_r(json_decode($return['message']));
```


## Configurations
To enable Debug
```php
$algorand->debug(1);
```

To enable SSL
```php
$algorand->setSSL('/home/felipe/certificate.cert');
```

## License
php-algorand-sdk is licensed under a MIT license. See the [LICENSE](https://github.com/ffsolutions/php-algorand-sdk/blob/master/LICENSE) file for details.


## Donate
If you would like to donate to help maintain our online nodes, this and future projects, this is our ALGO (Algorand) Wallet: IYVZLDFIF6KUMSDFVIKHPBT3FI5QVZJKJ6BPFSGIJDUJGUUASKNRA4HUHU

Thank you!
