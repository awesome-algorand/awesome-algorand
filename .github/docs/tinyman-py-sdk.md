# tinyman-py-sdk
Tinyman Python SDK

<p align="left">
<img src="https://visitor-badge.glitch.me/badge?page_id=tinymanorg.tinyman-py-sdk" />
<a href="https://github.com/tinymanorg/tinyman-py-sdk/actions/workflows/tests.yml"><img src="https://github.com/tinymanorg/tinyman-py-sdk/actions/workflows/tests.yml/badge.svg?branch=main" /></a>
</p>

---

## Design Goal
This SDK is designed for automated interaction with the Tinyman AMM. It will be most useful for developers who wish to create automated trading programs/bots. It may also be useful to create an alternative UI but that is not a design goal of this library.
It is designed to be reasonably low level so that pieces can be used in isolation. 

## Status
This SDK is currently under active early development and should not be considered stable.

The SDK supports Tinyman V2 and V1.1.


## Requirements
- Python 3.8+
- py-algorand-sdk 1.10.0+

## Installation
tinyman-py-sdk is not released on PYPI. It can be installed directly from this repository with pip:

`pip install git+https://github.com/tinymanorg/tinyman-py-sdk.git`


## Integration

If you are integrating your project into Tinyman, you can provide `client_name` while setting up Tinyman Client classes.
The client name will be added to the application call transaction's note field. It is recommended and completely optional.

```python
client = TinymanV2MainnetClient(..., client_name="project name", ...)
```

## V2

## Sneak Preview

```python
# examples/v2/sneak_preview.py

from examples.v2.utils import get_algod
from tinyman.v2.client import TinymanV2TestnetClient

algod = get_algod()
client = TinymanV2TestnetClient(algod_client=algod)

# Fetch our two assets of interest
USDC = client.fetch_asset(10458941)
ALGO = client.fetch_asset(0)

# Fetch the pool we will work with
pool = client.fetch_pool(USDC, ALGO)
print(f"Pool Info: {pool.info()}")

# Get a quote for a swap of 1 ALGO to USDC with 1% slippage tolerance
quote = pool.fetch_fixed_input_swap_quote(amount_in=ALGO(1_000_000), slippage=0.01)
print(quote)
print(f"USDC per ALGO: {quote.price}")
print(f"USDC per ALGO (worst case): {quote.price_with_slippage}")
```

## Tutorial

You can find a tutorial under the `examples/v2/tutorial` folder.

To run a step use `python <file_name>` such as `python 01_generate_account.py`.

#### Prerequisites
1. [Generating an account](examples/v2/tutorial/01_generate_account.py)
2. [Creating assets](examples/v2/tutorial/02_create_assets.py)

#### Steps

3. [Bootstrapping a pool](examples/v2/tutorial/03_bootstrap_pool.py)
4. [Adding initial liquidity to the pool](examples/v2/tutorial/04_add_initial_liquidity.py)
5. [Adding flexible (add two asset with a flexible rate) liquidity to the pool](examples/v2/tutorial/05_add_flexible_liquidity.py)
6. [Adding single asset (add only one asset) liquidity to the pool](examples/v2/tutorial/06_add_single_asset_liquidity.py)
7. [Removing liquidity to the pool](examples/v2/tutorial/07_remove_liquidity.py)
8. [Removing single asset(receive single asset) liquidity to the pool](examples/v2/tutorial/08_single_asset_remove_liquidity.py)
9. [Swapping fixed-input](examples/v2/tutorial/09_fixed_input_swap.py)
10. [Swapping fixed-output](examples/v2/tutorial/10_fixed_output_swap.py)

## Example Operations

<details>
<summary><strong>Bootstrap</strong></summary>

```python
txn_group = pool.prepare_bootstrap_transactions()
txn_group.sign_with_private_key(<ADDRESS>, <PRIVATE_KEY>)
txn_info = txn_group.submit(algod, wait=True)
```
</details>

<details>
<summary><strong>Add Liquidity</strong></summary>

#### Initial Add Liquidity

```python
quote = pool.fetch_initial_add_liquidity_quote(
    amount_a=<AssetAmount>,
    amount_b=<AssetAmount>,
)
txn_group = pool.prepare_add_liquidity_transactions_from_quote(quote)
txn_group.sign_with_private_key(<ADDRESS>, <PRIVATE_KEY>)
txn_info = txn_group.submit(algod, wait=True)
```

#### Flexible Add Liquidity

```python
quote = pool.fetch_flexible_add_liquidity_quote(
    amount_a=<AssetAmount>,
    amount_b=<AssetAmount>,
)
txn_group = pool.prepare_add_liquidity_transactions_from_quote(quote=quote)
txn_group.sign_with_private_key(<ADDRESS>, <PRIVATE_KEY>)
txn_info = txn_group.submit(algod, wait=True)
```

#### Single Asset Add Liquidity

```python
quote = pool.fetch_single_asset_add_liquidity_quote(amount_a=<AssetAmount>)
txn_group = pool.prepare_add_liquidity_transactions_from_quote(quote=quote)
txn_group.sign_with_private_key(<ADDRESS>, <PRIVATE_KEY>)
txn_info = txn_group.submit(algod, wait=True)
```
</details>

<details>
<summary><strong>Remove Liquidity</strong></summary>

#### Remove Liquidity

```python
quote = pool.fetch_remove_liquidity_quote(
    pool_token_asset_in=<AssetAmount>,
)
txn_group = pool.prepare_remove_liquidity_transactions_from_quote(quote=quote)
txn_group.sign_with_private_key(<ADDRESS>, <PRIVATE_KEY>)
txn_info = txn_group.submit(algod, wait=True)
```

#### Single Asset Remove Liquidity

```python
quote = pool.fetch_single_asset_remove_liquidity_quote(
    pool_token_asset_in=<AssetAmount>,
    output_asset=<Asset>,
)
txn_group = pool.prepare_remove_liquidity_transactions_from_quote(quote=quote)
txn_group.sign_with_private_key(<ADDRESS>, <PRIVATE_KEY>)
txn_info = txn_group.submit(algod, wait=True)
```

</details>

<details>
<summary><strong>Swap</strong></summary>

#### Fixed Input Swap

```python
quote = pool.fetch_fixed_input_swap_quote(amount_in=<AssetAmount>)
txn_group = pool.prepare_swap_transactions_from_quote(quote=quote)
txn_group.sign_with_private_key(<ADDRESS>, <PRIVATE_KEY>)
txn_info = txn_group.submit(algod, wait=True)
```

#### Fixed Output Swap

```python
quote = pool.fetch_fixed_output_swap_quote(amount_in=<AssetAmount>)
txn_group = pool.prepare_swap_transactions_from_quote(quote=quote)
txn_group.sign_with_private_key(<ADDRESS>, <PRIVATE_KEY>)
txn_info = txn_group.submit(algod, wait=True)
```
</details>

<details>
<summary><strong>Flash Loan</strong></summary>

1. [Flash Loan: Single Asset](examples/v2/tutorial/11_flash_loan_1_single_asset.py)
2. [Flash Loan: Multiple Assets](examples/v2/tutorial/12_flash_loan_2_multiple_assets.py)

</details>

<details>
<summary><strong>Flash Swap</strong></summary>

1. [Flash Swap: Pay in other currency](examples/v2/tutorial/13_flash_swap_1_pay_in_other_currency.py)
2. [Flash Swap: Pay in same currency](examples/v2/tutorial/14_flash_swap_2_pay_in_same_currency.py)
3. [Flash Swap: Pay in multiple currencies](examples/v2/tutorial/15_flash_swap_3_pay_in_multiple_currencies.py)

</details>

## V1.1

## Sneak Preview

```python
from tinyman.v1.client import TinymanTestnetClient
from algosdk.v2client.algod import AlgodClient


algod = AlgodClient('<TOKEN>', 'http://localhost:8080', headers={'User-Agent': 'algosdk'})
client = TinymanTestnetClient(algod_client=algod)

# Fetch our two assets of interest
TINYUSDC = client.fetch_asset(21582668)
ALGO = client.fetch_asset(0)

# Fetch the pool we will work with
pool = client.fetch_pool(TINYUSDC, ALGO)

# Get a quote for a swap of 1 ALGO to TINYUSDC with 1% slippage tolerance
quote = pool.fetch_fixed_input_swap_quote(ALGO(1_000_000), slippage=0.01)
print(quote)
print(f'TINYUSDC per ALGO: {quote.price}')
print(f'TINYUSDC per ALGO (worst case): {quote.price_with_slippage}')

# See the examples for the rest...

```

<details>
<summary><strong>Examples</strong></summary>

### Basic Swapping
[swapping1.py](examples/v1/swapping1.py)
This example demonstrates basic functionality including:
* retrieving Pool details
* getting a swap quote
* preparing swap transactions
* signing transactions
* submitting transactions
* checking excess amounts
* preparing redeem transactions

[swapping1_less_convenience.py](examples/v1/swapping1_less_convenience.py)
This example has exactly the same functionality as [swapping1.py](examples/v1/swapping1.py) but is purposely more verbose, using less convenience functions.


### Basic Pooling
[pooling1.py](examples/v1/pooling1.py)
This example demonstrates retrieving the current pool position/share for an address.

### Basic Add Liquidity (Minting)
[add_liquidity1.py](examples/v1/add_liquidity1.py)
This example demonstrates add liquidity to an existing pool.

### Basic Burning
TODO

</details>

## Conventions

* Methods starting with `fetch_` all make network requests to fetch current balances/state.
* Methods of the form `prepare_X_transactions` all return `TransactionGroup` objects (see below).
* All asset amounts are returned as `AssetAmount` objects which contain an `Asset` and `amount` (`int`).
* All asset amount inputs are expected as micro units e.g. 1 Algo = 1_000_000 micro units.

## Signing & Submission

The SDk separates transaction preparation from signing and submission to leave the developer in full control of how transactions are signed and submitted to the network.

### Preparation
The `prepare_X_transactions` methods all return a `TransactionGroup` object. This is a container object containing a list of transaction objects (`.transactions`) and a list for signed transactions (`.signed_transactions`). 

```python
transaction_group = client.prepare_app_optin_transactions(account['address'])
```


### Signing
In most cases some of the transactions have a corresponding entry in `.signed_transactions` because they have been signed by the Pool LogicSig. The remaining transactions should be signed by the 'user'.


The `TransactionGroup` includes a method to do this when signing with a private key:

```python
transaction_group.sign_with_private_key(account['address'], account['private_key'])
```

This helper method is equivalent to the following:
```python
for i, txn in enumerate(transaction_group.transactions):
    if txn.sender == account['address']:
        transaction_group.signed_transactions[i] = txn.sign(account['private_key'])
```

Any alternative method of signing can be used here following the same pattern. For example using KMD:
```python
kmd = algosdk.kmd.KMDClient(KMD_TOKEN, KMD_ADDRESS)
handle = kmd.init_wallet_handle(KMD_WALLET_ID, KMD_WALLET_PASSWORD)
for i, txn in enumerate(transaction_group.transactions):
    if txn.sender == account['address']:
        transaction_group.signed_transactions[i] = kmd.sign_transaction(handle, KMD_WALLET_PASSWORD, txn)
```

A User account LogicSig can also be used in a similar way or using the `sign_with_logicsig` convenience method:
```python
transaction_group.sign_with_logicsig(logicsig)
```

### Submission

A `TransactionGroup` containing fully signed transactions can be submitted to the network in either of two ways:

Using an Algod client:

```python
algod = AlgodClient(TOKEN, ADDRESS, headers={'User-Agent': 'algosdk'})
txid = algod.send_transactions(transaction_group.signed_transactions)
```

Or, using the convenience method of the `TinymanClient`:

```python
result = client.submit(transaction_group, wait=True)
```

This method submits the signed transactions and optionally waits for confirmation.


# License

tinyman-py-sdk is licensed under a MIT license except for the exceptions listed below. See the LICENSE file for details.

## Exceptions
`tinyman/v1/asc.json` is currently unlicensed. It may be used by this SDK but may not be used in any other way or be distributed separately without the express permission of Tinyman.
