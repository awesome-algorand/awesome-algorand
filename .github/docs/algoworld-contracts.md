<p align="center"><a  href="https://twitter.com/algoworld_nft/status/1450608110268211203"><img  width=100%  src="https://i.imgur.com/cGWGmxa.png"  alt="687474703a2f2f6936332e74696e797069632e636f6d2f333031336c67342e706e67"  border="0" /></a></p>

<p align="center">
    <a href="https://algorand.com"><img src="https://img.shields.io/badge/Powered by-Algorand-blue.svg" /></a>
    <a href="https://algoworld.io"><img src="https://img.shields.io/badge/AlgoWorld-Website-pink.svg" /></a>
    <a href="https://algoworldexplorer.io"><img src="https://img.shields.io/badge/AlgoWorldExplorer-Platform-red.svg" /></a>
    <a><img src="https://visitor-badge.glitch.me/badge?page_id=AlgoWorldNFT.algoworld-contracts&right_color=green" /></a>
    <a href="https://github.com/AlgoWorldNFT/algoworld-contracts/actions/workflows/ci.yaml"><img src="https://github.com/AlgoWorldNFT/algoworld-contracts/actions/workflows/ci.yaml/badge.svg" /></a>
    <a href="https://codecov.io/gh/AlgoWorldNFT/algoworld-contracts"><img src="https://codecov.io/gh/AlgoWorldNFT/algoworld-contracts/branch/main/graph/badge.svg?token=2O1VAOJCUD"  /></a>
</p>

## 📃 About

The following repository hosts the source codes for:
- `AlgoWorld Swapper`'s algorand smart signatures.
- `AlgoWorldExplorer`'s stateful smart contracts for card auctions and card trading. Modified version of [OpenNFT](https://github.com/ulamlabs/OpenNFT)'s smart contracts.

_**⚠️ NOTE: These contracts are not formally audited by accredited third parties. However, contracts are a basis for certain functionality on the AlgoWorldExplorer.io platform and were created in collaboration with Solution Architect from Algorand (credits @cusma). Code is provided under MIT license.**_

## Prerequisites

-   [poetry](https://python-poetry.org/)
-   [pre-commit](https://pre-commit.com/)
-   [Algorand Sandbox](https://github.com/algorand/sandbox)
-   [Docker](https://www.docker.com/)

## 🚀 Overview

AlgoWorld currently offers stateful contracts used for auction trading on AlgoWorldExplorer and several smart signatures used for swapping on AlgoWorld Swapper.

---

If you are looking to install algoworld contracts into your project run the following command:

```bash
pip install algoworld-contracts
```

### Example usage

```python
from algoworld_contracts import contracts

# Replace inputParams with real values
asa_to_asa_swap = contracts.get_swapper_teal(
        inputParams.creator_address,
        inputParams.offered_asa_id,
        inputParams.offered_asa_amount,
        inputParams.requested_asa_id,
        inputParams.requested_asa_amount,
        inputParams.incentive_wallet,
        inputParams.incentive_fee,
    )

# asa_to_asa_swap is a string of TEAL code
response = algod.compile(asa_to_asa_swap)
...
```

### Swapper

There are two main types of smart signatures available:

- [ASA to ASA swap | 🎴↔️🎴](algoworld_contracts/swapper/asa_to_asa_swapper.py):  Smart signature that allows performing a swap of any single ASA of specified amount to any other single ASA of specified amount.
- - [Swap Configuration Proxy 📝](algoworld_contracts/swapper/swap_proxy.py): Smart signature that powers the [AlgoWorld Swapper](https://swapper.algoworld.io) by allowing users to issue certain transactions that contain links to swap configuration files stored as `.json` files on `ipfs`. Proxy is then used to obtain those `ipfs` files by grabbing the latest pay transaction using Algorand Indexer queries.

- [ASAs to ALGO swap | 🎴🎴🎴↔️💰](algoworld_contracts/swapper/asas_to_algo_swapper.py): Smart signature that allows performing a swap of multiple ASAs of specified amount to ALGO of specified amount.

### Auction

A set of stateful smart contracts for card auctions and card trading:
- [ASAs for ALGO with trades and bidding | 🎴💰🔨](src/auction/manager.py): <br> Allows trading ASA via auctions, selling or purchasing directly.

## ⚙️ Installation

This section assumes that poetry and pre-commit are installed and executed from the root folder of this repository.

1. Clone the repo

```bash
git clone https://github.com/AlgoWorldNFT/algoworld-contracts
```

2. Install python requirements

```bash
poetry install # install all dependencies
poetry shell # activate virtual env
```

(OPTIONAL) 3. Configure `pre-commit` hooks

```bash
pre-commit install
```

If you are not going to setup `pre-commit` locally, there is a Github Actions plugin that will autoformat your branch if you are opening a PR with commits that contain un-formatted code.

## 🧪 Testing

Testing assumes that docker-compose is installed and available. Project is relying on `pytest-docker-compose` plugin that automatically boots up temporary algorand sandbox and destroys the containers after the tests are finished.

```bash
(.venv) pytest
```

You can also include `[pytest]` into your commit message to trigger the test in CI pipeline on `push` action (on pr it is triggered automatically).

## 🚧 Contribution guideline

See [`CONTRIBUTING.md`](CONTRIBUTING.md)

## ⭐️ Stargazers

Special thanks to everyone who forked or starred the repository ❤️

[![Stargazers repo roster for @AlgoWorldNFT/algoworld-contracts](https://reporoster.com/stars/dark/AlgoWorldNFT/algoworld-contracts)](https://github.com/AlgoWorldNFT/algoworld-contracts/stargazers)

[![Forkers repo roster for @AlgoWorldNFT/algoworld-contracts](https://reporoster.com/forks/dark/AlgoWorldNFT/algoworld-contracts)](https://github.com/AlgoWorldNFT/algoworld-contracts/network/members)
