<img src="/docs/media/logo-website.png" height="200" title="Algo Builder" />

The Algo Builder project is composed from the following packages:

- `algob`: framework to automate development of Algorand Assets and Smart Contracts.
- `web`: a package to interact with contracts from react app/frontend app.
- `runtime`: light Algorand runtime and TEAL interpreter.

## Objectives

Algo Builder is an trustworthy framework for Algorand dapps (Decentralized Applications). Its main goal is to make shipping Algorand applications simple, efficient, and salable. Think about it as a Truffle suite for Algorand. The framework provides following functionality through the `algob` tool:

- REPL (console Read-Eval-Print-Loop) to quickly and easily interact with Algorand Standard Assets and Smart Contracts
- integrated testing framework,
- helpful boilerplates allowing developers to focus on use-cases rather than code organization, examples
- Algorand private net
- templates/examples and guides to easily onboard developers

To attract more web developers we plan to build a JavaScript DSL for TEAL with TypeScript bindings (for TEAL inputs). Furthermore we would like to collaborate with SDKs teams to improve the overall development experience and make it ready for enterprise projects. Finally we want to collaborate with Algorand Wallet team to ensure a smooth wallet integration.

## Documentation

- [Home Page](https://algobuilder.dev/)
- [User Docs](https://algobuilder.dev/guide/README)
- [Quick Start](https://algobuilder.dev/guide/README#quick-start)
- [GitHub](https://github.com/scale-it/algo-builder)

## Examples

In the `/examples` directory we developped an extensive list of smart contract templates: from simple ASA management, security tokens to DAO implementations. Check the [list](./examples/README.md).

## dApp Templates

In the `Algo Builder dApp Templates` [repository](https://github.com/scale-it/algo-builder-templates), several templates can be found to use as a base for implementing dApps.

Using the `algob unbox-template` command, the developers can get a pre-built dApp project containing scripts to deploy assets and smart contracts with react.js interactive frontend. The templates use [AlgoSigner](https://github.com/PureStake/algosigner) to securely sign and send transactions to an Algorand Blockchain Network.

Detailed description about the templates can be found [here](https://github.com/scale-it/algo-builder-templates#algo-builder-templates).

# Contributing

### Branch policy

- The active branch is `develop` - all ongoing work is merged into the `develop` branch.
- `master` is the release branch - `develop` is merged into `master` during the release.
- Hot fixes are cherry picked to `master`.

## Working with monorepo

We use **yarn workspaces** to manage all sub packages. here is a list of commands which are helpful in a development workflow

- `yarn workspaces info`
- `yarn workspaces list`
- `yarn workspaces <package-name> <command>`, eg: `yarn workspaces mypkg1 run build` or `yarn workspaces mypkg1 run add --dev react`
- `yarn add algosdk` -- will add `algosdk` to all sub projects (workspaces)

`yarn` does not add dependencies to node_modules directories in either of your packages  –  only at the root level, i.e., yarn hoists all dependencies to the root level. yarn leverages symlinks to point to the different packages. Thereby, yarn includes the dependencies only once in the project.

You have to utilize yarn workspaces’ `noHoist` feature to use otherwise incompatible 3rd party dependencies working in the Mono-Repo environment.

### Creating a local project using algob from source

If you want to test the latest algob version from the `develop` branch, you can:

- `cd <path to algo-builder repo>/packages/algob` and run `./project-dev-script.sh`
- create a new node project and use link (`npm link` or `yarn link`) to link dependencies

### Testing

Each package has rich test suites. Whenever you add something new make sure you provide a test.

Restarting tests by hand is a bit more time consuming. We are using `mocha` framework to execute tests. It has a very useful feature: `mocha --watch` -- which will monitor for all file changes and re-execute tests when a file changed without adding a time overhead to start node and load all TypeScript modules.

To execute tests in a package (eg `packages/runtime`) run:

```
cd packages/runtime
yarn build
yarn run test
```

NOTE: you always have to build the typescript files first. If you are in a development mode, then it's worth to run build in a _watch_ mode (will watch for file changes and automatically recompile project, very fast). You can combine it with a watch mode for tests:

```
# in the project root:
yarn build:watch

# in new terminal:
cd packages/runtime
yarn run test -w
```

To execute tests in all workspace projects, run the following from the root directory:

```
yarn run test
```

To execute and watch tests in all workspaces, run the following from the root directory. Note: it will spawn multiple processes in the same terminal session. So if you want to stop the all processes you can either call `pkill -f mocha` or kill the terminal session.

```
yarn run test:watch
```

NOTE: For the moment test watching in `packages/algob` is not stable because of tear down issues in some test suites. We advise to **not use** test watcher in `packages/algob`.
