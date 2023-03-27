<p align="center"><a  href="https://github.com/cusma/algorealm"><img  width=100%  src="https://ipfs.algonode.xyz/ipfs/bafybeicqjdrwufixgun4quyble4kkvojouo3dnijuexx4wtnmt23p3dxeq"  border="0" /></a></p>

<p align="center">
    <a href="https://algorand.com"><img src="https://img.shields.io/badge/Powered by-Algorand-teal.svg" /></a>
    <img  src="https://visitor-badge.glitch.me/badge?page_id=cusma.algorealm&right_color=teal" />
    <a href="https://twitter.com/cusma_b"><img src="https://img.shields.io/badge/Created by-@cusma-teal.svg" /></a>
</p>

## Incipit

```
There was a time
When nothing but Entropy was there.
Then came the cryptographic Proof,
And took it care.

Verifiability of Randomness,
Since genesis block,
Brings Consensus over realm vastness,
So Algorand shall not fork.
```

## Become a Majesty of Algorand

Only generous hearts will rule over Algorand realm.

Show how generous is your heart donating some ALGOs to the [Rewards Pool](https://developer.algorand.org/docs/reference/algorand-networks/mainnet/#rewardspool-address) and claim the title of **Randomic Majesty of Algorand** or **Verifiable Majesty of Algorand**.

The more generous you are, the harder will be to be dethroned.

Join [AlgoRealm channel](https://t.me/algorealm)!

## Play with AlgoRealm CLI Web Emulator

Play [AlgoRealm on CLI web emulator](https://algorealm.vercel.app/console) by [@aorumbayev](https://github.com/aorumbayev).

## Play with AlgoRealm CLI


### 0. Prerequisites

-   [poetry](https://python-poetry.org/)
-   [python >= 3.10](https://www.python.org/)

### 1. Setup

```shell
$ poetry install # install dependencies
$ poetry shell # activate virtual environment
$ cd src # cd into source directory, to be replaced with UI webapp in future
```

### 2. How to play

Playing **AlgoRealm** from your CLI is pretty easy, just ask for help:

```shell
$ python3 algorealm.py -h
```

```shell
AlgoRealm, only generous heart will ever rule over Algorand. (by cusma)

Usage:
  algorealm.py poem
  algorealm.py dynasty [--test]
  algorealm.py longevity (--crown | --sceptre) [--test]
  algorealm.py braveness (--crown | --sceptre) [--test]
  algorealm.py claim-majesty (--crown | --sceptre) <majesty-name> <microalgos> [--test]
  algorealm.py claim-card
  algorealm.py buy-order <microalgos> [--notify]
  algorealm.py verify-order <seller-address>
  algorealm.py sell-card
  algorealm.py [--help]

Commands:
  poem             AlgoRealm's poem.
  dynasty          Print the glorious dynasty of AlgoRealm's Majesties.
  longevity        Print AlgoRealm's Majesties longevity.
  braveness        Print AlgoRealm's Majesties braveness.
  claim-majesty    Claim the Crown of Entropy or the Sceptre of Proof, become Majesty of Algorand.
  claim-card       Brake the spell and claim the AlgoRealm Card by AlgoWorld.
  buy-order        Place an order for the AlgoRealm Card.
  verify-order     Verify the partially signed AlgoRealm Card buy order.
  sell-card        Sell the AlgoRealm Card (paying a 10% royalty).

Options:
  -n, --notify    Notify the Seller about your buy order on-chain.
  -t, --test      TestNet mode
  -h, --help
```

⚠️ Keep your `<mnemonic>` safe! Although you will only use it on you local machine, is it strongly recommended to make use of a dedicated account just to play AlgoRealm!

> In case you want to give a try, you can play AlgoRealm on TestNet adding `-t`
> to CLI commands.

### 3. AlgoRealm Dynasty, Longevity and Braveness

Who are the Majesties of the Algorand realm?

1. Discover it directly on [Algorand blockchain](https://algoexplorer.io/application/137491307)

2. Discover it with your node:
```shell
$ ./goal app read --app-id 137491307 --global
```

3. Discover it with the AlgoRealm CLI:
```shell
$ python3 algorealm.py dynasty
```

```
                               __  __   ___   __  __
                               \*) \*)  \*/  (*/ (*/
                                \*\_\*\_|O|_/*/_/*/
                                 \_______________/
          _       __                 _______                  __
         / \     [  |               |_   __ \                [  |
        / _ \     | |  .--./)  .--.   | |__) |  .---.  ,--.   | |  _ .--..--.
       / ___ \    | | / /'`\;/ .'`\ \ |  __ /  / /__\\`'_\ :  | | [ `.-. .-. |
     _/ /   \ \_  | | \ \._//| \__. |_| |  \ \_| \__.,// | |, | |  | | | | | |
    |____| |____|[___].',__`  '.__.'|____| |___|'.__.'\'-;__/[___][___||__||__]
                     ( ( __))
                                  *** DYNASTY ***


👑 jkbishbish claimed the Crown of Entropy
on Block: 13578171 donating: 2 microALGOs to the Rewards Pool.

🪄 jkbishbish claimed the Sceptre of Proof
on Block: 13578330 donating: 2 microALGOs to the Rewards Pool.

👑 tmc claimed the Crown of Entropy
on Block: 14936018 donating: 3 microALGOs to the Rewards Pool.

🪄 tmc claimed the Sceptre of Proof
on Block: 14936235 donating: 3 microALGOs to the Rewards Pool.

👑 nullun claimed the Crown of Entropy
on Block: 14989913 donating: 4 microALGOs to the Rewards Pool.

🪄 nullun claimed the Sceptre of Proof
on Block: 14989913 donating: 4 microALGOs to the Rewards Pool.
```

4. Which was the longest lasting Majesty?
```shell
$ python3 algorealm.py longevity --crown
```

```
   *** 👑 RANDOMIC MAJESTY LONGEVITY ***

+--------------------+--------------------+
|    Majesty Name    | Longevity (blocks) |
+--------------------+--------------------+
| MillionAlgosFather |      5768768       |
|       nullun       |      3366046       |
|     jkbishbish     |      1357847       |
|        Matt        |      1248429       |
|      renangeo      |       416539       |
|        👑🅿️        |       158346       |
|        tmc         |       53895        |
| MillionAlgosFather |       32978        |
|       nullun       |        3369        |
+--------------------+--------------------+
```

5. Who is the bravest Majesty of all time?
```shell
$ python3 algorealm.py braveness --crown
```

```
*** 👑 RANDOMIC MAJESTY BRAVENESS ***

+--------------------+-----------+
|    Majesty Name    | Braveness |
+--------------------+-----------+
|      renangeo      |   7.824   |
| MillionAlgosFather |   4.605   |
|        👑🅿️        |   1.609   |
|     jkbishbish     |     1     |
|        tmc         |   0.405   |
|       nullun       |   0.288   |
|       nullun       |    0.0    |
| MillionAlgosFather |    0.0    |
|        Matt        |    0.0    |
+--------------------+-----------+
```

> Braveness is based on the relative gorwth of donation amounts (`d'`, `d`):
>
> `braveness = ln(d') - ln(d)`

### 4. Claim the Crown of Entropy or the Sceptre of Proof

Chose your `<majesty-name>` and become part of the Dynasty! Remember that to dethrone the current Majesties you must donate to the Algorand's Rewards Pool more `<microalgos>` than the last donation.

```shell
$ python3 claim-majesty (--crown | --sceptre) <majesty-name> <microalgos> [--test]
```

⚠️ Enter the the `mnemonic` formatting it as: `"word_1 word_2 word_3 ... word_25"` and keep it safe!

### 5. Claim the AlgoRealm Special Card

The [AlgoRealm Card](https://algoexplorer.io/asset/321172366) is a unique [AlgoWorld NFT](https://algoworld.io/) Special Card, securely stored in an enchanted coffer.


 <img src="https://user-images.githubusercontent.com/65770425/132135850-c4193efe-5d21-4cd6-a9bb-ae72b3d5b357.png" alt="algorealm_card" width="250" />


Only the generous heart of the [Great Majesty of Algorand](https://github.com/cusma/algorealm) will ever able to break the spell, claim the **unique Special Card** and trade it! So, you previously need to conquer both the [Crown of Entropy](https://github.com/cusma/algorealm#claim-the-crown-of-entropy) and the [Sceptre of Proof](https://github.com/cusma/algorealm#claim-the-sceptre-of-proof), ascending to [AlgoRealm's throne](https://algoexplorer.io/application/137491307).

The AlgoRealm Card can be claimed **starting from block 16,250,000** using the command `claim-card`: hold strong both the Crown and the Sceptre and keep the throne until there!

```shell
$ python3 algorealm.py claim-card [--test]
```

⚠️ Enter the the `mnemonic` formatting it as: `"word_1 word_2 word_3 ... word_25"` and keep it safe!

### 6. Place a buy-order

As a **Buyer** you can easily place a **buy-order** proposal to the **Seller** using the `buy-order` command. You just need to choose the `<microalgos>` amount for the buy order proposal.

Using the `--notify` option the **Seller** will receive a notification on-chain, being acknowledged about the new buy-order proposal.

```shell
$ python3 algorealm.py buy-order <microalgos> [--notify] [--test]
```

⚠️ Enter the the `mnemonic` formatting it as: `"word_1 word_2 word_3 ... word_25"` and keep it safe!

As result, a *Partially Signed Trade Group Transaction* is created as `trade.gtx` file in the `algorealm.py` CLI directory. Note that there is **no counter-party risk** in this operation: as a **Buyer** you can safely send the `trade.gtxn` file to the **Seller**, being sure that the trade will be executed **if and only if** the Seller will transfer the AlgoRealm Special Card to you.

### 7. Verify a buy-order

As a **Seller** you can review and verify the buy-order proposal, validating the amounts of the trade. Place the `trade.gtxn` file, received from the **Buyer**, in the same directory of your `algorealm.py` CLI.

The `verify-order` command requires your `<seller-address>` as argument.

```shell
$ python3 algorealm.py verify-order <seller-address>
```

Some compliancy checks are performed over the `trade.gtx` file before displaying the buy-order summary:

```shell
    * =========================== ORDER SUMMARY =========================== *

       BUYER:	<BUYER_ADDRESS>
       SELLER:	<SELLER_ADDRESS>
       AMOUNT:	1.0 ALGO
       ROYALTY:	0.1 ALGO

       LAST VALID BLOCK: 13184621

    * ===================================================================== *
```

If you agree with the buy-order proposal you can sell the AlgoRealm Special Card.

### 8. Sell card

As a **Seller**, if you agree with the buy-order proposal, you can sell your AlgoRealm Special Card using the command `sell-card`.

```shell
$ python3 algorealm.py sell-card [--test]
```

⚠️ Enter the the `mnemonic` formatting it as: `"word_1 word_2 word_3 ... word_25"` and keep it safe!


## Play with goal CLI

AlgoRealm could also be a good challenge to [run your own Algorand node](https://developer.algorand.org/docs/run-a-node/setup/install/) and familiarise the [goal CLI commands](https://developer.algorand.org/docs/reference/cli/goal/goal/).

<details>
  <summary>Click to expand the guidelines!</summary>

### 1. Claim the Crown of Entropy

1. Save the [AlgoRealm Law](https://github.com/cusma/algorealm/blob/main/algorealm_law.teal) into your node directory.
2. Find out who owns the [Crown of Entropy](https://algoexplorer.io/asset/137493252) (keep the `CROWN_OWNER_ADDRESS`) and Opt-In.

```bash
$ ./goal asset send -f YOUR_ADDRESS -t YOUR_ADDRESS --assetid 137493252 -a 0
```

3. Write the unsigned `crown_claim.txn` Applicarion Call transaction passing `"str:YOUR_NAME"` as `--app-arg`.

```bash
$ ./goal app call --app-id 137491307 -f YOUR_ADDRESS --app-arg "str:Crown" --app-arg "str:YOUR_NAME" -o crown_claim.txn
```

4. Write the unsigned `crown_donation.txn` Payment transaction to the Rewards Pool specifying `YOUR_DONATION` in microALGOs. The claim will be successful if `YOUR_DONATION` is grater than the current one.

```bash
$ ./goal clerk send -f YOUR_ADDRESS -t 737777777777777777777777777777777777777777777777777UFEJ2CI -a YOUR_DONATION -o crown_donation.txn
```

5. Write the unsigned `crown_transfer.txn` Asset Transfer transaction form `CROWN_OWNER_ADDRESS` to `YOUR_ADDRESS`.

```bash
$ ./goal asset send -f CROWN_OWNER_ADDRESS -t YOUR_ADDRESS --assetid 137493252 -a 1 --clawback L64GYN3IM763NDQJQD2IX35SCWQZRHWEMX55JTOUJ2PMHL6ZCMHLR4OJMU -o crown_transfer.txn
```

6. Build the unsigned Group Transaction.

```bash
$ cat crown_claim.txn crown_donation.txn crown_transfer.txn > claim.txn

$ ./goal clerk group -i claim.txn -o claim.gtxn
```

7. Split the Group Transaction and sign the single transactions (no longer valid if submitted as standalone).

```bash
$ ./goal clerk split -i claim.gtxn -o unsigned_claim.txn

$ ./goal clerk sign -i unsigned_claim-0.txn -o claim-0.stxn

$ ./goal clerk sign -i unsigned_claim-1.txn -o claim-1.stxn

$ ./goal clerk sign -i unsigned_claim-2.txn -p algorealm_law.teal -o claim-2.stxn
```

8. Submit the signed Group Transaction: claim the Crown of Entropy and became the Randomic Majesty of Algorand!

```bash
$ cat claim-0.stxn claim-1.stxn claim-2.stxn > claim.sgtxn

$ ./goal clerk rawsend -f claim.sgtxn
```

### 2. Claim the Sceptre of Proof

1. Save the [AlgoRealm Law](https://github.com/cusma/algorealm/blob/main/algorealm_law.teal) into your node directory.
2. Find out who owns the [Sceptre of Proof](https://algoexplorer.io/asset/137494385) (keep the `SCEPTRE_OWNER_ADDRESS`) and Opt-In.

```bash
$ ./goal asset send -f YOUR_ADDRESS -t YOUR_ADDRESS --assetid 137494385 -a 0
```

3. Write the unsigned `sceptre_claim.txn` Applicarion Call transaction passing `"str:YOUR_NAME"` as `--app-arg`.

```bash
$ ./goal app call --app-id 137491307 -f YOUR_ADDRESS --app-arg "str:Sceptre" --app-arg "str:YOUR_NAME" -o sceptre_claim.txn
```

4. Write the unsigned `sceptre_donation.txn` Payment transaction to the Rewards Pool specifying `YOUR_DONATION` in microALGOs. The claim will be successful if `YOUR_DONATION` is grater than the current one.

```bash
$ ./goal clerk send -f YOUR_ADDRESS -t 737777777777777777777777777777777777777777777777777UFEJ2CI -a YOUR_DONATION -o sceptre_donation.txn
```

5. Write the unsigned `sceptre_transfer.txn` Asset Transfer transaction form `SCEPTRE_OWNER_ADDRESS` to `YOUR_ADDRESS`.

```bash
$ ./goal asset send -f SCEPTRE_OWNER_ADDRESS -t YOUR_ADDRESS --assetid 137494385 -a 1 --clawback L64GYN3IM763NDQJQD2IX35SCWQZRHWEMX55JTOUJ2PMHL6ZCMHLR4OJMU -o sceptre_transfer.txn
```

6. Build the unsigned Group Transaction.

```bash
$ cat sceptre_claim.txn sceptre_donation.txn sceptre_transfer.txn > claim.txn

$ ./goal clerk group -i claim.txn -o claim.gtxn
```

7. Split the Group Transaction and sign the single transactions (no longer valid if submitted as standalone).

```bash
$ ./goal clerk split -i claim.gtxn -o unsigned_claim.txn

$ ./goal clerk sign -i unsigned_claim-0.txn -o claim-0.stxn

$ ./goal clerk sign -i unsigned_claim-1.txn -o claim-1.stxn

$ ./goal clerk sign -i unsigned_claim-2.txn -p algorealm_law.teal -o claim-2.stxn
```

8. Submit the signed Group Transaction: claim the Sceptre of Proof and became the Verifiable Majesty of Algorand!

```bash
$ cat claim-0.stxn claim-1.stxn claim-2.stxn > claim.sgtxn

$ ./goal clerk rawsend -f claim.sgtxn
```

### 3. Claim the AlgoRealm Special Card

You can also claim and trade the **AlgoRealm Special Card** using the goal CLI [following these instructions](https://github.com/cusma/algorealm/tree/main/card#readme).

</details>



## Tip the Dev

If you enjoyed AlgoRealm or find it useful as free and open source learning example, consider tipping the Dev:

`XODGWLOMKUPTGL3ZV53H3GZZWMCTJVQ5B2BZICFD3STSLA2LPSH6V6RW3I`

Here you find the [AlgoRealm slide deck](https://docs.google.com/presentation/d/1pkE_VWuq_zPOtkc8tK8MYKPzdBwUQA8r5UgACpBpmvk/edit?usp=sharing) presented at Algorand's Office Hours!

Join [AlgoRealm channel](https://t.me/algorealm)!

## ⭐️ Stargazers

Special thanks to everyone who forked or starred the repository ❤️

[![Stargazers repo roster for @AlgoWorldNFT/algoworld-contracts](https://reporoster.com/stars/dark/AlgoRealm/algorealm)](https://github.com/AlgoRealm/algorealm/stargazers)

[![Forkers repo roster for @AlgoWorldNFT/algoworld-contracts](https://reporoster.com/forks/dark/AlgoRealm/algorealm)](https://github.com/AlgoRealm/algorealm/network/members)
