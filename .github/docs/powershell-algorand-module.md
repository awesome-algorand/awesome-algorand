# powershell-algorand-module
[![Dev CI](https://dev.azure.com/gbo-devops/github-pipelines/_apis/build/status/Algorand.PowerShell/Algorand.PowerShell%20Dev%20CI?branchName=develop)](https://dev.azure.com/gbo-devops/github-pipelines/_build/latest?definitionId=13&branchName=develop)
[![PSGallery version](https://img.shields.io/powershellgallery/v/Algorand?include_prereleases)](https://www.powershellgallery.com/packages/Algorand)
[![Donate Algo](https://img.shields.io/badge/Donate-ALGO-000000.svg?style=flat)](https://algoexplorer.io/address/EJMR773OGLFAJY5L2BCZKNA5PXLDJOWJK4ED4XDYTYH57CG3JMGQGI25DQ)

# Overview
This PowerShell module provides tools for the Algorand blockchain.

## Roadmap
- [x] Initial implementation
- [x] Publish to module repository
- [x] Examples
- [ ] Help documentation 
- [ ] Advanced use cases

# Installation
This module is published to [PSGallery](https://www.powershellgallery.com/packages/Algorand), therefore it can be installed with the following command:

```PowerShell
PS> Install-Module -Name Algorand -Verbose
```

Note, after installing the module call `Import-Module` to load it into the current session.

# Getting Started
The module is pre-configured for Mainnet, Testnet, and Betanet. For each of the pre-configured networks, the module connects to nodes maintained by [AlgoNode.io](https://algonode.io/) (Thanks AlgoNode!). The current Algorand network configuration determines where requests are directed. The current network can be obtained by calling `Get-AlgorandNetwork` with no arguments. 

## Setting up the Account Store
This module can be configured to manage accounts. Accounts are persisted in the Account Store, which stores data in a [KeePass](https://keepass.info/) database using [pt.KeePassLibStd](https://github.com/panteam-net/pt.KeePassLibStd). To setup the Account Store, call `Initialize-AlgorandAccountStore` and enter and confirm a password. In subsequent sessions, use `Open-AlgorandAccountStore` to make the accounts accessible.

```PowerShell
PS C:\Users\admin> Initialize-AlgorandAccountStore
Set password for the new Account Store instance.
Enter password: ********
Confirm password: ********

Created account store: 'C:\Users\admin\AppData\Local\.algorand\accounts.kdbx'
```

It is not neccessary to use the Account Store to obtain an account object for signing transactions. An account object can be initialized at any time with the following command:

```PowerShell
PS C:\Users\admin> New-AlgorandAccount -Name "My Account" -Mnemonic "$ValidMnemonic"
```

## Getting the configured network
Call `Get-AlgorandNetwork` to get the current network

```PowerShell
PS C:\Users\admin> Get-AlgorandNetwork

Name    GenesisId    GenesisHash
----    ---------    -----------
testnet testnet-v1.0 SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=
```

Call `Get-AlgorandNetwork -GetAll` to get all networks
 
```PowerShell
PS C:\Users\admin> Get-AlgorandNetwork -GetAll

Name    GenesisId    GenesisHash
----    ---------    -----------
mainnet mainnet-v1.0 wGHE2Pwdvd7S12BL5FaOP20EGYesN73ktiC1qzkkit8=
testnet testnet-v1.0 SGO1GKSzyE7IEPItTxCByw9x8FmnrCDexi9/cOUJOiI=
betanet betanet-v1.0 mFgazF+2uRS1tMiL9dsj01hJGySEmPN28B/TjjvpVW0=
```

## Getting the node status
Use `Get-AlgorandNodeStatus` to get the status of the configured algod node.

```PowerShell
PS C:\Users\admin> Get-AlgorandNodeStatus

CatchupTime                 : 0
LastRound                   : 21140662
LastVersion                 : https://github.com/algorandfoundation/specs/tree/d5ac876d7ede07367dbaa26e149aa42589aac1f7
NextVersion                 : https://github.com/algorandfoundation/specs/tree/d5ac876d7ede07367dbaa26e149aa42589aac1f7
NextVersionRound            : 21140663
NextVersionSupported        : True
StoppedAtUnsupportedRound   : False
TimeSinceLastRound          : 1039953532
LastCatchpoint              :
Catchpoint                  :
CatchpointTotalAccounts     : 0
CatchpointProcessedAccounts : 0
CatchpointVerifiedAccounts  : 0
CatchpointTotalBlocks       : 0
CatchpointAcquiredBlocks    : 0
```

# Usage
## Examples
## Get $ALGO balance
```PowerShell
PS> Get-AlgorandAccount | Get-AlgorandAccountInfo | Select -ExpandProperty Amount
22001500
```

### Get ASA balance
```PowerShell
PS> Get-AlgorandAccount | Get-AlgorandAccountInfo | Select -ExpandProperty Assets

    Amount  AssetId Creator IsFrozen
    ------  ------- ------- --------
 733638011 21582668            False
 268130222 26832577            False
    588105 26835113            False
    270313 51435943            False
     48007 51437163            False
    308119 56963708            False
```

### Send a payment transaction
```PowerShell
PS> $sender = Get-AlgorandAccount
PS> $receiver = "ZZ6Z5YKFYOEINYKVID4HNJCM23OWAP5UP6IRTE4YPY27VMXPDJHMVAWUAY"
PS> $amount = 3000

PS> $tx = New-AlgorandPaymentTransaction -Sender $sender -Amount $amount -Receiver $receiver
PS> $signedTx = Sign-AlgorandTransaction -Transaction $tx -Account $sender
PS> Submit-AlgorandTransaction -Transaction $signedTx

TxId
----
4NYOHPWD5MWIMPGE4PELLI3FPKO757HJADXUJI3HM7Q3WF7TYGJA
```

## Helpful Commands

### List the available commands in the module
```PowerShell
PS> Get-Module -Name Algorand | Select -ExpandProperty ExportedCommands | Select -ExpandProperty Values | Select Name

Name
----
Add-AlgorandNetwork
Close-AlgorandAccountStore
ConvertTo-AlgorandTransaction
Find-AlgorandAccount
...
```

# Build
## Prerequisites
* .NET 6 SDK
* PowerShell 7.2

## Local
Clone this repository and execute `build-and-load-local.ps1` in a PowerShell window to build the module and import it into the current session. By default, when building locally the module is named `Algorand.Local`.

## Pipelines
powershell-algorand-module build pipelines use the [Assembly Info Task](https://github.com/BMuuN/vsts-assemblyinfo-task) extension.

# License
powershell-algorand-module is licensed under a MIT license except for the exceptions listed below. See the LICENSE file for details.

## Exceptions
None.

# Disclaimer
Nothing in the repo constitutes professional and/or financial advice. Use this module at your own risk.