# Smart-ASA

Smart ASA reference implementation combines the simplicity and security of the Algorand Standard Assets (ASA)s with the composability and programmability of Algorand Smart Contracts. The Smart ASA offers a new, powerful, L1 feature that extends regular ASAs up to the limits of your imagination!

- [Smart ASA ABI JSON](https://github.com/algorandlabs/smart-asa/blob/main/smart_asa_abi.json)
- [Smart ASA App TEAL Approval](https://github.com/algorandlabs/smart-asa/blob/main/smart_asa_approval.teal)
- [Smart ASA App TEAL Clear](https://github.com/algorandlabs/smart-asa/blob/main/smart_asa_clear.teal)
- [Smart ASA App Example](https://explorer.dappflow.org/explorer/application/107042851/transactions)

**⚠️ Disclamer: This code is not audited!**

- [Overview](#overview)
- [Reference implementation rational](#reference-implementation-rational)
  * [Underlying ASA configuration](#underlying-asa-configuration)
  * [State Schema](#state-schema)
    + [Global State](#global-state)
    + [Local State](#local-state)
    + [Self Validation](#self-validation)
    + [Smart Contract ABI's type check](#smart-contract-abi-s-type-check)
- [Smart ASA Methods](#smart-asa-methods)
  * [Smart ASA App Create](#smart-asa-app-create)
  * [Smart ASA App Opt-In](#smart-asa-app-opt-in)
  * [Smart ASA App Close-Out](#smart-asa-app-close-out)
  * [Smart ASA Creation](#smart-asa-creation)
  * [Smart ASA Configuration](#smart-asa-configuration)
  * [Smart ASA Transfer](#smart-asa-transfer)
    + [Mint](#mint)
    + [Burn](#burn)
    + [Clawback](#clawback)
    + [Transfer](#transfer)
  * [Smart ASA Global Freeze](#smart-asa-global-freeze)
  * [Smart ASA Account Freeze](#smart-asa-account-freeze)
  * [Smart ASA Destroy](#smart-asa-destroy)
  * [Smart ASA Getters](#smart-asa-getters)
- [Smart ASA CLI](#smart-asa-cli)
  * [Install](#install)
  * [Usage](#usage)
  * [Create Smart ASA NFT](#create-smart-asa-nft)
  * [Fractionalize Smart ASA NFT](#fractionalize-smart-asa-nft)
  * [Smart ASA NFT opt-in](#smart-asa-nft-opt-in)
  * [Mint Smart ASA NFT](#mint-smart-asa-nft)
  * [Smart NFT ASA global freeze](#smart-nft-asa-global-freeze)
  * [Smart NFT ASA rename](#smart-nft-asa-rename)
  * [Smart NFT ASA global unfreeze](#smart-nft-asa-global-unfreeze)
  * [Smart NFT ASA burn](#smart-nft-asa-burn)
  * [Smart ASA destroy](#smart-asa-destroy)
- [Security Considerations](#security-considerations)
  * [Prevent malicious Close-Out and Clear State](#prevent-malicious-close-out-and-clear-state)
  * [Conscious Smart ASA Destroy](#conscious-smart-asa-destroy)
- [Conclusions](#conclusions)

## Overview

The Smart ASA introduced with [ARC-0020](https://github.com/aldur/ARCs/blob/smartasa/ARCs/arc-0020.md) represents a new building block for blockchain applications. It offers a more flexible way to work with ASAs providing re-configuration functionalities and the possibility of building additional business logics around operations like asset _transfers_, _royalties_, _role-based-transfers_, _limit-amount-transfers_, _mints_, and _burns_. This reference implementation provides a basic Smart ASA contract as well as an easy to use CLI to interact with its functionalities.

It is worth noting that Smart ASA extends ASA configurability to **any field**!
With Smart ASA users can now reconfigure properties like `name`, `unit_name`, `url` and even properties like `total`, `decimals` or `default_frozen`! This makes the Smart ASA a perfect fit for "evolvable" assets, like NFTs.


## Reference implementation rational

A Smart ASA combines together a traditional ASA, called *Underlying ASA*, and an Algorand Smart Contract, called *Smart ASA App*. Essentially, the smart contract controls the ASA, implementing the  `create`, `opt-in`, `configure`, `transfer`, `global-freeze`, `freeze`, `close-out`, and `destroy` methods, plus some useful `getters`.

### Underlying ASA configuration

The `create` method triggers an `AssetConfigTx` transaction (inner transaction) that generates a new ASA, called *Underlying ASA*. The ASA is created with the following configuration:

| Property         | Value                                 |
|------------------|---------------------------------------|
| `total`          | 2^64-1                                |
| `decimals`       | 0                                     |
| `default_frozen` | True                                  |
| `unit_name`      | S-ASA                                 |
| `asset_name`     | SMART-ASA                             |
| `url`            | smart-asa-app-id:\<Smart ASA App ID\> |
| `manager_addr`   | \<Smart ASA App Addr\>                |
| `reserve_addr`   | \<Smart ASA App Addr\>                |
| `freeze_addr`    | \<Smart ASA App Addr\>                |
| `clawback_name`  | \<Smart ASA App Addr\>                |

The ASA is set with maximum supply as (`total` = max `uint64`), it is not divisible, and it is frozen by default. The unit and asset names are standard strings that identify a Smart ASA.

The `url` field is used to bind the Underlying ASA with the Smart ASA App ID who controls it, with the following encoding:

`smart-asa-app-id:<App ID>`

Finally, the `manager`, `reserve`, `freeze`, and `clawback` roles are assigned to the *Smart ASA App* address.

> **The Underlying ASA can only be controlled by the smart contract**.

### State Schema

The `StateSchema` of the Smart Contract has been designed to match 1-to-1 the parameters of an ASA. This reference implementation also requires users to initialize their `LocalState` by opting-in into the application.

#### Global State

The `GlobalState` of the Smart ASA App is defined as follows:

Integer Variables:

- `total`: total supply of a Smart ASA. This value cannot be greater than the *Underlying ASA* total supply or lower than the current cirulating supply (in case of reconfiguration);
- `decimals`: number of digits to use after the decimal point. If 0, the Smart ASA is not divisible. If 1, the base unit of the Smart ASA is in tenth, it 2 it is in hundreds, if 3 it is in thousands, and so on;
- `default_frozen`: True to freeze Smart ASA holdings by default;
- `smart_asa_id`: asset ID of the *Underlying ASA*;
- `frozen`: True to globally freeze Smart ASA transfers for all holders.

Bytes Variables:

- `unit_name`: name of a unit of the Smart ASA;
- `name`: name of the Smart ASA;
- `url`: URL with additional information on the Smart ASA;
- `metadata_hash`: Smart ASA metadata hash;
- `manager_addr`: Address of the account entitle to manage the configuration of the Smart ASA and destroy it;
- `reserve_addr`: Address of the account entitled to mint and burn the Smart ASA;
- `freeze_addr`: Address of the account entitled to freeze holdings or even globally freeze the Smart ASA;
- `clawback_addr`: Address of the account that can clawback holdings of the Smart ASA.

**The *Smart ASA App* of this reference implementation has been designed to control one ASA at a time. However the same app could be re-used for several Smart ASAs**. For this reason, the `smart_asa_id` variable has been added to the `GlobalState` to monitor the ID of the current *Underlying ASA* controlled by the application. This value is also stored into the local state of opted-in users, enforcing cross-checks between local and global states. This also avoids issues like unauthorized transfers (see [Security Considerations](https://github.com/algorandlabs/smart-asa#security-considerations) for more details).

Bonus feature: This reference implementation also includes the Smart ASA global `frozen` variable. It can only be updated by the freeze address which has the authority of globally freezing the asset with a single action, rather than freezing accounts one by one.

Finally, a new functional authority has been assigned to the `reserve` address of the Smart ASA. It is now the (_only_) entity in charge of `minting` and `burning` Smart ASAs (see the [Smart ASA Transfer](https://github.com/algorandlabs/smart-asa#smart-asa-transfer) interface for more details).

#### Local State

The opted-in users `LocalState` is defined as follows:

Integer Variables:

- `smart_asa_id`: asset ID of the *Underlying ASA* of the Smart ASA a user has opted-in;
- `frozen`: True to freeze the holdings of the account.

#### Self Validation

The Smart ASA reference implementation enforces self validation of the `StateSchema`. On creation, it controls the size of the given schema for both the global and local states. The expected values are:

|           | Global | Local |
|-----------|--------|-------|
| **Ints**  | 5      | 2     |
| **Bytes** | 8      | 0     |

#### Smart Contract ABI interface

Smart Contract methods has been implemented to comply with the [Algorand ABI](https://developer.algorand.org/docs/get-details/dapps/smart-contracts/ABI/) interface. The whole ABI interface of the Smart ASA reference implementation can be found in `smart_asa_abi.json`.

The validation checks on the ABI types are carried on the client side. The Smart Contract enforces the following on-chain checks:

- `address` length must be equal to 32 bytes;
- `Bool` values must be equal to 0 or 1.

## Smart ASA Methods

Smart ASA reference implementation follows the ABI specified by ARC-20 to
ensure full composability and interoperability with the rest of
Algorand's ecosystem (e.g. wallets, chain explorers, external dApp, etc.).

The implementation of the ABI relies on the new PyTeal ABI Router component, which
automatically generates ABI JSON by using simple Python _decorators_ for Smart
Contract methods. PyTeal ABI Router takes care of ABI types and methods'
signatures encoding as well.

### Smart ASA App Create

_Smart ASA Create_ is a `BareCall` (no argument needed) that instantiate the Smart
ASA App, verifying the consistency of the `SateSchema` assigned to the create
Application Call. This method initializes the whole Global State to default
upon creation.

### Smart ASA App Opt-In

_Smart ASA Opt-In_ represents the account opt-in to the Smart ASA. The argument `asset` represents the *Underlying ASA*. This method initializes the `LocalState` of the user. If the Smart ASA is `default_frozen` then the opting-in users are `frozen` too.

```json
{
    "name": "asset_app_optin",
    "args": [
        {
            "type": "asset",
            "name": "asset",
            "desc": "Underlying ASA ID (ref. App Global State: \"smart_asa_id\")."
        },
        {
            "type": "axfer",
            "name": "underlying_asa_optin",
            "desc": "Underlying ASA opt-in transaction."
        }
    ],
    "returns": {
        "type": "void"
    },
    "desc": "Smart ASA atomic opt-in to Smart ASA App and Underlying ASA."
}
```

### Smart ASA App Close-Out

_Smart ASA Close-Out_ closes out an account from the Smart ASA. It shadows the exact behavior of a traditional ASA. In particular, The argument `close_asset` represents the _Underlying ASA_ to be closed, whereas the `close_to` is the account to which all the remainder balance is sent on closing. This method removes the *Smart ASA App* `LocalState` from the calling account as well as closing out the _Underlying ASA_. The Smart ASA closing procedure proceeds as follows:

1. If the _Underlying ASA_ has been destroyed, then no checks is performed on `close_to` account;
2. If the user account is _frozen_ or the whole _Underlying ASA_ is _frozen_, then the `close_to` MUST be the Smart ASA Creator (*Smart ASA App*);
3. If the `close_to` account is not the Smart ASA Creator, then it MUST have opted-in to the Smart ASA.

```json
{
    "name": "asset_app_closeout",
    "args": [
        {
            "type": "asset",
            "name": "close_asset",
            "desc": "Underlying ASA ID (ref. App Global State: \"smart_asa_id\")."
        },
        {
            "type": "account",
            "name": "close_to",
            "desc": "Account to send all Smart ASA reminder to. If the asset/account is forzen then this must be set to Smart ASA Creator."
        }
    ],
    "returns": {
        "type": "void"
    },
    "desc": "Smart ASA atomic close-out of Smart ASA App and Underlying ASA."
}
```

### Smart ASA Creation

_Smart ASA Create_ is the creation method of a Smart ASA. It creates a new _Underlying ASA_ and parametrises the controlling Application with the given properties.

```json
{
    "name": "asset_create",
    "args": [
        {
            "type": "uint64",
            "name": "total",
            "desc": "The total number of base units of the Smart ASA to create."
        },
        {
            "type": "uint32",
            "name": "decimals",
            "desc": "The number of digits to use after the decimal point when displaying the Smart ASA. If 0, the Smart ASA is not divisible."
        },
        {
            "type": "bool",
            "name": "default_frozen",
            "desc": "Smart ASA default frozen status (True to freeze holdings by default)."
        },
        {
            "type": "string",
            "name": "unit_name",
            "desc": "The name of a unit of Smart ASA."
        },
        {
            "type": "string",
            "name": "name",
            "desc": "The name of the Smart ASA."
        },
        {
            "type": "string",
            "name": "url",
            "desc": "Smart ASA external URL."
        },
        {
            "type": "byte[]",
            "name": "metadata_hash",
            "desc": "Smart ASA metadata hash (suggested 32 bytes hash)."
        },
        {
            "type": "address",
            "name": "manager_addr",
            "desc": "The address of the account that can manage the configuration of the Smart ASA and destroy it."
        },
        {
            "type": "address",
            "name": "reserve_addr",
            "desc": "The address of the account that holds the reserve (non-minted) units of the asset and can mint or burn units of Smart ASA."
        },
        {
            "type": "address",
            "name": "freeze_addr",
            "desc": "The address of the account that can freeze/unfreeze holdings of this Smart ASA globally or locally (specific accounts). If empty, freezing is not permitted."
        },
        {
            "type": "address",
            "name": "clawback_addr",
            "desc": "The address of the account that can clawback holdings of this asset. If empty, clawback is not permitted."
        }
    ],
    "returns": {
        "type": "uint64",
        "desc": "New Smart ASA ID."
    },
    "desc": "Create a Smart ASA (triggers inner creation of an Underlying ASA)."
}
```

### Smart ASA Configuration

_Smart ASA Configuration_ is the update method of a Smart ASA. It updates the
parameters of an existing Smart ASA. Only the `manager` has the authority to
reconfigure the asset by invoking this method.

> The ABI method needs all Smart ASA fields, even those one not to be changed, by assigning the current value to the unchanged fields. The Smart ASA Client of this reference implementation abstracts this complexity taking care of unspecified fields by replicating current Smart ASA state for the unchanged fields as default.

The following restrictions apply in this Smart ASA reference implementation:

- `manager_addr`, `reserve_addr`, `freeze_addr` and `clawback_addr` addresses can no longer be configured once set to `ZERO_ADDRESS`;
- `total` cannot be configured to a value lower than the current circulating supply.

```json
{
    "name": "asset_config",
    "args": [
        {
            "type": "asset",
            "name": "config_asset"
        },
        {
            "type": "uint64",
            "name": "total",
            "desc": "The total number of base units of the Smart ASA to create. It can not be configured to less than its current circulating supply."
        },
        {
            "type": "uint32",
            "name": "decimals",
            "desc": "The number of digits to use after the decimal point when displaying the Smart ASA. If 0, the Smart ASA is not divisible."
        },
        {
            "type": "bool",
            "name": "default_frozen",
            "desc": "Smart ASA default frozen status (True to freeze holdings by default)."
        },
        {
            "type": "string",
            "name": "unit_name",
            "desc": "The name of a unit of Smart ASA."
        },
        {
            "type": "string",
            "name": "name",
            "desc": "The name of the Smart ASA."
        },
        {
            "type": "string",
            "name": "url",
            "desc": "Smart ASA external URL."
        },
        {
            "type": "byte[]",
            "name": "metadata_hash",
            "desc": "Smart ASA metadata hash (suggested 32 bytes hash)."
        },
        {
            "type": "address",
            "name": "manager_addr",
            "desc": "The address of the account that can manage the configuration of the Smart ASA and destroy it."
        },
        {
            "type": "address",
            "name": "reserve_addr",
            "desc": "The address of the account that holds the reserve (non-minted) units of the asset and can mint or burn units of Smart ASA."
        },
        {
            "type": "address",
            "name": "freeze_addr",
            "desc": "The address of the account that can freeze/unfreeze holdings of this Smart ASA globally or locally (specific accounts). If empty, freezing is not permitted."
        },
        {
            "type": "address",
            "name": "clawback_addr",
            "desc": "The address of the account that can clawback holdings of this asset. If empty, clawback is not permitted."
        }
    ],
    "returns": {
        "type": "void"
    },
    "desc": "Configure the Smart ASA. Use existing values for unchanged parameters. Setting Smart ASA roles to zero-address is irreversible."
}
```

### Smart ASA Transfer

_Smart ASA Transfer_ is the asset transfer method of a Smart ASA. It defines the transfer of an asset between an `asset_sender` and `asset_receiver` specifying the `asset_amount` to be transferred. This method automatically distinguishes four types of transfer, such as `mint`, `burn`, `clawback`, and regular `transfer`.

```json
{
    "name": "asset_transfer",
    "args": [
        {
            "type": "asset",
            "name": "xfer_asset",
            "desc": "Smart ASA ID to transfer."
        },
        {
            "type": "uint64",
            "name": "asset_amount",
            "desc": "Smart ASA amount to transfer."
        },
        {
            "type": "account",
            "name": "asset_sender",
            "desc": "Smart ASA sender, for regular transfer this must be equal to the Smart ASA App caller."
        },
        {
            "type": "account",
            "name": "asset_receiver",
            "desc": "The recipient of the Smart ASA transfer."
        }
    ],
    "returns": {
        "type": "void"
    },
    "desc": "Smart ASA transfers: regular, clawback (Clawback Address), mint or burn (Reserve Address)."
}
```

#### Mint

In the reference implementation only the `reserve` address can _mint_ a Smart ASA. A minting succeeds if the following conditions are met:

- the Smart ASA is not globally `frozen`;
- `asset_sender` is the *Smart ASA App*;
- `asset_receiver` is not `frozen`;
- `asset_receiver` Smart ASA ID in Local State is up-to-date;
- `asset_amount` does not exceed the outstanding available supply of the Smart ASA.

> Reference implementation checks that `smart_asa_id` is _up-to-date_ in Local
> State since the Smart ASA App could create a new Underlying ASA (if the
> previous one has been dystroied by the Manager Address). This requires users
> to opt-in again and initialize accordingly a coherent `frozen` status for the
> new Smart ASA (which could potentially have been created as `default_frozen`).

#### Burn

In the reference implementation only the `reserve` address can burn a Smart ASA. A burning succeeds if the following conditions are met:

- the Smart ASA is not globally `frozen`;
- `asset_sender` is the `reserve` address;
- `asset_sender` is not `frozen`;
- `asset_sender` Smart ASA ID in Local State is up-to-date;
- `asset_receiver` is the *Smart ASA App*.

#### Clawback

The `clawback` address of a Smart ASA can invoke a clawback transfer from and to any asset holder (or revoke an asset). A clawback succeeds if the following conditions are met:

- `asset_sender` Smart ASA ID in Local State is up-to-date;
- `asset_receiver` Smart ASA ID in Local State is up-to-date;.

Checking that Smart ASA ID in Local State is up-to-date both for `asset_sender` and `asset_receiver` implicitly verifies that both users are opted-in to the *Smart ASA App*. This ensures that _minting_ and _burning_ can not be executed as _clawback_, since the *Smart ASA App* can not opt-in to itself.

#### Transfer

A regular transfer of a Smart ASA can be invoked by any opted-in asset holder. It succeeds if the following conditions are met:

- the Smart ASA is not globally `frozen`;
- `asset_sender` is not `frozen`;
- `asset_sender` Smart ASA ID in Local State is up-to-date;
- `asset_receiver` is not `frozen`;
- `asset_receiver` Smart ASA ID in Local State is up-to-date.

### Smart ASA Global Freeze

_Smart ASA Global Freeze_ is the freeze method of a Smart ASA. It enables the `freeze` address to globally freeze a Smart ASA. A frozen Smart ASA cannot be transferred, minted or burned.

```json
{
    "name": "asset_freeze",
    "args": [
        {
            "type": "asset",
            "name": "freeze_asset",
            "desc": "Smart ASA ID to freeze/unfreeze."
        },
        {
            "type": "bool",
            "name": "asset_frozen",
            "desc": "Smart ASA ID forzen status."
        }
    ],
    "returns": {
        "type": "void"
    },
    "desc": "Smart ASA global freeze (all accounts), called by the Freeze Address."
}
```

### Smart ASA Account Freeze

_Smart ASA Account Freeze_ is the account freeze method of a Smart ASA. It enables the `freeze` address to freeze a Smart ASA holder. Freezed accounts cannot receive nor send the asset.

```json
{
    "name": "account_freeze",
    "args": [
        {
            "type": "asset",
            "name": "freeze_asset",
            "desc": "Smart ASA ID to freeze/unfreeze."
        },
        {
            "type": "account",
            "name": "freeze_account",
            "desc": "Account to freeze/unfreeze."
        },
        {
            "type": "bool",
            "name": "asset_frozen",
            "desc": "Smart ASA ID forzen status."
        }
    ],
    "returns": {
        "type": "void"
    },
    "desc": "Smart ASA local freeze (account specific), called by the Freeze Address."
}
```

### Smart ASA Destroy

_Smart ASA Destroy_ is the destroy method of a Smart ASA. In this reference implementation only the `manager` can invoke the Smart ASA destroy. This method clears the `GlobalState` schema of a Smart ASA, destroying any previous configuration.

> A Smart ASA can be destroyed if and only if the `circulating supply = 0`. After a Smart ASA destroy, users remain opted-in to the *Smart ASA App*, but with an outdated `smart_asa_id` in their local state. The section [Security Considerations](https://github.com/algorandlabs/smart-asa#security-considerations) discusses the side effects of a Smart ASA destroy.

```json
{
    "name": "asset_destroy",
    "args": [
        {
            "type": "asset",
            "name": "destroy_asset",
            "desc": "Underlying ASA ID (ref. App Global State: \"smart_asa_id\")."
        }
    ],
    "returns": {
        "type": "void"
    },
    "desc": "Destroy the Underlying ASA, must be called by Manager Address."
}
```

### Smart ASA Getters

_Getter_ methods expose relevant information of a Smart ASA. To retrieve the whole configuration you can query the ABI method `get_asset_config` which returns a Tuple with all the configuration parameters!

The reference implementation also exposes the following getters:

- `get_asset_is_frozen`: which returns `True` if the Smart ASA is globally frozen;
- `get_account_is_frozen`: which returns `True` if a given account is frozen;
- `get_circulating_supply`: which returns the current circulating supply of a smart ASA;
- `get_optin_min_balance`: which returns the minimum balance (in ALGO) required to opt-in the Smart ASA.

Getters ABI interface example:


```json
{
  "name": "get_<param>",
  "args": [
    {"name": "asset", "type": "asset"}
  ],
  "returns": {"type": "<Tuple | uint64>"}
}
```

## Smart ASA CLI
The Smart ASA CLI has been conceived to offer the community a comprehensive and intuitive tool to interact with all the functionalities of the Smart ASA of this reference implementation. The CLI, as-is, is intended for testing purposes and can only be used within an Algorand Sandbox environment.

### Install

**CLI Requirement: Algorand Sandbox** (try it with `dev` mode first!)

The `Pipfile` contains all the dependencies to install the Smart ASA CLI using
`pipenv` entering:

```shell
pipenv install
```

### Usage
The Smart ASA CLI plays the same role as `goal asset` to facilitate a seamless
understanding of this new "smarter" ASA.

The CLI has been built with `docopt`, which provides an intuitive and standard
command line usage:

- `<...>` identify mandatory positional arguments;
- `[...]` identify optional arguments;
- `(...|...)` identify mandatory mutually exclusive arguments;
- `[...|...]` identify optional mutually exclusive arguments;
- `--arguments` could be followed by a `<value>` (if required) or not;

All the `<account>`s (e.g. `<creator>`, `<manager>`, etc.) must be addresses of
a wallet account managed by `sandbox`'s KMD.

Using the command line you can perform all the actions over a Smart ASA, just
like an ASA!

```shell
Smart ASA (ARC-20 reference implementation)

Usage:
  smart_asa create  <creator> <total> [--decimals=<d>] [--default-frozen=<z>]
                    [--name=<n>] [--unit-name=<u>] [--metadata-hash=<s>]
                    [--url=<l>] [--manager=<m>] [--reserve=<r>]
                    [--freeze=<f>] [--clawback=<c>]
  smart_asa config  <asset-id> <manager> [--new-total=<t>] [--new-decimals=<d>]
                    [--new-default-frozen=<z>] [--new-name=<n>]
                    [--new-unit-name=<u>] [--new-metadata-hash=<s>]
                    [--new-url=<u>] [--new-manager=<m>] [--new-reserve=<r>]
                    [--new-freeze=<f>] [--new-clawback=<c>]
  smart_asa destroy <asset-id> <manager>
  smart_asa freeze  <asset-id> <freeze> (--asset | --account=<a>) <status>
  smart_asa optin   <asset-id> <account>
  smart_asa optout  <asset-id> <account> <close-to>
  smart_asa send    <asset-id> <from> <to> <amount>
                    [--reserve=<r> | --clawback=<c>]
  smart_asa info    <asset-id> [--account=<a>]
  smart_asa get     <asset-id> <caller> <getter> [--account=<a>]
  smart_asa         [--help]

Commands:
  create     Create a Smart ASA
  config     Configure a Smart ASA
  destroy    Destroy a Smart ASA
  freeze     Freeze whole Smart ASA or specific account, <status> = 1 is forzen
  optin      Optin Smart ASAs
  optout     Optout Smart ASAs
  send       Transfer Smart ASAs
  info       Look up current parameters for Smart ASA or specific account
  get        Look up a parameter for Smart ASA

Options:
  -h, --help
  -d, --decimals=<d>           [default: 0]
  -z, --default-frozen=<z>     [default: 0]
  -n, --name=<n>               [default: ]
  -u, --unit-name=<u>          [default: ]
  -l, --url=<l>                [default: ]
  -s, --metadata-hash=<s>      [default: ]
  -m, --manager=<m>            Default to Smart ASA Creator
  -r, --reserve=<r>            Default to Smart ASA Creator
  -f, --freeze=<f>             Default to Smart ASA Creator
  -c, --clawback=<c>           Default to Smart ASA Creator
```

### Create Smart ASA NFT
Let's create a beautiful 🔴 Smart ASA NFT (non-fractional for the moment)...

```shell
python3 smart_asa_cli.py create KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ 1 --name Red --unit-name 🔴

 --- Creating Smart ASA App...
 --- Smart ASA App ID: 2988

 --- Funding Smart ASA App with 1 ALGO...

 --- Creating Smart ASA...
 --- Created Smart ASA with ID: 2991
```

The Smart ASA is created directly by the Smart ASA App, so upon creation the
whole supply is stored in Smart ASA App account. A *minting* action is required
to put units of Smart ASA in circulation (see
[Mint Smart ASA NFT](./README.md#mint-smart-asa-nft)).

```shell
python3 smart_asa_cli.py info 2991

        Asset ID:         2991
        App ID:           2988
        App Address:      T6QBA5AXSJMBG55Y2BVDR6MN5KTXHHLU7LWDY3LGZNAPGIKDOWMP4GF5PU
        Creator:          KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Asset name:       Red

        Unit name:        🔴

        Maximum issue:    1 🔴
        Issued:           0 🔴
        Decimals:         0
        Global frozen:    False
        Default frozen:   False
        Manager address:  KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Reserve address:  KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Freeze address:   KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Clawback address: KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
```

### Fractionalize Smart ASA NFT
One of the amazing new feature of Smart ASAs is that they are **completely**
re-configurable after creation! Exactly: you can even reconfigure their
`total` or their `decimals`!

So let's use this new cool feature to **fractionalize** the Smart ASA NFT after
its creation by setting the new `<total>` to 100 and `<decimals>` to 2!

```shell
python3 smart_asa_cli.py config 2991 KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ --new-total 100 --new-decimals 2

 --- Configuring Smart ASA 2991...
 --- Smart ASA 2991 configured!
```

```shell
python3 smart_asa_cli.py info 2991

        Asset ID:         2991
        App ID:           2988
        App Address:      T6QBA5AXSJMBG55Y2BVDR6MN5KTXHHLU7LWDY3LGZNAPGIKDOWMP4GF5PU
        Creator:          KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Asset name:       Red

        Unit name:        🔴

        Maximum issue:    100 🔴 <-- 😱
        Issued:           0 🔴
        Decimals:         2      <-- 😱
        Global frozen:    False
        Default frozen:   False
        Manager address:  KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Reserve address:  KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Freeze address:   KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Clawback address: KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
```

### Smart ASA NFT opt-in
We can now opt-in the Smart ASA using the `optin` command that manages both the
undelying ASA opt-in and the Smart ASA App opt-in under the hood.

> Note that opt-in to Smart ASA App is required only if the Smart ASA need
> local state (e.g. *account frozen*).

```shell
python3 smart_asa_cli.py optin 2991 KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ

 --- Opt-in Smart ASA 2991...

 --- Smart ASA 2991 state:
{'frozen': 0, 'smart_asa_id': 2991}
```

### Mint Smart ASA NFT

Only Smart ASA Reserve Address can mint units of Smart ASA from the Smart ASA
App, with the following restrictions:

- Smart ASA can not be *over minted* (putting in circulation more units than
`total`);
- Smart ASA can not be minted if the *asset is global frozen*;
- Smart ASA can not be minted if the minting receiver *account is frozen*;

```shell
python3 smart_asa_cli.py send 2991 T6QBA5AXSJMBG55Y2BVDR6MN5KTXHHLU7LWDY3LGZNAPGIKDOWMP4GF5PU
KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ 100
--reserve KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ

 --- Minting 100 units of Smart ASA 2991
 from T6QBA5AXSJMBG55Y2BVDR6MN5KTXHHLU7LWDY3LGZNAPGIKDOWMP4GF5PU
 to KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ...
 --- Confirmed!
```

```shell
python3 smart_asa_cli.py info 2991

        Asset ID:         2991
        App ID:           2988
        App Address:      T6QBA5AXSJMBG55Y2BVDR6MN5KTXHHLU7LWDY3LGZNAPGIKDOWMP4GF5PU
        Creator:          KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Asset name:       Red

        Unit name:        🔴

        Maximum issue:    100 🔴
        Issued:           100 🔴 <-- 👀
        Decimals:         2
        Global frozen:    False
        Default frozen:   False
        Manager address:  KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Reserve address:  KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Freeze address:   KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Clawback address: KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
```

### Smart NFT ASA global freeze
Differently from regular ASA, Smart ASA can now be *globally frozen* by Freeze
Account, meaning that the whole Smart ASA in atomically frozen regardless the
particular *frozen state* of each account (which continues to be managed in
the same way as regular ASA).

Let's freeze the whole Smart ASA before starting administrative operations on
it:

```shell
python3 smart_asa_cli.py freeze 2991 KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ --asset 1

 --- Freezing Smart ASA 2991...
```

```shell
python3 smart_asa_cli.py info 2991

        Asset ID:         2991
        App ID:           2988
        App Address:      T6QBA5AXSJMBG55Y2BVDR6MN5KTXHHLU7LWDY3LGZNAPGIKDOWMP4GF5PU
        Creator:          KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Asset name:       Red

        Unit name:        🔴

        Maximum issue:    100 🔴
        Issued:           100 🔴
        Decimals:         2
        Global frozen:    True   <-- 😱
        Default frozen:   False
        Manager address:  KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Reserve address:  KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Freeze address:   KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Clawback address: KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
```

### Smart NFT ASA rename
Now that the whole Smart ASA is globally frozen, let's take advantage again of
Smart ASA full reconfigurability to change its `--name` and `--unit-name`!

```shell
python3 smart_asa_cli.py config 2991 KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ --new-name Blue --new-unit-name 🔵

 --- Configuring Smart ASA 2991...
 --- Smart ASA 2991 configured!
```

```shell
python3 smart_asa_cli.py info 2991

        Asset ID:         2991
        App ID:           2988
        App Address:      T6QBA5AXSJMBG55Y2BVDR6MN5KTXHHLU7LWDY3LGZNAPGIKDOWMP4GF5PU
        Creator:          KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Asset name:       Blue   <-- 😱

        Unit name:        🔵     <-- 😱

        Maximum issue:    100 🔵
        Issued:           100 🔵
        Decimals:         2
        Global frozen:    True
        Default frozen:   False
        Manager address:  KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Reserve address:  KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Freeze address:   KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Clawback address: KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
```

### Smart NFT ASA global unfreeze
The Smart ASA is all set! Let's *unfreeze* it globally!

```shell
python3 smart_asa_cli.py freeze 2991 KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ --asset 0

 --- Unfreezing Smart ASA 2991...
```

```shell
python3 smart_asa_cli.py info 2991

        Asset ID:         2991
        App ID:           2988
        App Address:      T6QBA5AXSJMBG55Y2BVDR6MN5KTXHHLU7LWDY3LGZNAPGIKDOWMP4GF5PU
        Creator:          KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Asset name:       Blue

        Unit name:        🔵

        Maximum issue:    100 🔵
        Issued:           100 🔵
        Decimals:         2
        Global frozen:    False  <-- 😱
        Default frozen:   False
        Manager address:  KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Reserve address:  KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Freeze address:   KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Clawback address: KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
```

### Smart NFT ASA burn
Another exclusive capability of Smart ASA Reserve Address is *burning* the
Smart ASA with the following limitation:

- Smart ASA can not be burned if the *asset is global frozen*;
- Smart ASA can not be burned if the Reserve *account is frozen*;

```shell
python3 smart_asa_cli.py send 2991 KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
T6QBA5AXSJMBG55Y2BVDR6MN5KTXHHLU7LWDY3LGZNAPGIKDOWMP4GF5PU 100
--reserve KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ

 --- Burning 100 units of Smart ASA 2991
 from KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
 to T6QBA5AXSJMBG55Y2BVDR6MN5KTXHHLU7LWDY3LGZNAPGIKDOWMP4GF5PU...
 --- Confirmed!
```

```shell
python3 smart_asa_cli.py info 2991

        Asset ID:         2991
        App ID:           2988
        App Address:      T6QBA5AXSJMBG55Y2BVDR6MN5KTXHHLU7LWDY3LGZNAPGIKDOWMP4GF5PU
        Creator:          KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Asset name:       Blue

        Unit name:        🔵

        Maximum issue:    100 🔵
        Issued:           0 🔵    <-- 👀
        Decimals:         2
        Global frozen:    False
        Default frozen:   False
        Manager address:  KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Reserve address:  KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Freeze address:   KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
        Clawback address: KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ
```

### Smart ASA destroy
Similarly to regular ASA, Smart ASA can be destroyed by Smart ASA Manager
Address if and only if the Smart ASA Creator hold the `total` supply.

```shell
python3 smart_asa_cli.py destroy 2991 KAVHOSWPO3XLBL5Q7FFOTPHAIRAT6DRDXUYGSLQOAEOPRSAXJKKPMHWLLQ

 --- Destroying Smart ASA 2991...
 --- Smart ASA 2991 destroyed!
```

## Security Considerations

### Prevent malicious Clear State

A malicious user could attempt to Clear its Local State to hack the `frozen` state of a Smart ASA. Consider the following scenario:

- Smart ASA `default_frozen = False`;
- Eve is regularly opted-in to the Smart ASA;
- Eve receives 5 Smart ASAs from Bob (Smart ASA manager and freezer) and get freezed afterwards;
- Eve can now Clear its Local State and Opt-In again to reset its `frozen` state and be free to spend the Smart ASAs.

To avoid this situation, the reference implementation introduces:
- *Opt-In condition*: set `frozen` status of the account to `True` if
upon the opt-in, after a Clear State, the account holds an amount of Smart ASA.

### Conscious Smart ASA Destroy

Upon an `asset_destroy`, the `GlobalState` of the *Smart ASA App* is re-initialized and the _Underlying ASA_ destroyed. However, the destroy does not affect users' `LocalState`. Let's consider the case a `manager` invokes an `asset_destroy` over Smart ASA `A` and afterwards an `asset_create` to instantiate Smart ASA `B` with the same *Smart ASA App*.

- Eve was opted-in to *Smart ASA App* and was not frozen;
- Bob (manager) destroys Smart ASA `A` (assuming `circulating_supply = 0`);
- Bob creates Smart ASA `B` with param `default_frozen = True`;
- Eve is opted-in with `frozen = False`;
- Eve can freely receive and spend Smart ASA `B`.

To avoid this issue, the reference implementation includes the current `smart_asa_id` in both the `GlobalState` and `LocalState`. Smart ASA transfers can now be approved only for users opted-in with the current _Underlying ASA_.

## Conclusions

Smart ASA reference implementation is a building block that shows how regular ASA can be turned into a more powerful and sophisticated L1 tool. By adopting ABI the Smart ASA will be easily interoperable and composable with the rest of Algorand's ecosystem (e.g. wallets, chain explorers, external dApp, etc.).

This reference implementation is intended to be used as initial step for more specific and customized transferability logic like: royalties, DAOs' assets, NFTs, in-game assets etc.

We encourage the community to expand and customize this new tool to fit
specific dApp!

Enjoy experimenting and building with Smart ASA!

## Credits to community

Thanks to everyone who contributed or starred the repository! ⭐

[![Stargazers repo roster for @algorandlabs/smart-asa](https://reporoster.com/stars/dark/algorandlabs/smart-asa)](https://github.com/algorandlabs/smart-asa/stargazers)
