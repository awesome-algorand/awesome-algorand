![image](https://gitcdn.link/repo/scale-it/algo-builder/master/media/logo.svg)
# Algo Builder Templates

Dapp templates for [Algo Builder](https://github.com/scale-it/algo-builder).

Distributed Applications (dapps) are basically decentralized applications. The templates in this repository are extremely helpful and easy to use. They are designed and implemented to provide aspiring developers a headstart in building dapps on Algorand Blockchain. The templates use [algosdk](https://github.com/algorand/js-algorand-sdk), [Algo Builder](https://github.com/scale-it/algo-builder), [Algosigner](https://github.com/PureStake/algosigner), [Wallet Connect](https://docs.walletconnect.com/quick-start/dapps/client) and [MyAlgo Wallet](https://github.com/randlabs/myalgo-connect)

The detailed description about each template and how to properly use them can be found in the `docs` directory.

## Usage

Each template is a single project (with 1 package.json file) comprising of:
 - An `algob` project : used to deploy ASA's, stateless and stateful contracts. Use `algob deploy` to deploy your `/scripts`. Sample algob project can  be found [here](https://github.com/scale-it/algo-builder/tree/master/packages/algob/sample-project), check the project [README.md](https://github.com/scale-it/algo-builder/blob/master/packages/algob/sample-project/README.md) for more details.
 - [create-react-app](https://github.com/facebook/create-react-app): React js application for your frontend of web dApp. You can use the `AlgoSigner` global object in your app to use it's API's. Example can be found in the `default` template.

Deployment information (using `algob deploy` above) is stored in  `checkpoints` (in `/artifacts`). Checkpoint information is available for user in the React application.

The templates can be easily bootstrap using the `algob unbox-template` command.

After successfully unboxing the template, please link the `algob` package in the template directory to use it for running scripts.
The steps for the process can be found [here](https://github.com/scale-it/algo-builder/#requirements).

To learn how to install and use `algob`, visit [Algo Builder](https://algobuilder.dev).

## Quick Start

`algob unbox-template <template-name> <destination-directory> --force (flag)`
 - if `destination-directory` is not passed then current directory will be used.
 - if `template-name` is not passed, then by default template "/default" is unboxed.
 - if `--force` is passed, then files are overwritten. If it isn't passed, then for each conflicting file, user is made to choose whether to overwrite that file or not.
 - if `template-name` passed is not present as an existing template, the command provides an interactive way to choose from the existing templates.
 - The command also asks if the user wants to install the dependencies as a part of the current process.

## Available templates

- [*htlc*](./htlc): There exists a descriptive example explaining how HTLC contracts work with Algo-Builder. It can be found [here](https://github.com/scale-it/algo-builder/tree/master/examples/htlc-pyteal-ts). Use `algob deploy` to deploy scripts: which creates and fund HTLC contract account which is defined in assets/htlc.py. Withdraw from the escrow using React frontend (after `yarn start`).

- [*shop*](./shop): Template with two rows to buy tickets: a) Queens Concert (5 ALGO); b) Beyonce Concert (10 ALGO). In this template we demonstrate usage of a payment widget to trigger a purchase (in this case it would be purchasing tickets for a concert). You can connect to the network using different wallets i.e either with MyAlgo Wallet, Wallet Connect or AlgoSigner. To know more about wallet integration read [here](https://github.com/scale-it/algo-builder/blob/master/packages/web/README.md) 

- [*wallet*](./wallet): Demonstrate how to connect to Algorand wallet in browser and interact with smart contracts via wallets.

## Add new template / Update existing template

We love your input! We want to make contributing to this project as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features/templates

To add a new dapp template or update an existing one, feel free to create a pull request from your fork to this repo.

You can also chat with us on the `#algo-builder` channel at the Algorand [discord](https://discord.com/invite/hbcUSuw) server.

## Connect algob project settings with a webapp

An algob project can be easily connected/integrated with your dapp. You can learn how to do it in [algob webapp project settings guide](https://github.com/scale-it/algo-builder/blob/develop/docs/guide/algob-web.md#connect-algob-project-settings-with-a-webapp).

## Loading assets and checkpoints in webapp

Assets and checkpoints can be easily loaded in your web app. You can learn how to do it from [checkpoint guide](https://github.com/scale-it/algo-builder/blob/master/docs/guide/algob-web.md#checkpoints).
