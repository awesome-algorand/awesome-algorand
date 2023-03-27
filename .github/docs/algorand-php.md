<p align="center"> 
<img src="https://miro.medium.com/max/700/1*BFpFCJepifaREIg7qLSLag.jpeg">
</p>

# algorand-php
[![Packagist][packagist-shield]][packagist-url]
[![Downloads][downloads-shield]][downloads-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

Algorand is a public blockchain and protocol that aims to deliver decentralization, scale and security for all participants.
Their PURE PROOF OF STAKE™ consensus mechanism ensures full participation, protection, and speed within a truly decentralized network. With blocks finalized in seconds, Algorand’s transaction throughput is on par with large payment and financial networks. And Algorand is the first blockchain to provide immediate transaction finality. No forking. No uncertainty. 


## Introduction
Algorand-php is a community SDK with an elegant approach to connect your application to the Algorand blockchain, send transactions, create assets and query the indexer with just a few lines of code.

Once installed, you can simply connect your application to the blockchain and start sending payments

```php
$algorand->sendPayment($account, $recipient, Algo::toMicroAlgos(10), 'Hi');
```

or create a new asset:

```php
$algorand->assetManager()->createNewAsset($account, 'PHPCoin', 'PHP', 500000, 2);
```

## Features
* Algod
* Indexer
* KMD
* Transactions
* Key registration
* Authorization
* Atomic Transfers
* Account management
* Asset management
* Smart contracts
* Laravel support :heart:

## Getting started

### Installation
> **Note**: Algorand-php requires PHP 7.4+

You can install the package via composer:

```bash
composer require rootsoft/algorand-php
```

## Usage
Create an ```AlgodClient```, ```IndexerClient``` and ```KmdClient``` and pass them to the ```Algorand``` constructor.
We added extra support for locally hosted nodes & third party services (like PureStake).

```php
$algodClient = new AlgodClient(PureStake::MAINNET_ALGOD_API_URL, 'YOUR-API-KEY');
$indexerClient = new IndexerClient(PureStake::MAINNET_INDEXER_API_URL, 'YOUR-API-KEY');
$kmdClient = new KmdClient('127.0.0.1', 'YOUR-API-KEY');
$algorand = new Algorand($algodClient, $indexerClient, $kdmClient);
```

### Laravel :heart:
We've added special support to make the life of a Laravel developer even more easy!

Publish the ```algorand.php``` config file using:
```
php artisan vendor:publish --provider="Rootsoft\Algorand\AlgorandServiceProvider" --tag="config"
```

Open the ```config/algorand.php``` file in your project and insert your credentials

```php
return [
    'algod' => [
        'api_url' => 'https://testnet-algorand.api.purestake.io/ps2',
        'api_key' => 'YOUR API KEY',
        'api_token_header' => 'x-api-key',
    ],
    'indexer' => [
        'api_url' => 'https://testnet-algorand.api.purestake.io/idx2',
        'api_key' => 'YOUR API KEY',
        'api_token_header' => 'x-api-key',
    ],
    'kmd' => [
        'api_url' => '127.0.0.1',
        'api_key' => '',
        'api_token_header' => 'X-KMD-API-Token',
    ],
];
```

Now you can use the ```Algorand``` Facade!

```php
Algorand::sendPayment($account, $recipient, Algo::toMicroAlgos(10), 'Hi');
```

## Account Management
Accounts are entities on the Algorand blockchain associated with specific onchain data, like a balance. An Algorand Address is the identifier for an Algorand account.
You can use the ```AccountManager``` to perform all account related tasks.

### Creating a new account

Creating a new account is as easy as calling:
```php
$account = $algorand->accountManager()->createNewAccount();
```

With the given account, you can easily extract the public Algorand address, signing keys and seedphrase/mnemonic.
```php
$address = $account->getPublicAddress();
$seedphrase = $account->getSeedPhrase();
```

### Loading an existing account

You can load an existing account using your **generated secret key or binary seed**.

```php
$algorand->accountManager()->loadAccountFromSecret('secret key');
$algorand->accountManager()->loadAccountFromSeed(hex2bin($seed));
```

### Restoring an account

Recovering an account from your 25-word mnemonic/seedphrase can be done by passing an **array or space delimited string**

```php
$account = Algorand::accountManager()->restoreAccount($seedphrase);
```

## Transactions
There are multiple ways to create a transaction. We've included helper functions to make our life easier.

```php
$algorand->sendPayment($account, $recipient, Algo::toMicroAlgos(10), 'Hi');
```

Or you can use the ```TransactionBuilder``` to create more specific, raw transactions:

```php
// Create a new transaction
$transaction = TransactionBuilder::payment()
    ->sender($account->getAddress())
    ->note('Algonauts assemble!')
    ->amount(Algo::toMicroAlgos(1.2)) // 5 Algo
    ->receiver($recipient)
    ->useSuggestedParams(Algorand::client())
    ->suggestedFeePerByte(10)
    ->build();

// Sign the transaction
$signedTransaction = $transaction->sign($account);

// Send the transaction
$transactionId = $algorand->sendTransaction($signedTransaction);
```

## Atomic Transfer
An Atomic Transfer means that transactions that are part of the transfer either all succeed or all fail.
Atomic transfers allow complete strangers to trade assets without the need for a trusted intermediary,
all while guaranteeing that each party will receive what they agreed to.

Atomic transfers enable use cases such as:

* **Circular trades** - Alice pays Bob if and only if Bob pays Claire if and only if Claire pays Alice.
* **Group payments** - Everyone pays or no one pays.
* **Decentralized exchanges** - Trade one asset for another without going through a centralized exchange.
* **Distributed payments** - Payments to multiple recipients.

An atomic transfer can be created as following:

```php
// Create a new transaction
$transaction1 = TransactionBuilder::payment()
    ->sender($accountA->getAddress())
    ->note('Atomic transfer from account A to account B')
    ->amount(Algo::toMicroAlgos(1.2)) // 5 Algo
    ->receiver($accountB->getAddress())
    ->useSuggestedParams($algorand)
    ->build();

// Create a new transaction
$transaction2 = TransactionBuilder::payment()
    ->sender($accountB->getAddress())
    ->note('Atomic transfer from account B to account A')
    ->amount(Algo::toMicroAlgos(2)) // 5 Algo
    ->receiver($accountA->getAddress())
    ->useSuggestedParams($algorand)
    ->build();

// Combine the transactions and calculate the group id
$transactions = AtomicTransfer::group([$transaction1, $transaction2]);

// Sign the transaction
$signedTransaction1 = $transaction1->sign($accountA);
$signedTransaction2 = $transaction2->sign($accountB);

// Assemble transactions group
$signedTransactions = [$signedTransaction1, $signedTransaction2];

$algorand->sendTransactions($signedTransactions);
```

## Asset Management

**Create a new asset**

Creating a new asset is as simple as using the ```AssetManager``` included in the Algorand SDK:

```php
$algorand->assetManager()->createNewAsset($account, 'Laracoin', 'LARA', 500000, 2);
```

Or as usual, you can use the ```TransactionBuilder``` to create your asset:

```php
// Create a new asset
$transaction = TransactionBuilder::assetConfig()
    ->assetName($assetName)
    ->unitName($unitName)
    ->totalAssetsToCreate(BigInteger::of($totalAssets))
    ->decimals($decimals)
    ->defaultFrozen($defaultFrozen)
    ->managerAddress($managerAddress)
    ->reserveAddress($reserveAddress)
    ->freezeAddress($freezeAddress
    ->clawbackAddress($clawbackAddress )
    ->sender($address)
    ->suggestedParams($params)
    ->build();

// Sign the transaction
$signedTransaction = $transaction->sign($account);

// Broadcast the transaction on the network
$algorand->sendTransaction($signedTransaction);
```

**Edit an asset**

After an asset has been created only the manager, reserve, freeze and clawback accounts can be changed.
All other parameters are locked for the life of the asset.

If any of these addresses are set to "" that address will be cleared and can never be reset for the life of the asset.
Only the manager account can make configuration changes and must authorize the transaction.

```php
$algorand->assetManager()->editAsset(14192345, $account, $newAccount->getAddress());
```

**Destroy an asset**

```php
$algorand->assetManager()->destroyAsset(14192345, $account);
```

**Opt in to receive an asset**

Before being able to receive an asset, you should opt in
An opt-in transaction is simply an asset transfer with an amount of 0, both to and from the account opting in.
Assets can be transferred between accounts that have opted-in to receiving the asset.

```php
$algorand->assetManager()->optIn(14192345, $newAccount);
```

**Transfer an asset**

Transfer an asset from the account to the receiver.
Assets can be transferred between accounts that have opted-in to receiving the asset.
These are analogous to standard payment transactions but for Algorand Standard Assets.

```php
$algorand->assetManager()->transfer(14192345, $account, 1000, $newAccount->getAddress());
```

**Freeze an asset**

Freezing or unfreezing an asset requires a transaction that is signed by the freeze account.

Upon creation of an asset, you can specify a freeze address and a defaultfrozen state.
If the defaultfrozen state is set to true the corresponding freeze address must issue unfreeze transactions,
to allow trading of the asset to and from that account.
This may be useful in situations that require holders of the asset to pass certain checks prior to ownership.

```php
$algorand->assetManager()->freeze(14192345, $account, $newAccount->getAddress(), false);
```

**Revoking an asset**

Revoking an asset for an account removes a specific number of the asset from the revoke target account.
Revoking an asset from an account requires specifying an asset sender (the revoke target account) and an
asset receiver (the account to transfer the funds back to).

```php
$algorand->assetManager()->revoke(14192345, $account, 1000, $newAccount->getAddress());
```

## Stateless Smart Contracts

Most Algorand transactions are authorized by a signature from a single account or a multisignature account.
Algorand’s stateful smart contracts allow for a third type of signature using a
Transaction Execution Approval Language (TEAL) program, called a logic signature (LogicSig).
Stateless smart contracts provide two modes for TEAL logic to operate as a LogicSig,
to create a contract account that functions similar to an escrow or to delegate signature authority to another account.

### Contract Account

Contract accounts are great for setting up escrow style accounts where you want to limit withdrawals or you want to do periodic payments, etc.
To spend from a contract account, create a transaction that will evaluate to True against the TEAL logic,
then add the compiled TEAL code as its logic signature.
It is worth noting that anyone can create and submit the transaction that spends from a contract account as long as they have the compiled TEAL contract to add as a logic signature.

Sample teal file
```teal
// samplearg.teal
// This code is meant for learning purposes only
// It should not be used in production
arg_0
btoi
int 123
==
```

```php
$arguments = [BigInteger::of(123)->toBytes()];

$result = $this->algorand->applicationManager()->compileTEAL($this->sampleArgsTeal);
$lsig = LogicSignature::fromProgram($result->program(), $arguments);
$receiver = 'KTFZ5SQU3AQ6UFYI2QOWF5X5XJTAFRHACWHXAZV6CPLNKS2KSGQWPT4ACE';

$transaction = TransactionBuilder::payment()
    ->sender($lsig->toAddress())
    ->note('Contract account')
    ->amount(100000)
    ->receiver(Address::fromAlgorandAddress($receiver))
    ->useSuggestedParams($this->algorand)
    ->build();

// Sign the logic transaction
$signedTx = $lsig->signTransaction($transaction);

// Send the transaction
$pendingTx = $this->algorand->sendTransaction($signedTx, true);
```

### Account Delegation

Stateless smart contracts can also be used to delegate signatures, which means that a private key can sign a TEAL program
and the resulting output can be used as a signature in transactions on behalf of the account associated with the private key.
The owner of the delegated account can share this logic signature, allowing anyone to spend funds from his or her account according to the logic within the TEAL program.

```php
$arguments = [BigInteger::of(123)->toBytes()];

$result = $this->algorand->applicationManager()->compileTEAL($this->sampleArgsTeal);
$lsig = LogicSignature::fromProgram($result->program(), $arguments)->sign($this->account);
$receiver = 'KTFZ5SQU3AQ6UFYI2QOWF5X5XJTAFRHACWHXAZV6CPLNKS2KSGQWPT4ACE';

$transaction = TransactionBuilder::payment()
    ->sender($this->account->getAddress())
    ->note('Account delegation')
    ->amount(100000)
    ->receiver(Address::fromAlgorandAddress($receiver))
    ->useSuggestedParams($this->algorand)
    ->build();

// Sign the logic transaction
$signedTx = $lsig->signTransaction($transaction);

// Send the transaction
$pendingTx = $this->algorand->sendTransaction($signedTx, true);
```

## Stateful Smart Contracts
Stateful smart contracts are contracts that live on the chain and are used to keep track of some form of global and/or local state for the contract.
Stateful smart contracts form the backbone of applications that intend to run on the Algorand blockchain. Stateful smart contracts act similar to Algorand ASAs in that they have specific global values and per-user values.

**Create a new application**

Before creating a stateful smart contract, the code for the ApprovalProgram and the ClearStateProgram program should be written.
The creator is the account that is creating the application and this transaction is signed by this account.
The approval program and the clear state program should also be provided.
The number of global and local byte slices (byte-array value) and integers also needs to be specified.
These represent the absolute on-chain amount of space that the smart contract will use.
Once set, these values can never be changed.

When the smart contract is created the network will return a unique ApplicationID.
This ID can then be used to make ApplicationCall transactions to the smart contract.

```php
$localInts = 1;
$localBytes = 1;
$globalInts = 1;
$globalBytes = 0;

$approvalProgram = $this->algorand->applicationManager()->compileTEAL($this->approvalProgramSource);
$clearProgram = $this->algorand->applicationManager()->compileTEAL($this->clearProgramSource);

$pendingTx = $this->algorand->applicationManager()->createApplication(
    $account,
    $approvalProgram->program(),
    $clearProgram->program(),
    new StateSchema($globalInts, $globalBytes),
    new StateSchema($localInts, $localBytes),
    true,
);
```

Or you can build the raw transaction using the ```TransactionBuilder::applicationCreate```.

```php
$localInts = 1;
$localBytes = 1;
$globalInts = 1;
$globalBytes = 0;

$approvalProgram = $this->algorand->applicationManager()->compileTEAL($this->approvalProgramSource);
$clearProgram = $this->algorand->applicationManager()->compileTEAL($this->clearProgramSource);

$transaction = TransactionBuilder::applicationCreate()
    ->sender($account->getAddress())
    ->approvalProgram($approvalProgram->program())
    ->clearStateProgram($clearProgram->program())
    ->globalStateSchema(new StateSchema($globalInts, $globalBytes))
    ->localStateSchema(new StateSchema($localInts, $localBytes))
    ->useSuggestedParams($this->algorand)
    ->build();

$signedTx = $transaction->sign($account);

$pendingTx = $this->algorand->sendTransaction($signedTx, true);
```

**Opt into the Smart Contract**

Before any account, including the creator of the smart contract, can begin to make Application
Transaction calls that use local state, it must first opt into the smart contract.
This prevents accounts from being spammed with smart contracts.
To opt in, an ApplicationCall transaction of type OptIn needs to be signed and submitted by the
account desiring to opt into the smart contract.

```php
$txId = $this->algorand->applicationManager()->optIn($account, BigInteger::of(22266683));
```

Or you can build the raw transaction using the ```TransactionBuilder::applicationOptIn```.

```php
$transaction = TransactionBuilder::applicationOptIn()
    ->sender($account->getAddress())
    ->applicationId(BigInteger::of(19964146))
    ->useSuggestedParams($this->algorand)
    ->build();

$signedTx = $transaction->sign($account);

$txId = $this->algorand->sendTransaction($signedTx);
```

**Calling a Stateful Smart Contract**

Once an account has opted into a stateful smart contract it can begin to make calls to the contract.
Depending on the individual type of transaction as described in The Lifecycle of a Stateful Smart
Contract, either the ApprovalProgram or the ClearStateProgram will be called.
Generally, individual calls will supply application arguments.
See [Passing Arguments to a Smart Contract](https://developer.algorand.org/docs/features/asc1/stateful/#passing-arguments-to-stateful-smart-contracts) for details on passing arguments.

```php
$arguments = AlgorandUtils::parse_application_arguments('str:arg1,int:12');
$txId = $this->algorand->applicationManager()->call($account, BigInteger::of(22266683), $arguments);
```

Or you can build the raw transaction using ```TransactionBuilder:applicationCall```.

```php
$arguments = AlgorandUtils::parse_application_arguments('str:arg1,int:12');

$transaction = TransactionBuilder::applicationCall()
    ->sender($account->getAddress())
    ->applicationId(BigInteger::of(19964146))
    ->arguments($arguments)
    ->accounts([$account->getAddress()])
    ->foreignApps([22240890])
    ->foreignAssets([408947])
    ->useSuggestedParams($this->algorand)
    ->build();

$signedTx = $transaction->sign($account);

$txId = $this->algorand->sendTransaction($signedTx);
```

**Update a Stateful Smart Contract**

A stateful smart contract’s programs can be updated at any time.
This is done by an ApplicationCall transaction type of UpdateApplication.
This operation requires passing the new programs and specifying the application ID.
The one caveat to this operation is that global or local state requirements for the smart contract can never be updated.

```php
$approvalProgram = $this->algorand->applicationManager()->compileTEAL($this->approvalProgramSource);
$clearProgram = $this->algorand->applicationManager()->compileTEAL($this->clearProgramSource);

$txId = $this->algorand->applicationManager()->update(
    $account,
    BigInteger::of(19964146),
    $approvalProgram->program(),
    $clearProgram->program(),
);
```

Or you can build the raw transaction using ```TransactionBuilder:applicationUpdate```.

```php
$approvalProgram = $this->algorand->applicationManager()->compileTEAL($this->approvalProgramSource);
$clearProgram = $this->algorand->applicationManager()->compileTEAL($this->clearProgramSource);

$transaction = TransactionBuilder::applicationUpdate()
    ->sender($account->getAddress())
    ->applicationId(BigInteger::of(19964146))
    ->approvalProgram($approvalProgram->program())
    ->clearStateProgram($clearProgram->program())
    ->useSuggestedParams($this->algorand)
    ->build();

$signedTx = $transaction->sign($account);
$txId = $this->algorand->sendTransaction($signedTx);
```

**Delete a Stateful Smart Contract**

To delete a smart contract, an ApplicationCall transaction of type DeleteApplication must be submitted to the blockchain.
The ApprovalProgram handles this transaction type and if the call returns true the application will be deleted.

```php
$txId = $this->algorand->applicationManager()->deleteApplication($account, BigInteger::of(22257782));
```

**Close out**

The user may discontinue use of the application by sending a close out transaction. This will remove the local state for this application from the user's account

```php
$txId = $this->algorand->applicationManager()->closeOut($account, BigInteger::of(19964146));
```

**Clear state**

The user may clear the local state for an application at any time, even if the application was deleted by the creator. This method uses the same 3 parameter.

```php
$txId = $this->algorand->applicationManager()->clearState($account, BigInteger::of(19964146));
```

## Multi Signatures
Multisignature accounts are a logical representation of an ordered set of addresses with a threshold and version.
Multisignature accounts can perform the same operations as other accounts, including sending transactions and participating in consensus.
The address for a multisignature account is essentially a hash of the ordered list of accounts, the threshold and version values.
The threshold determines how many signatures are required to process any transaction from this multisignature account.

**Create a multisignature address**

```php
$one = Address::fromAlgorandAddress('XMHLMNAVJIMAW2RHJXLXKKK4G3J3U6VONNO3BTAQYVDC3MHTGDP3J5OCRU');
$two = Address::fromAlgorandAddress('HTNOX33OCQI2JCOLZ2IRM3BC2WZ6JUILSLEORBPFI6W7GU5Q4ZW6LINHLA');
$three = Address::fromAlgorandAddress('E6JSNTY4PVCY3IRZ6XEDHEO6VIHCQ5KGXCIQKFQCMB2N6HXRY4IB43VSHI');

$publicKeys = array_map(fn (Address $value) => new Ed25519PublicKey($value->address), [$one, $two, $three]);
$msigAddr = new MultiSignatureAddress(1, 2, $publicKeys);
```

**Sign a transaction with a multisignature account**

This section shows how to create, sign, and send a transaction from a multisig account.

```php
$account1 = Account::seed($seed1);
$account2 = Account::seed($seed2);
$account3 = Account::seed($seed3);

$publicKeys = array_map(fn (Account $value) => new Ed25519PublicKey($value->getPublicKey()), [$account1, $account2, $account3]);
$msigAddr = new MultiSignatureAddress(1, 2, $publicKeys);

$transaction = TransactionBuilder::payment()
    ->sender($msigAddr->toAddress())
    ->note('MSA')
    ->amount(Algo::fromMicroAlgos(1000000))
    ->receiver($account3->getAddress())
    ->useSuggestedParams($this->algorand)
    ->build();

$signedTx = $msigAddr->sign($account1, $transaction);
$completeTx = $msigAddr->append($account2, $signedTx);
$completeTx2 = $msigAddr->append($account3, $completeTx);

$txId = $this->algorand->sendTransaction($completeTx2);
```

## Key Management Daemon

The Key Management Daemon (kmd) is a low level wallet and key management tool. It works in conjunction with algod and goal to keep secrets safe.
kmd tries to ensure that secret keys never touch the disk unencrypted.

* kmd has a data directory separate from algod's data directory. By default, however, the kmd data directory is in the kmd subdirectory of algod's data directory.
* kmd starts an HTTP API server on localhost:7833 by default.
* You talk to the HTTP API by sending json-serialized request structs from the kmdapi package.

Note: If you are using a third-party API service, this process likely will not be available to you.

```php
$request = new CreateWalletRequest([
   "wallet_name" => "test1",
   "wallet_password" => "test",
   "wallet_driver_name" => "sqlite",
]);

try {
    $result = $algorand->kmd()->createWallet($request);
    print_r($result);
} catch (Exception $e) {
    echo 'Exception when calling DefaultApi->createWallet: ', $e->getMessage(), PHP_EOL;
}
```

Check out the [Algorand Developer documentation ](https://developer.algorand.org/docs/features/accounts/create/#wallet-derived-kmd) to learn more about the Key Management Daemon.

## Indexer
Algorand provides a standalone daemon algorand-indexer that reads committed blocks from the Algorand blockchain and
maintains a local database of transactions and accounts that are searchable and indexed.

The PHP SDK makes it really easy to search the ledger in a fluent api and enables application developers to perform rich and efficient queries on accounts,
transactions, assets, and so forth.

At the moment we support queries on transactions, assets and accounts.

### Transactions
Allow searching all transactions that have occurred on the blockchain.

```php
$algorand->indexer()
    ->transactions()
    ->whereCurrencyIsLessThan(Algo::toMicroAlgos(1000))
    ->whereCurrencyIsGreaterThan(Algo::toMicroAlgos(500))
    ->whereAssetId(14502)
    ->whereNotePrefix('PHP')
    ->whereTransactionType(TransactionType::PAYMENT())
    ->search();
```

### Assets
Allow searching all assets that are created on the blockchain.

```php
$algorand->indexer()
    ->assets()
    ->whereUnitName('PHP')
    ->whereAssetName('PHPCoin')
    ->whereCurrencyIsLessThan(Algo::toMicroAlgos(1000))
    ->whereCurrencyIsGreaterThan(Algo::toMicroAlgos(500))
    ->whereAssetId(14502)
    ->search();
```

### Accounts
Allow searching all accounts that are created on the blockchain.

```php
Algorand::indexer()
    ->accounts()
    ->whereAssetId(15205)
    ->whereAuthAddress('RQM43TQH4CHTOXKPLDWVH4FUZQVOWYHRXATHJSQLF7GN6CFFLC35FLNYHM')
    ->limit(5)
    ->search();
```

### Applications
Allow searching all applications on the blockchain.

```php
Algorand::indexer()
    ->applications()
    ->whereApplicationId(19964146)
    ->limit(5)
    ->search();
```

## Changelog

Please see [CHANGELOG](CHANGELOG.md) for more information on what has changed recently.

## Contributing & Pull Requests
Feel free to send pull requests.

Please see [CONTRIBUTING](.github/CONTRIBUTING.md) for details.

## Questions?
Do you have any questions, join us at the official Algorand [Discord](https://discord.com/invite/84AActu3at)!

## Credits

- [Tomas Verhelst](https://github.com/rootsoft)
- [All Contributors](../../contributors)

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[packagist-shield]: https://img.shields.io/packagist/v/rootsoft/algorand-php.svg?style=for-the-badge
[packagist-url]: https://packagist.org/packages/rootsoft/algorand-php
[downloads-shield]: https://img.shields.io/packagist/dt/rootsoft/algorand-php.svg?style=for-the-badge
[downloads-url]: https://packagist.org/packages/rootsoft/algorand-php
[issues-shield]: https://img.shields.io/github/issues/rootsoft/algorand-php.svg?style=for-the-badge
[issues-url]: https://github.com/rootsoft/algorand-php/issues
[license-shield]: https://img.shields.io/github/license/rootsoft/algorand-php.svg?style=for-the-badge
[license-url]: https://github.com/rootsoft/algorand-php/blob/master/LICENSE.txt
