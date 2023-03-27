# dotnet-yieldly-sdk
[![Dev CI Status](https://dev.azure.com/gbo-devops/github-pipelines/_apis/build/status/Yieldly/Yieldly%20Dev%20CI?branchName=develop)](https://dev.azure.com/gbo-devops/github-pipelines/_build/latest?definitionId=4&branchName=develop)
[![NuGet version](https://badge.fury.io/nu/yieldly.svg)](https://badge.fury.io/nu/yieldly)
[![Donate Algo](https://img.shields.io/badge/Donate-ALGO-000000.svg?style=flat)](https://algoexplorer.io/address/EJMR773OGLFAJY5L2BCZKNA5PXLDJOWJK4ED4XDYTYH57CG3JMGQGI25DQ)

# Overview
This library provides access to the [Yieldly](https://app.yieldly.finance/) No Loss Lottery and Staking contracts on the Algorand blockchain.

## Stake pools
Arbitrary stake pools are now supported. Use the `FetchStakingPoolAsync(...)` method on `YieldlyClient` to retrieve pool, this object can be used by following the same pattern as the client itself. That is, either pass the account instance to a method, which will submit signed transactions to complete an operation, or use the `Prepare...` methods to create a transaction group and handle signing the applicable transactions (see the [example](/example) directory for sample implementations).

## Roadmap
- [x] Add support for TEAL5 Staking pools
- [ ] Add example projects for staking pool operations
- [ ] Create PowerShell module and cmdlets for common operations
- [ ] Investigate Liquidity Staking pool support
- [ ] Investigate NFT prize game support

# Installation
Releases are available at [nuget.org](https://www.nuget.org/packages/Yieldly/).

## Package Manager
```
PM> Install-Package -Id Yieldly
```

## .NET CLI
```
dotnet add package Yieldly
```

# Getting Started
Other than initializing a client instance, no specific setup is required. However, if your application generates a high volume of requests it is suggested that you setup your own Algod node. See the links below for more information:
* [Algorand node on Linux/Mac](https://developer.algorand.org/docs/run-a-node/setup/install/)
* [Algorand node on Windows](https://github.com/randlabs/algorand-windows-node)

## Notes
The default client connects to an Algod node maintained by [AlgoNode.io](https://algonode.io/) (Thanks AlgoNode!). It's important that your application handle rate limiting (HTTP 429) responses by decreasing the frequency of requests. See [this guide](https://docs.microsoft.com/en-us/dotnet/architecture/microservices/implement-resilient-applications/implement-http-call-retries-exponential-backoff-polly) for a discussion on the topic.

# Usage
This section contains examples for interacting with the lottery and staking contracts. It's possible to use this SDK without passing the Account object to SDK methods, see the `Verbose` example projects in the [example](/example) directory.

TEAL5 staking pools are now supported. The `Type` property on `AsaStakingPool` indicate the pool type.

## Lottery Deposit
Deposit ALGO in the no loss lottery.

```C#
// Initialize the client
var client = new YieldlyClient();

// Deposit 10 ALGO in the no loss lottery
var amountToDeposit = Utils.AlgosToMicroalgos(10.0);

var result = await client.LotteryDepositAsync(account, amountToDeposit);
```

## Lottery Withdrawal
Withdraw ALGO participating in the no loss lottery.

```C#
// Initialize the client
var client = new YieldlyClient();

// Fetch all Yieldly amounts
var amounts = await client.FetchAmountsAsync(account.Address);

// Withdraw all ALGO currently deposited in the no loss lottery
var result = await client.LotteryWithdrawAsync(account, amounts.AlgoInLottery);
```

## Lottery Reward Claim
Claim reward from lottery participation. Note, this does not include winning the lottery, just the rewards in YLDY.

```C#
// Initialize the client
var client = new YieldlyClient();

// Fetch all Yieldly amounts
var amounts = await client.FetchAmountsAsync(account.Address);

// Claim current Yieldy rewards from lottery
var result = await client.LotteryClaimRewardAsync(account, amounts.LotteryReward.Yieldly);
```

## Staking Deposit
Deposit YLDY in the staking pool.

```C#
// Initialize the client
var client = new YieldlyClient();

// Deposit 1000 YLDY in the Yieldly staking pool
var amountToDeposit = YieldlyUtils.YieldlyToMicroyieldly(1000.0);

var result = await client.YieldlyStakingDepositAsync(account, amountToDeposit);
```

## Staking Withdrawal
Withdraw YLDY in the staking pool.

```C#
// Initialize the client
var client = new YieldlyClient();

// Fetch all Yieldly amounts
var amounts = await client.FetchAmountsAsync(account.Address);

// Withdraw all YLDY currently deposited in the Yieldly staking pool
var result = await client.YieldlyStakingWithdrawAsync(account, amounts.YieldlyStaked);
```

## Staking Reward Claim
Claim rewards from staking pool participation.

```C#
// Initialize the client
var client = new YieldlyClient();

// Fetch all Yieldly amounts
var amounts = await client.FetchAmountsAsync(account.Address);

// Withdraw all ALGO and YLDY currently available as rewards from Yieldly staking pool participation
var result = await client.YieldyStakingClaimRewardAsync(account, amounts.StakingReward);
```

# Examples
Full examples, simple and verbose, can be found in [example](/example).

# How?
This SDK was built by analyzing the transactions created by the [Yieldly](https://app.yieldly.finance/) website in [AlgoExporer](https://algoexplorer.io/). A special thanks [@JoshLmao](https://github.com/JoshLmao), his code provided a starting point for reward calculations. 

## Notes
The order of transactions in each transaction group is significant. Each transaction group, except lottery winning, has been tested.

## Special Thanks
Special thanks to [@JoshLmao](https://github.com/JoshLmao) for [yly-calc](https://github.com/JoshLmao/ydly-calc/blob/main/src/js/YLDYCalculation.js).

# Build
dotnet-yieldly-sdk build pipelines use the [Assembly Info Task](https://github.com/BMuuN/vsts-assemblyinfo-task) extension.

# License
dotnet-yieldly-sdk is licensed under a MIT license except for the exceptions listed below. See the LICENSE file for details.

## Exceptions
None.

# Disclaimer
Nothing in the repo constitutes professional and/or financial advice. Use this SDK at your own risk.