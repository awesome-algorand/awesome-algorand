# Algonaut.js

[Examples](https://thencc.github.io/algonautjs/examples/) | [API Docs](https://thencc.github.io/algonautjs/docs/classes/Algonaut.html)

Algonaut.js is designed to be a front end developer friendly and browser friendly library to facilitate intuitive transactions on the Algorand network.  Algorand is incredibly fast, powerful and secure, but it's early days and the tooling is still a little intense.

After working with the existing frameworks for a couple months, we decided to just create what we felt was missing!  Get in here and help!

THE GOAL OF THIS LIBRARY IS SIMPLICITY AND EASE OF USE for the front end crew.  This library aims to bring you closer to key concepts behind the mature transactional fiesta that is Algorand though ease of use.  If you need a robust contract creation and debugging environment, please take the wonderful Algo Builder for a spin!

## API Approach

We package, expose and depend on the JavaScript Algosdk.  It's there if you need it, but that API is pretty intense for day-to-day use.  With Algonaut.js, you can run one-off transactions with a vastly simplified API as compared to transacting with the Algosdk directly.  We're trying to solve for the 90% cases and ask you to dive into the hard stuff only if you actually need to use it.

To create an instance with a node and get ready to transact:

```js
import Algonaut from '@thencc/algonautjs';

const algonaut = new Algonaut({
  BASE_SERVER: 'https://testnet-algorand.api.purestake.io/ps2',
  LEDGER: 'TestNet',
  PORT: '',
  API_TOKEN: { 'X-API-Key': 'MY_KEY_HERE' },
  SIGNING_MODE: 'wallet-connect' // this is mandatory if you are using WalletConnect!
});

algonaut.recoverAccount(a_mnemonic_phrase);
```

## Atomic Transactions

One of the most powerful aspects of the Algorand chain is the ability to group transactions together and run them as one.  The API for this is, again, pretty hard to folow for your average FED.  With Algonaut.js, the aim is to make using this incredibly powerful API simple and intuitive:

```js
// this transaction must pay and and then make a request to an Algorand Smart Contract
// in one transaction. It must also include the asset index in the "assets" arg and an
// app index in the applications arg
const status = await algonaut.sendAtomicTransaction([
  await algonaut.atomicPayment({ to: appAddress, amount: 250000 }),
  await algonaut.atomicCallApp({
    appIndex: appIndex,
    appArgs: ['get_bananas'],
    optionalFields: { applications: [ bananaPriceTicker ] , assets: [ bananaAsaIndex ]
  })
])
```

## Interacting with Smart Contracts

Algorand smart contracts are fast, light, and super clean.  Trying to communicate their APIs across our team has been really hard.  For that reason, Algonaut.js supports a simple TypeScript descriptor for both Stateful and Stateless Smart contracts.  The goal is to be able to load this TypeScript descriptor into your dev envirnment and get a sense of what you can and can't do with a contract's API.

Even the concept of Stateless contracts will be a curve climb for a lot of front end people.  Our goal with this descriptor approach is to communicate a baseline of information about what transactions are permitted, expected, etc, without the front-end developer needing to go into the TEAL or PyTeal directly to figure this stuff out.

Here again we are trying to account for the 90% use case, not every possible case.  The goal is simplicity and ease of use, understanding that there will always be those complex cases where you have to go down to the metal.

```js
const response = await algonaut.callApp(
  {
    appIndex: 123456789,
    appArgs: ['set_name', 'New Name']
  }
);
 ```

## Usage

Install from NPM:

```npm install @thencc/algonautjs --save```

Usage:

```js
import Algonaut from '@thencc/algonautjs';
const algonaut = new Algonaut({
  BASE_SERVER: 'https://testnet-algorand.api.purestake.io/ps2',
  LEDGER: 'TestNet',
  PORT: '',
  API_TOKEN: { 'X-API-Key': 'YOUR_API_TOKEN' }
});

const account = algonaut.recoverAccount("a mnemonic phrase");
algonaut.setAccount(account);

const txnStatus = await algonaut.sendAlgo({
  to: "toAddress",
  amount: 1000,
  optionalFields: { note: "a note for the transaction" }
});
console.log(txnStatus);
```

## Testing

Unit tests are in `tests/algonaut.test.ts` and implemented with Jest.

1. Copy the .env.sample file and replace the values with your node configuration, and a test account mnemonic that is funded with ALGO.
2. Run `npm run test`

Integration tests are also available. See [./tests/README.md](./tests/README.md) for more details.

## Contributing

### To generate docs:

```npm run docs```

[Typedoc options](https://typedoc.org/guides/options/) are set in `typedoc.json`.

---
### Publishing to NPM:

[ *latest/release* ]
stable releases have the default npm tag of `latest` (installable via `npm i @thencc/algonautjs` or `npm i @thencc/algonautjs@latest`) and are automatically published from the repo's `release` branch via a Github Action. so simply pull request the `main` branch (or feature specific branch) into `release` to publish to npm.

[ *beta/main* ]
similarly, pushing commits or merging pull requests to the repo's `main` branch will automatically publish to the npm `beta` release installable via `npm i @thencc/algonautjs@beta`.

note:
- to update either the `latest` or `beta` releases, the version in `package.json` must be higher than the previous release.

### Testing

Please make sure all tests pass before submitting a pull request!

(see [./tests/README.md](./tests/README.md))

---

TBD:

- setting up a dev env
- ESLint and code style
- building and testing with Vite and Node
