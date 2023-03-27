```
      _       __                 ____  _____   _               
     / \     [  |               |_   \|_   _| (_)              
    / _ \     | |  .--./)  .--.   |   \ | |   __   _ .--..--.  
   / ___ \    | | / /'`\;/ .'`\ \ | |\ \| |  [  | [ `.-. .-. | 
 _/ /   \ \_  | | \ \._//| \__. |_| |_\   |_  | |  | | | | | | 
|____| |____|[___].',__`  '.__.'|_____|\____|[___][___||__||__]
                 ( ( __))                                      
                                                       by cusma
```
# AlgoNim: let's play a crypto-Nim on Algorand from the CLI

## What's Nim?
[**Nim**](https://en.wikipedia.org/wiki/Nim) is a very simple mathematical game of strategy for two players. With a lot of imagination let's name them **Alice** and **Bob**.

Just to be fair from the very beginning: Nim is a **zero-sum game** and has been **"mathematically solved"**, this means that exists an **"easily calculated"** perfect strategy to determine which player will win and what winning moves are open to that player.

**So if Alice is a computer, Bob better avoid betting on winning the game.**

## What's AlgoNim?
**AlgoNim** is a cryptographic version of Nim that runs on [Algorand](https://algorand.foundation/) Layer 1, directly on the Pure Proof of Stake consensus protocol, so nobody can cheat. The game implementation takes advantage of all the features introduced in Algorand 2.0 protocol: [**Algorand Standard Assets (ASA)**](https://developer.algorand.org/docs/features/asa/), [**Atomic Transfers (AT)**](https://developer.algorand.org/docs/features/atomic_transfers/) and [**Algorand Smart Contracts (ASC1)**](https://developer.algorand.org/docs/features/asc1/) using Algorand  [**Python SDK**](https://developer.algorand.org/docs/reference/sdks/#python) +  [**PyTeal**](https://github.com/algorand/pyteal). PyTeal is a binding for [**TEAL**](https://developer.algorand.org/docs/features/asc1/teal_overview/), the **stateless bytecode stack based** language for ASC1, in this sense AlgoNim is a truly stateless game.

Through the **seamless interaction** between Algorand Python SDK and PyTeal, AlgoNim **automatically writes** and initializes a **dedicated set of stateless TEAL ASC1s and ASAs** for each match. The whole match set-up **takes few seconds** and **costs about 0.008 ALGOS** for transactions fees. AlgoNim accounts initialization and opt-in **require minimum balances**, so the Dealer needs 0.8 ALGO that can be refunded by slightly enhancing the TEAL ASCs1 making them more cost-efficient. Considerng that a new ASA + ASC1 architecture is generated for each match, **this time/cost performance is quite impressive if compared to other blockchains**.

AlgoNim is played entirely from the **command line interface**. Find other AlgoNim players: https://t.me/algonim

## AlgoNim rules
AlgoNim is based on **Nim's "normal" single heap variant**. Alice is the player who creates the match: she is the **Dealer** and sets up the game table. Bob is the **Opponent**.

Rules are trivial:
1. The Dealer chooses a heap of **N** pieces to be palced on the game table for the match;
2. The Dealer chooses the number **M** of pieces that can be removed at the most from the game table in each turn;
3. Alice and Bob choose who moves first;
4. On each turn each player removes **at least 1** and **at the most M** pieces from the game table;

**Who removes the last piece of the heap form the table wins the match!**

Alice and Bob may choose **betting** some ALGOs for the match. Further implementations will accept **AlgoNim ASA Score Points** other then the betting reward for the matches, this will enable an **AlgoNim global ranking** too!

## Install AlgoNim
### Step 1 - Python modules
AlgoNim uses the following Python3 modules:
1. `msgpack`
2. `docopt`
3. `algosdk`
4. `pyteal`

so you need to install them (if not already present):

```bash
$ pip3 install --upgrade msgpack
$ pip3 install --upgrade docopt
$ pip3 install --upgrade py-algorand-sdk
$ pip3 install --upgrade pyteal
```

### Step 2 - Environment setting
To run AlgoNim smoothly you need to set the following environmental variables:
```bash
$ export ALGORAND_DATA=/path/to/node/data
$ export PATH=/path/to/node/:$PATH
```
Attention: setting `$ALGORAND_DATA` on your node you choose playing AlgoNim on MainNet, TestNet or BetaNet.

### Step 3 - AlgoNim files
Copy following AlgoNim files into your `node` directory (the same of `goal`):

1. `algonim.py`
2. `algonim_asa.py`
3. `algonim_asc1.py`
4. `algonim_moves.py`
5. `algonim_lib.py`

## How to play
Playing AlgoNim from your CLI is pretty easy, just ask for help:

**Input**
```bash
$ python3 algonim.py --help
```
**Output**
```
AlgoNim, the first crypto-mini-game on Algorand! (by cusma)
Usage:
  algonim.py setup <dealer_mnemonic> <opponent_address> <hours_duration>
                   [--bet-amount=<ba>] [--pieces=<ps>] [--max-removal=<mr>]
  algonim.py join <opponent_mnemonic>
  algonim.py play <player_mnemonic> <asa_pieces_amount>
  algonim.py status <player_address>
  algonim.py close <player_address>
  algonim.py [--help]

Commands:
  setup    Dealer sets up a new AlgoNim match.
  join     Opponent joins the match.
  play     Play your turn.
  status   Display current match status.
  close    Close expired AlgoNim Bet Escrows.

Options:
  -b <ba> --bet-amount=<ba>     Set the bet amount in microAlgos
                                [default: 0].
  -p <ps> --pieces=<ps>         Set the total amount of pieces on game table
                                [default: 21].
  -m <mr> --max-removal=<mr>    Set maximum amount of pieces removal
                                [default: 4].
  -h --help
```

### Step 1 - Match set up (Dealer)
In the first step the Dealer sets up the match, generating the ASAs + ASC1s game architecture. To set up the match the Dealer may choose the following options (or left them void for default values otherwise):
1. `[--bet-amount=<ba>]` is the bet proposal expressed in microALGO;
2. `[--pieces=<ps>]` is the number of pieces that the Dealer distributes on the Game Table;
3. `[--max-removal=<mr>]` is the maximum number of pieces that can be removed from the Game Table on each turn by the players;

**Input**
```bash
$ python3 algonim.py setup <dealer_mnemonic> NMZRQMXXYSRKVG4ZYJ5OUIN3AOLWJ2ZB5GVIGECAYM6G77D23MPA4BRP6I 2 20000000 21 4
```
**Output**
```
              _       _         
  /\/\   __ _| |_ ___| |__    _ 
 /    \ / _` | __/ __| '_ \  (_)
/ /\/\ \ (_| | || (__| | | |  _ 
\/    \/\__,_|\__\___|_| |_| (_)
                                
MATCH DURATION:		 120.0 min
PIECES ON GAME TABLE:	 21 

RULES:
1. Players on each turn must remove at least 1 ASA Piece
2. Players on each turn must remove at most 4 ASA Piece
3. Who removes the last ASA Piece form the Game Table wins the match!

Player 1 - Dealer:	SVMHAG6PLL27YYGQX4ETEIZ2GHLSO6M5ICU2MBJVKMDT2ERPNSE27OGWIE
Player 2 - Opponent:	NMZRQMXXYSRKVG4ZYJ5OUIN3AOLWJ2ZB5GVIGECAYM6G77D23MPA4BRP6I 

AlgoNim ASA Pieces ID:	 7329523
AlgoNim ASA Turn ID:	 7329527 

AlgoNim Sink Account:			      7EUFKLR636O34XW2ZRMTVOCQAXIHUDEEKIY4ZPWAGDRU6A5AONKVN5K4R4
AlgoNim Game Table Account:		      JBASDWK7MQNRCYUDZBBGR4DFHEGQTCSZQWNUMW4O2XBNON5CFLWALGKJCA
AlgoNim Bet Escrow Player 1 Account:	      PUEKG6EPXF2HMUHB3GTTODXBGUXZX26YK36SJHU7X3ZPQWSKZXUZJAZT3Q
AlgoNim Bet Escrow Player 2 Account:          W6YG5653UWDU4XTSK2767FHLQOTLXGRG53ZJGV6SEVTSMWOMJOAAMBGTX4

Send 'algonim.match' file to your opponent join the match!

May the best win!

```
The scripts generates both the `*.teal` and `*.tealc` ASC1s files and the `algonim.match` in which match's data are packed. The Dealer than sends `algonim.match` to the Opponent.

### Step 2 - Join the match (Opponent)
To join the match the Opponent must decide whether accept the Dealer bet proposal or not. Accepting the proposal the Opponet will Opt-In the match's ASAs and fund both the Bet Escrows with the same amount issuing an Atomic Transfer (already signed by the Dealer).

**Input**
```bash
$ python3 algonim.py join <opponent_mnemonic>
```
**Output**
```
      _       __                 ____  _____   _               
     / \     [  |               |_   \|_   _| (_)              
    / _ \     | |  .--./)  .--.   |   \ | |   __   _ .--..--.  
   / ___ \    | | / /'`\;/ .'`\ \ | |\ \| |  [  | [ `.-. .-. | 
 _/ /   \ \_  | | \ \._//| \__. |_| |_\   |_  | |  | | | | | | 
|____| |____|[___].',__`  '.__.'|_____|\____|[___][___||__||__]
                 ( ( __))                                      
                                                       by cusma
                                                               
  Welcome to AlgoNim, the first crypto-mini-game on Algorand!  

The Dealer wants to bet 20.0 ALGO.
Do you want to join the match? [y/N]
```
Match's ASAs Opt-In and betting AT.

### Step 3 - Play turn (Dealer or Opponent)
To play a turn the Player must own the AlgoNim ASA Turn. With `algonim.py play` players may play both a regular turn and the last turn, closing the match and claiming the rewards locked in the Bet Escrows Account.

**Input**
```bash
$ python3 algonim.py play <player_mnemonic> 4
```
**Output**
```
Removing 4 pieces from the Game table...
```
Play Turn Atomic Transfer consists of:
1. Asset Send of 1 ASA Turn to the other player;
2. Asset Send of an amount **P** (1 <= P <= M) ASA Pieces from the Game Table Account to Sink Account;

OR

Play Last Turn Atomic Transfer consists of:
1. Asset Send of 1 ASA Turn to the other player;
2. Asset Send of an amount **P** (1 <= P <= M) ASA Pieces from the Game Table Account to Sink Account;
3. Asset Send of ASA Pieces **total supply** from Sink Account to winner account;
4. Close Bet Escrow Accounts claiming the betting rewards;

### AlgoNim match's status
Each player can check the current match's status with `algonim.py status`:

**Input**
```bash
$ python3 algonim.py status NMZRQMXXYSRKVG4ZYJ5OUIN3AOLWJ2ZB5GVIGECAYM6G77D23MPA4BRP6I
```
**Output**
```
MATCH TOTAL PIECES:		21
PIECES ON THE GAME TABLE:	17
It's your turn! Play your best move!

OPPONENT BET ESCROW AMOUNT:	 20100000
YOUR BET ESCROW AMOUNT:		 20100000
Your Bet Escrow is still locked. 82 blocks left!
```
Displays ASA Pieces total amount for this match, ASA Pieces currently on the Game Table, Player's Turn and Bet Escrows status.

### Bet Escrows closing
At the end of the match **the winner can claim its own bet amount back** closing the Bet Escrow when it expires with `algonim.py close`:

**Input**
```bash
$ python3 algonim.py close NMZRQMXXYSRKVG4ZYJ5OUIN3AOLWJ2ZB5GVIGECAYM6G77D23MPA4BRP6I
```

If one of the players does not act for long time, both players can close their expired Bet Escrows claiming their own bets back.

## Open future implementations
1. Improving robustness of Bet Escrows (preventing players to stop the game in the middle simply waiting Bet Escrows expiry);
2. Freezing match’s ASAs for anyone but the players;
3. Automatically destroying match’s ASAs at the end of the game;
4. Adding ASA AlgoNim Score in the Sink from Scores Pool as reward for the winner;
5. Implementing a "Multi-heaps" variant;
6. Implementing a "Championship" mode (2 out of 3 matches).

## Troubleshooting

### Issue with `KeyError: 'microalgo_bet_amount'`

This issue arises if you do not use the latest version of `msgpack`.
`msgpack` version 1.0.0 is needed.
Run: 
```bash
$ pip3 install --upgrade msgpack
```

## Contact
For any issue, improvement proposal or comment please reach me out at: algonim.cusma@gmail.com

## Tip the Dev

If you enjoyed AlgoNim or find it useful as free and open source learning example, consider tipping the Dev:

`XODGWLOMKUPTGL3ZV53H3GZZWMCTJVQ5B2BZICFD3STSLA2LPSH6V6RW3I`
