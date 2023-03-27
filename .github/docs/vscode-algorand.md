# Algorand VS Code Extension

This is a VS Code extension for the [Algorand Blockchain](https://www.algorand.com/).

## How to Use

### Prerequisite

- [VS Code](https://code.visualstudio.com/)
- [Docker for Desktop](https://www.docker.com/products/docker-desktop) (this extension uses docker to run Algorand node and Algorand compiler)

### Installation

[Install the extension](https://marketplace.visualstudio.com/items?itemName=obsidians.vscode-algorand) from the VS Code Marketplace. You can also download pre-release versions from [releases](https://github.com/ObsidianLabs/vscode-algorand/releases) and install through *VS Code / Extensions / Install from VSIX...*

### Features

#### TEAL language support

- TEAL syntax highlight
- Hover information
- Auto-complete

#### TEAL & PyTeal compiler integration

1. Open a `*.teal` or `*.pyteal` file
<img src="./screenshots/teal-file.png">

2. Press `Cmd+Shift+B` to call out the compiler task
<img src="./screenshots/teal-compile.png">
3. For the first time running the compiler, you will probably see the *No build task to fun found. Configure Build Task...* notification. Click it and you will see an option *Algorand Compiler: TEAL or PyTeal*. Click it again and VS Code will configure a `tasks.json` file for you. Switch to your `.teal` or `.pyteal` file and click `Cmd+Shift+B` to compile
<img src="./screenshots/compile-task.png">


#### Algorand Panel

Algorand Panel is a dedicated interface for Algorand-related operations, accessible through a button at the left of the bottom bar. Please make sure you have installed and started Docker before using the Algorand Panel.
<img src="./screenshots/bottom-bar.png">
- **Install Algorand node ([algorand/stable](https://hub.docker.com/r/algorand/stable))** - This is the official docker image for Algorand node. Click the *New Instance* button and click the *Algorand version* to open the dropdown. You can install and manage Algorand nodes in the *Algorand Version Manager*.
<img src="./screenshots/version-manager.png">
- **Manage Algorand node instances** - Click the *New Instance* button, enter the instance name and select a version for algorand node to create a new instance. The extension will download the network [snapshot](https://github.com/algorand/sandbox/blob/master/sandbox#L20) to expedite the sync process.
<img src="./screenshots/new-instance.png">
- **Start a local node** - Just click the *Start* button
<img src="./screenshots/start-node.png">
- **Display node logs** - Shown in VS Code terminal
<img src="./screenshots/node-log.png">

> NOTE: When you start a local node, may you need to sync node network, you can use fast catchup, please reference the official document: https://developer.algorand.org/docs/run-a-node/setup/install/#sync-node-network-using-fast-catchup.

#### Algorand transactions

You can use the Algorand Panel to construct transactions with a user interface. It supports

- All types of algorand transaction
	- [regular payment](https://developer.algorand.org/docs/features/transactions/signatures/#multisignatures)
	- [ASA operations](https://developer.algorand.org/docs/features/asa/) including *create*, *opt in*, *transfer*, *modify*, *freeze* and *destroy*
	- [key registration](https://developer.algorand.org/docs/features/transactions/#key-registration-transaction)
- [Atomic Transfers](https://developer.algorand.org/docs/features/atomic_transfers/)
- [Multi-sig](https://developer.algorand.org/docs/features/transactions/signatures/#multisignatures)
- Stateless Algorand Smart Contract (ASC) executions for both
	- [contract account](https://developer.algorand.org/docs/features/asc1/stateless/modes/#contract-account)
	- [delegated approval](https://developer.algorand.org/docs/features/asc1/stateless/modes/#delegated-approval)

There are some examples of transaction in the `example/txns` folder, you can import it and try to push transactions in the Algorand Panel.
<img src="./screenshots/txns-example.png">

Before using the feature, please make sure you have successfully started an Algorand node.

An Algorand transaction can consist of a list of individual parts, known as *atomic transfer*. Therefore, the content of a transaction is an array, which in the simplest case only contains one item. Click the dropdown button at the right of the *Transaction Array* input and select *Add New Item...* You will see a popup window guiding you through making a single transaction. Once you filled out the required information and clicked *Confirm*, you will see the newly created transaction added to the *Transaction Array* as well as in the *Transaction Object* below. If you want to modify or delete it, click the item in the array or the `x` button respectively.
<img src="./screenshots/add-item.png">

To be able to perform the signing process, you need to provide a `keys.json` file of the following format. Be careful that all private information here is saved in plain text so **DO NOT USE THEM ON MAINNET**.

``` js
[
  {
    "address": "{address A}",
    "mnemonic": "{mnemonic for address A}"
  },
  {
    "address": "{address B}",
    "mnemonic": "{mnemonic for address B}"
  }
  // and more
]
```

When finished, click the *Push Transaction* button, confirm and send the transaction to the Algorand network.
<img src="./screenshots/sign-push.png">
#### Algorand smart contract
We provide an example project to demostrate how to use this extension to work on Algorand smart contract.

1. Open the `example` in VS Code as the project root folder;
<img src="./screenshots/example-folder.png">

2. Open the file `main.py` and press `Cmd+Shift+B` to compile the PyTeal script to TEAL. A file of name `main.teal` will be generated;
<img src="./screenshots/teal-gen.png">

3. Open the file `main.teal` and press `Cmd+Shift+B` to compile the TEAL script;
<img src="./screenshots/teal-compile.png">

4. Open the *Algorand Panel* and start an Algorand node. Make sure the node has synced with the network;
<img src="./screenshots/start-node.png">

5. Import the transaction by selecting the file `txns/call_contract.json`;
<img src="./screenshots/call_contract.png">

6. Click the *Push Transaction* button to push the transaction.
<img src="./screenshots/sign-push.png">

## Develop the Extension

### Project Structure

```
.
├── package.json // The extension manifest.
├── example // example project with transaction objects
├── client
│   ├── src
│   │   ├── view // The frontend for Algorand Panel (React)
│   │   └── extension // Extension & Language Client
└── server // Language Server
    └── src
        └── server.ts // Entry point
```

### Run in dev mode

- Run `npm install` in this folder. This installs all necessary npm modules in both the client and server folder
- Open VS Code on this folder
- Press Ctrl+Shift+B to compile the client and server
- Switch to the Debug viewlet
- Select `Launch Client` from the drop down

### Build from source

- Run `npm install -g @vscode/vsce`
- Run `npm install` in this folder
- Run `vsce package`
