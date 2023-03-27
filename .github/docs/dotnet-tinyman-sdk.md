# dotnet-tinyman-sdk
[![Dev CI Status](https://dev.azure.com/gbo-devops/github-pipelines/_apis/build/status/Tinyman%20Dev%20CI?branchName=develop)](https://dev.azure.com/gbo-devops/github-pipelines/_build/latest?definitionId=1&branchName=develop)
[![NuGet version](https://badge.fury.io/nu/tinyman.svg)](https://badge.fury.io/nu/tinyman)
[![Donate Algo](https://img.shields.io/badge/Donate-ALGO-000000.svg?style=flat)](https://algoexplorer.io/address/EJMR773OGLFAJY5L2BCZKNA5PXLDJOWJK4ED4XDYTYH57CG3JMGQGI25DQ)

# Overview
This library provides access to the [Tinyman AMM](https://docs.tinyman.org/) on the Algorand blockchain.

## Release Notes
* v2.1.0.1
	* Addss support for re-keyed accounts
* v2.0.0.1
	* Adds support for Tinyman V2
    * Significant refactor; removes 'Action' classes 
* v1.0.0.2
	* Updates Algorand SDK to 1.0.0.15; target net6.0

## Known Issues

### High Severity
* The V1 pools should NOT be used as they are vulnerable to a liquidity draining attack.
	* See the announcement [here](https://tinymanorg.medium.com/official-announcement-about-the-incidents-of-01-01-2022-56abb19d8b19) for more information.

# Installation
Releases are available at [nuget.org](https://www.nuget.org/packages/Tinyman/).

## Package Manager
```
PM> Install-Package -Id Tinyman
```

## .NET CLI
```
dotnet add package Tinyman
```

# Getting Started
Other than initializing a client instance, no specific setup is required. However, if your application generates a high volume of requests it is suggested that you setup your own Algod node. See the links below for more information:
* [Algorand node on Linux/Mac](https://developer.algorand.org/docs/run-a-node/setup/install/)
* [Algorand node on Windows](https://github.com/randlabs/algorand-windows-node)

## Notes
Default clients connect to Algod nodes maintained by [AlgoNode.io](https://algonode.io/) (Thanks AlgoNode!). It's important that your application handle rate limiting (HTTP 429) responses by decreasing the frequency of requests. See [this guide](https://docs.microsoft.com/en-us/dotnet/architecture/microservices/implement-resilient-applications/implement-http-call-retries-exponential-backoff-polly) for a discussion on the topic.

# Usage

## Swapping
Swap one asset for another in an existing pool.

```C#
// Initialize the client
var client = new TinymanV2TestnetClient(); // or TinymanV1TestnetClient();

// Get the assets
var tinyUsdc = await client.FetchAssetAsync(21582668);
var algo = await client.FetchAssetAsync(0);

// Get the pool
var pool = await client.FetchPoolAsync(algo, tinyUsdc);

// Get a quote to swap 1 Algo for tinyUsdc
var amountIn = Algorand.Utils.Utils.AlgosToMicroalgos(1.0);
var quote = pool.CalculateFixedInputSwapQuote(new AssetAmount(algo, amountIn), 0.005);

// Perform the swap
var result = await client.SwapAsync(account, quote);
```

## Minting
Add assets to an existing pool in exchange for the liquidity pool asset.

```C#
// Initialize the client
var client = new TinymanV2TestnetClient(); // or TinymanV1TestnetClient();

// Get the assets
var tinyUsdc = await client.FetchAssetAsync(21582668);
var algo = await client.FetchAssetAsync(0);

// Get the pool
var pool = await client.FetchPoolAsync(algo, tinyUsdc);

// Get a quote to add 1 Algo and the corresponding tinyUsdc amount to the pool
var amountIn = Algorand.Utils.Utils.AlgosToMicroalgos(1.0);
var quote = pool.CalculateMintQuote(new AssetAmount(algo, amountIn), 0.005);

// Perform the minting
var result = await client.MintAsync(account, quote);
```

## Burning
Exchange the liquidity pool asset for the pool assets.

```C#
// Initialize the client
var client = new TinymanV2TestnetClient(); // or TinymanV1TestnetClient();

// Get the assets
var tinyUsdc = await client.FetchAssetAsync(21582668);
var algo = await client.FetchAssetAsync(0);

// Get the pool
var pool = await client.FetchPoolAsync(algo, tinyUsdc);

// Get a quote to swap the entire liquidity pool asset balance for pooled assets
var amount = client.GetBalance(account.Address, pool.LiquidityAsset);
var quote = pool.CalculateBurnQuote(amount, 0.005);

// Perform the burning
var result = await client.BurnAsync(account, quote);
```

## Redeeming (V1 only)
Redeem excess amounts from previous transactions.

```C#
// Initialize the client
var client = new TinymanV1TestnetClient();

// Fetch the amounts
var excessAmounts = await client.FetchExcessAmountsAsync(account.Address);

// Redeem each amount
foreach (var quote in excessAmounts) {
	var result = await client.RedeemAsync(account, quote);
}
```

# Examples
Full examples, simple and verbose, can be found in [/example](/example).

# Build
dotnet-tinyman-sdk build pipelines use the [Assembly Info Task](https://github.com/BMuuN/vsts-assemblyinfo-task) extension.

# License
dotnet-tinyman-sdk is licensed under a MIT license except for the exceptions listed below. See the LICENSE file for details.

## Exceptions
`src\Tinyman\V1\asc.json` is currently unlicensed. It may be used by this SDK but may not be used in any other way or be distributed separately without the express permission of Tinyman. It is used here with permission.

# Disclaimer
Nothing in the repo constitutes professional and/or financial advice. Use this SDK at your own risk.