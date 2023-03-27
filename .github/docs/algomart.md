<br />
<p align="center"><img alt="AlgoMart Logo" src="./AlgoMart-Logo.png" width="400" height="140"></p>
<br />

# AlgoMart Marketplace

## 🚧 2.0 Work In Progress 🚧

### Please note that the current version of this project should be considered _*unstable*_ for the time being as we finalize the upgrade to version 2.0

---

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)][code of conduct]

### Migration

This project is developed to be a foundational starter for creating your own NFT storefront on the Algorand blockchain. It is a monorepo that includes:

- A [headless CMS](./apps/cms) (Directus)
- A [back-end API](./apps/api) (Fastify)
- A [job server](./apps/scribe) (BullMQ)
- A [front-end](./apps/web) sample implementation (NextJS)
- Shared [libs](#libs)
- [Terraform templates](./terraform/envs/dev) for setting up infrastructure on Google Cloud Platform
- [GitHub Workflows](./.github/workflows) for linting, type-checking, building, dockerizing, and deploying

## 📚 General Project Overview

The main purpose of this platform is twofold; to make it easy for developers to spin up a custom storefront that interfaces with the blockchain, and to make that storefront accessible to the storefront administrators and its end-users who might not be familiar with the technical nuances of blockchain technology.

In order to accomplish this, storefront administrators should be able to easily to create, configure, and mint NFTs. Likewise, end-users should be able to redeem, purchase, or bid on them without concern of what's happening behind the scenes on the blockchain.

### Backend Overview

To accomplish these challenges, **templates** are used within the CMS.

NFT Templates represent an NFT that will be minted (any number of specified times). It includes key information such as title, description, rarity, and other important configurable metadata that will be consumed by the API.

NFT Templates are grouped within Pack Templates. Packs can contain one or more NFT Templates and also have a number of configurable settings. Most notably, they can be set to be purchasable, to be auctioned, to be claimed via an auto-generated redemption code, or to be given away free. For a full overview of the CMS model, see the [CMS README](apps/cms/README.md).

Meanwhile, the API continually polls the CMS for new NFT Templates and Pack Templates. So once the templates are configured in the CMS, the API will find them, generate the NFT instances in the API's database, and then group them into Packs based on the Pack template's configuration.

From here on out, the NFT and Pack information can be accessed from the API and displayed to an end-user, who can then purchase, bid on, redeem, or freely claim the Pack (based on the corresponding Pack template's configuration).

### Frontend Overview

The backend API can be accessed via REST endpoints by a frontend. This frontend can be custom-built, or the included NextJS web project can be used and further customized.

When an end-user registers through the site, a user account record is created via the API and a new Algorand wallet is generated on their behalf. That wallet's mnemonic key is encrypted via a secret PIN code the end-user provides upon sign-up.

An authenticated end-user can then engage in user flows that allow them to acquire Packs (again, containing one or more to-be-minted NFTs). In the case of a monetary transaction, an end-user can enter their credit card information. Upon submission, this information will be validated and processed via Circle's Payments API. Upon a valid confirmation, the API then mints and transfers the assets to the user's wallet.

## 🚧 Pre-release

This software is in a pre-release state. This means while we strive to keep it stable and include database migrations, sometimes we may introduce breaking changes or an accidental bug. Follow our [issue tracker][issue tracker] for more details on what's coming next.

## ✅ Requirements

- Node.js v16.10 or greater (lts is v16.13.1 as of Jan 2022 and works well), npm v7 or greater (manage version via [nvm][nvm])
- PostgreSQL ([Postgres.app][postgres app] is recommended on macOS, or run via `docker-compose up db`)
- [Redis][redis] for jobs
- algod (Algorand node)
  - Consider using a [third party api][third party api] for initial setup and experimentation.
  - A [sandbox][sandbox] is [recommended][recommended] for continued learning about Algorand and its smart signatures/smart contracts
- [Circle][circle] account for taking payments
- [Firebase][firebase] account for authentication
- [Pinata][pinata] account for storing NFTs
- [Chainalysis][chainalysis] for blockchain address verification

## 🤷 Optional

- [SendGrid][sendgrid] for sending email notifications
- [Google Cloud Platform][gcp] account for hosting
- Install the [Nx CLI][nx cli] for ease of development: `npm i -g nx`
- [Docker][docker] for a local dev environment using VSCode Dev Containers or docker compose

## 🚀 Get Started

You can either build and run each application manually or you can use `docker-compose`.

### Development Environment Setup

1. Create .env files

   ```bash
      cp ./.env.exmaple ./.env
      cp ./apps/cms/.env.example ./apps/cms/.env
      cp ./apps/scribe/.env.example ./apps/scribe/.env
      cp ./apps/api/.env.example ./apps/api/.env
      cp ./apps/web/.env.example ./apps/web/.env
   ```

2. Address ` SETUP:` comments in env files

3. Initialize the databases with `npm run drop-tables && npm run initialize`

4. Start the CMS `nx serve cms`

   1. If database is empty, it will automatically seed itself with test data
   2. Checkpoint: you should be able to log in the CMS and see some sample pack templates (http://localhost:8055/admin/content/pack_templates)

5. Start the job server `nx serve scribe`

   1. Checkpoint: you should be able to see the jobs dashboard (http://localhost:3002/bullboard)
   2. Run the `sync-cms-cache` job manually, twice, by promoting the delayed job in the dashboard
   3. Checkpoint: you should see rows in the Pack table in the API database (`algomart_api.public.Pack`)

6. Start the API `nx serve api`

   1. Checkpoint: you should be able to see swagger docs (http://localhost:3001/docs/static/index.html)

7. Start the web server `nx serve web`

   1. Checkpoint: You should be able to register an AlgoMart account, sign in and see some drops available (http://localhost:3000/drops)

8. Configure [Circle webhooks](apps/api#circle-webhooks)

   1. Add Money to your merchant wallet to cover/float [pending end user credit card transactions](https://developers.circle.com/docs/post-payments-processing#card-payments-settlement)
      1. Get your merchant wallet's address using your Circle my-sandbox account's "Transfer from a blockchain wallet" functionality
      2. Send testnet USDC to your merchant wallet from [Algorand Testnet Dispenser](https://dispenser.testnet.aws.algodev.network/)
   2. Checkpoint: you can add money to your wallet using one of Circle's [test card numbers](https://developers.circle.com/docs/test-card-numbers)

9. Purchase a pack using credits

   1. Using credits from the previous step
   2. Checkpoint: you have collectibles in your collection

10. Configure an Algorand sandbox (optional)

    ### Local Algorand Setup

    This is an alternative to using a 3rd party Algorand node API.
    For local development, the [Algorand Sandbox](https://github.com/algorand/sandbox) is handy docker instance that makes interfacing with the blockchain simple from your local machine.
    More information on Sandbox vs Third-party API services [here](https://developer.algorand.org/docs/get-started/devenv/)

    - Download the [Algorand Sandbox](https://github.com/algorand/sandbox) and start up the docker instance:

    ```bash
    ./sandbox up
    ```

    - By default this will create a private network, as well as fund a few accounts with Algos. You'll need to generate a passphrase mnemonic for one of these accounts. To see the list of the created accounts:

    ```bash
    ./sandbox goal account list
    ```

    - Take the `<ADDRESS>` from the first account and input here

    ```bash
    ./sandbox goal account export -a <ADDRESS>
    ```

    Use this outputted mnemonic as the FUNDING_MNEMONIC variable within the `.env` file within the `api` and `scribe` projects.

    _Disclaimer:_ If you use a private network as described above, you will not be able to test features that require a public network, including the [Pera Wallet](https://perawallet.app/) (the mobile non-custodial wallet app for Algorand). For running a public network node, see below.

    ### Testnet Algorand Setup

    Alternatively you may choose to run the algorand sandbox on a public network such as testnet. In that case you'll need a few additional steps, such as creating and funding an account.

    - To run sandbox on testnet:

    ```bash
    ./sandbox up testnet
    ```

    - Then create an account:

    ```bash
    ./sandbox goal account new
    ```

    This will create a new, unfunded account. Testnet accounts can be funded with fake Algos using the [Testnet Dispenser](https://dispenser.testnet.aws.algodev.network/). You can then follow the account export steps above to get your mnemonic passphrase.

    _Disclaimer:_ The sandbox testnet configuration will not provide an indexer. There are public indexer's available (e.g. https://algoindexer.testnet.algoexplorerapi.io/), and the Indexer Configuration will need to be updated in both `app` and `scribe` .env files.

    To learn more about available `goal` CLI commands for e.g. creating a new account, see [the Alogrand docs](https://developer.algorand.org/docs/clis/goal/goal/).

## 💾 DB initialization

To initialize the databases:

```bash
npm run drop-tables  # drop existing CMS and API databases
npm run initialize   # initialize the CMS and API databases
```

## 🏃 Run

Run all 4 projects (api, cms, web, & scribe) simultaneously with combined output.

```bash
npm start
```

## 📦 Build

To build _everything_:

```bash
npm run build
```

## ⚙️ Unit Tests

To run all tests:

```
npm test
```

To run tests/lint only a specific library:

```bash
# assuming shared-utils is an nx library
# (ie. an alias for libs/shared/utils defined in workspace.json)...
nx run shared-utils:test
nx run shared-utils:lint
```

## ⚙️ E2E Tests

To run End-to-end integration tests with Cypress:

Be sure to follow steps outlined in the [web-e2e README](apps/web-e2e/README.md) first.

```bash
# To open the Cypress UI and watch the tests run:
npm run test:cypress:open

# To run the test in the terminal
npm run test:cypress:run
```

## 🧹 Linting

To run eslint for all projects:

```
npm run lint
```

## 🐳 Running with docker-compose

Alternative to running the services manually, they can also be run via Docker. After creating the relevant `.env` files above, add a file called `.babelrc` to the root of the web project (`apps/web/`) and populate it with:

```json
{ "presets": ["next/babel"] }
```

Then run all services:,

## 🆚 Running with VSCode Dev Containers.

This codebase leverages VSCode Dev Containers.

1. Install VSCode Remote Containers plugin.

1. Open the project in VSCode. When prompted, click the "Reopen in Container" button

## 🪆 Project dependencies

When updating dependencies, there are a few things that must be kept in mind.

### Directus

If doing any updates to the Directus version, the version numbers must match across the application and the snapshot.yml file must be created with the updated version. You can use `apps/cms/scripts/directus-update.sh` to perform these steps. Update the version number at the top of the script.

1. Update versions
   1. Pin `directus`, `@directus/sdk`, and `@directus/extensions-sdk` versions in `package.json`
   1. Pin `host` version in `/apps/cms/extensions/displays/pack-price/package.json`
   1. Pin `host` version in `/apps/cms/extensions/interfaces/price-conversion/package.json`
   1. Pin `host` version in `/apps/cms/extensions/hooks/import-data/package.json`
   1. Pin `host` version in `/apps/cms/extensions/hooks/kyc-management/package.json`
   1. Pin `host` version in `/apps/cms/extensions/hooks/set-verification-status/package.json`
   1. Set npm install step of `/docker/deploy/cms/Dockerfile` to version
1. Run `npm install` from root to generate latest `package-lock.json`
1. Run `nx export cms` to generate latest `snapshot.yml`
1. Rebuild cms extensions, either via `nx build cms` or all of these:
   1. Run `nx build-price-display cms` to generate latest js file
   1. Run `nx build-price-interface cms` to generate latest js file
   1. Run `nx build-import-data cms` to generate latest js file
   1. Run `nx build-kyc-management cms` to generate latest js file
   1. Run `nx build-set-verification-status cms` to generate latest js file

## Libs

`libs/*`

Shared Typescript [interfaces and enums](./libs/schemas)

For performance and code organization reasons, the [Nx docs](https://nx.dev/structure/applications-and-libraries) recommend
putting as much functionality as possible into libs, even if the code is only used in a single app. In Nx, a lib is more than just a directory under the `libs/` directory. Each lib must have an entry in the workspace.json file for the lib to build and import correctly.

Linting will fail for any lib code that tries to import code from an app. This means that lib code should never access things like
global configuration variables or environment variables. (eg. `Configuration`) Rather, lib code should receive any environment configuration via
arguments that are passed in.

If you wanted to create a new library at the path `libs/shared/utils`, you'd use the nx generator...
`nx generate @nrwl/node:lib utils --directory shared`

## 🚢 Deployment

Please see the detailed [step-by-step guide](./docs/deploy/README.md)
for instructions on how to use the included Terraform templates
and Github Workflow to create a complete storefront environment
on Google Cloud Platform.

[algorand sandbox]: https://github.com/algorand/sandbox
[api]: apps/api
[circle]: https://www.circle.com
[cms]: apps/cms
[code of conduct]: CODE_OF_CONDUCT.md
[directus]: https://directus.io
[firebase]: https://firebase.google.com/
[gcp]: https://cloud.google.com
[issue tracker]: https://github.com/deptagency/algomart/issues
[nvm]: https://github.com/nvm-sh/nvm
[postgres app]: https://postgresapp.com
[schemas]: libs/schemas
[sendgrid]: https://sendgrid.com
[web]: apps/web
[nx cli]: https://nx.dev/using-nx/nx-cli#nx-cli
[pinata]: https://www.pinata.cloud/
[scribe]: apps/scribe
[redis]: https://redis.io
[docker]: https://www.docker.com
[third party api]: https://developer.algorand.org/docs/get-started/devenv/#2-third-party-api-services
[sandbox]: https://developer.algorand.org/docs/get-started/devenv/#1-sandbox
[recommended]: https://developer.algorand.org/docs/get-started/devenv/#recommendation
[chainalysis]: https://www.chainalysis.com/
