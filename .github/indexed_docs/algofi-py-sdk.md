> This resource is auto indexed by AwesomeAlgo, all credits to algofi-py-sdk, for more details refer to https://github.com/Algofiorg/algofi-py-sdk

---

![algofi-py-sdk](https://user-images.githubusercontent.com/18899131/201798470-e5831f45-9e57-42de-bf0c-de26e1b1812c.jpg)

# algofi-py-sdk

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/Algofiorg/algofi-py-sdk/tree/main.svg?style=shield)](https://dl.circleci.com/status-badge/redirect/gh/Algofiorg/algofi-py-sdk/tree/main)
[![Documentation Status](https://readthedocs.org/projects/algofi-py-sdk/badge/?version=latest)](https://algofi-py-sdk.readthedocs.io/en/latest/?badge=latest)

The official Algofi V1 Python SDK. In the process of being deprecated and replaced by the [Algofi V2 Python SDK](https://github.com/Algofiorg/algofi-python-sdk).

## Documentation
https://algofi-py-sdk.readthedocs.io/en/latest/index.html

## Design Goal
This SDK is useful for developers who want to programatically interact with the Algofi lending protocol.

## Status

This SDK is currently under active early development and should not be considered stable.

## Installation
algofi-py-sdk is not yet released on PYPI. It can be installed directly from this repository with pip:

`pip install git+https://github.com/Algofiorg/algofi-py-sdk` 

To run examples:
1. create an examples/.env file
mnemonic=[25 char mnemonic]
storage_mnemonic="" (leave empty string, examples/setup.py will set)
2. Fund the account for mnemonic with 20 test ALGO
3. Run python3 examples/setup.py
4. Run examples e.g. examples/add_collateral.py

## Examples

### Add liquidity (mint)
[mint.py](https://github.com/Algofiorg/algofi-py-sdk/blob/main/examples/mint.py)

This example shows how to add liquidity to the platform

### Burn asset (burn)
[burn.py](https://github.com/Algofiorg/algofi-py-sdk/blob/main/examples/burn.py)

This example shows how to burn bank assets to redeem for underlying liquidity

### Add collateral (add_collateral)
[add_collateral.py](https://github.com/Algofiorg/algofi-py-sdk/blob/main/examples/add_collateral.py)

This example shows how to add minted bank assets to collateral

### Add liquidity to collateral (mint_to_collateral)
[mint_to_collateral.py](https://github.com/Algofiorg/algofi-py-sdk/blob/main/examples/mint_to_collateral.py)

This example shows how to add liquidity to the platform collateral

### Remove collateral (remove_collateral)
[remove_collateral.py](https://github.com/Algofiorg/algofi-py-sdk/blob/main/examples/remove_collateral.py)

This example shows how to remove bank asset collateral from platform

### Remove collateral to underlying (remove_collateral_underlying)
[remove_collateral_underlying.py](https://github.com/Algofiorg/algofi-py-sdk/blob/main/examples/remove_collateral_underlying.py)

This example shows how to remove bank asset collateral from platform to underlying asset

### Borrow (borrow)
[borrow.py](https://github.com/Algofiorg/algofi-py-sdk/blob/main/examples/borrow.py)

This example shows how to borrow an underlying asset against provided collateral

### Repay Borrow (repay_borrow)
[repay_borrow.py](https://github.com/Algofiorg/algofi-py-sdk/blob/main/examples/repay_borrow.py)

This example shows how to repay borrowed assets

### Staking (stake & unstake)
[staking.py](https://github.com/Algofiorg/algofi-py-sdk/blob/main/examples/staking.py)

This example shows how to stake and unstake in a staking contract

# License

algofi-py-sdk is licensed under a MIT license except for the exceptions listed below. See the LICENSE file for details.
