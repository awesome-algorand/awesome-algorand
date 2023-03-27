> This resource is auto indexed by AwesomeAlgo, all credits to use-wallet, for more details refer to https://github.com/txnlab/use-wallet

---

# @TxnLab/use-wallet

React hooks for using Algorand compatible wallets with web applications.

## Supported Providers

- [Pera](https://perawallet.app/)
- [MyAlgo](https://wallet.myalgo.com/home)
- [Defly](https://defly.app)
- [AlgoSigner](https://www.purestake.com/technology/algosigner)
- [Exodus](https://www.exodus.com)
- [WalletConnect](https://walletconnect.com)
- [KMD](https://developer.algorand.org/docs/rest-apis/kmd)

## Demo

Preview a basic implementation in [Storybook](https://txnlab.github.io/use-wallet) or check out [this example](https://github.com/gabrielkuettel/use-wallet-example).

## Quick Start

⚠️ If you're using `create-react-app` and `webpack 5` (most newer React projects), you will need to install polyfills. Follow [these directions](#webpack-5).

### Yarn

```bash
yarn add @txnlab/use-wallet
```

Install peer dependencies (if needed)

```bash
yarn add algosdk @blockshake/defly-connect @perawallet/connect @randlabs/myalgo-connect @walletconnect/client algorand-walletconnect-qrcode-modal @json-rpc-tools/utils
```

### NPM

```bash
npm install @txnlab/use-wallet
```

Install peer dependencies (if needed)

```bash
npm install algosdk @blockshake/defly-connect @perawallet/connect @randlabs/myalgo-connect @walletconnect/client algorand-walletconnect-qrcode-modal @json-rpc-tools/utils
```

### Set up the Wallet Provider

In `app.js`, initialize the Wallet Provider so that the `useWallet` hook can be used in the child components, and use the `reconnectProviders` function to restore sessions for users returning to the app.

```jsx
import React from 'react'
import { reconnectProviders, initializeProviders, WalletProvider } from '@txnlab/use-wallet'

const walletProviders = initializeProviders()

export default function App() {
  // Reconnect the session when the user returns to the dApp
  React.useEffect(() => {
    reconnectProviders(walletProviders)
  }, [])

  return <WalletProvider value={walletProviders}>...</WalletProvider>
}
```

The `reconnectProviders` function is used to restore session states of wallets that rely on the `WalletConnect` protocol.

By default, all of the supported providers except for `KMD` are returned by `useConnectWallet`. An array can be passed to `initializeProviders` to determine which providers your dApp supports, as shown below.

```jsx
import { initializeProviders, PROVIDER_ID } from '@txnlab/use-wallet'

const walletProviders = initializeProviders([PROVIDER_ID.KMD_WALLET, PROVIDER_ID.WALLET_CONNECT])
```

For more configuration options, see [Provider Configuration](#provider-configuration).

### Connect

Map through the `providers` object to list the providers and enable users to connect.

```jsx
import React from 'react'
import { useWallet } from '@txnlab/use-wallet'

export default function Connect() {
  const { providers, activeAccount } = useWallet()

  // Map through the providers.
  // Render account information and "connect", "set active", and "disconnect" buttons.
  // Finally, map through the `accounts` property to render a dropdown for each connected account.
  return (
    <div>
      {providers?.map((provider) => (
        <div key={'provider-' + provider.metadata.id}>
          <h4>
            <img width={30} height={30} alt="" src={provider.metadata.icon} />
            {provider.metadata.name} {provider.isActive && '[active]'}
          </h4>
          <div>
            <button onClick={provider.connect} disabled={provider.isConnected}>
              Connect
            </button>
            <button onClick={provider.disconnect} disabled={!provider.isConnected}>
              Disconnect
            </button>
            <button
              onClick={provider.setActiveProvider}
              disabled={!provider.isConnected || provider.isActive}
            >
              Set Active
            </button>
            <div>
              {provider.isActive && provider.accounts.length && (
                <select
                  value={activeAccount?.address}
                  onChange={(e) => provider.setActiveAccount(e.target.value)}
                >
                  {provider.accounts.map((account) => (
                    <option key={account.address} value={account.address}>
                      {account.address}
                    </option>
                  ))}
                </select>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
```

Each provider has two connection states: `isConnected` and `isActive`.

`isConnected` means that the user has authorized the provider to talk to the dApp. The connection flow does not need to be restarted when switching to this wallet from a different one.

`isActive` indicates that the provider is currently active and will be used to sign and send transactions when using the `useWallet` hook.

The `activeAccount` is the primary account that is currently active and will be used to sign and send transactions.

### Sign and send transactions

Construct a transaction using `algosdk`, and sign and send the transaction using the `signTransactions` and `sendTransactions` functions provided by the `useWallet` hook.

```jsx
import React from 'react'
import {
  useWallet,
  DEFAULT_NODE_BASEURL,
  DEFAULT_NODE_TOKEN,
  DEFAULT_NODE_PORT
} from '@txnlab/use-wallet'
import algosdk from 'algosdk'

const algodClient = new algosdk.Algodv2(DEFAULT_NODE_TOKEN, DEFAULT_NODE_BASEURL, DEFAULT_NODE_PORT)

export default function Transact() {
  const { activeAddress, signTransactions, sendTransactions } = useWallet()

  const sendTransaction = async (from?: string, to?: string, amount?: number) => {
    if (!from || !to || !amount) {
      throw new Error('Missing transaction params.')
    }

    const suggestedParams = await algodClient.getTransactionParams().do()

    const transaction = algosdk.makePaymentTxnWithSuggestedParamsFromObject({
      from,
      to,
      amount,
      suggestedParams
    })

    const encodedTransaction = algosdk.encodeUnsignedTransaction(transaction)

    const signedTransactions = await signTransactions([encodedTransaction])

    const waitRoundsToConfirm = 4

    const { id } = await sendTransactions(signedTransactions, waitRoundsToConfirm)

    console.log('Successfully sent transaction. Transaction ID: ', id)
  }

  if (!activeAddress) {
    return <p>Connect an account first.</p>
  }

  return (
    <div>
      <button
        onClick={() => sendTransaction(activeAddress, activeAddress, 1000)}
        className="button"
      >
        Sign and send transactions
      </button>
    </div>
  )
}
```

### Display account details

The `activeAccount` object can be used to display details for the currently active account. For convenience, the `activeAddress` property shows the currently active address.

```jsx
import React from 'react'
import { useWallet } from '@txnlab/use-wallet'

export default function Account() {
  const { activeAccount } = useWallet()

  if (!activeAccount) {
    return <p>No account active.</p>
  }

  return (
    <div>
      <h4>Active Account</h4>
      <p>
        Name: <span>{activeAccount.name}</span>
      </p>
      <p>
        Address: <span>{activeAccount.address}</span>
      </p>
      <p>
        Provider: <span>{activeAccount.providerId}</span>
      </p>
    </div>
  )
}
```

### Check connection status

The `isActive` and `isReady` properties can be used to check the status of the wallets. The `isActive` property determines whether or not an account is currently active. The `isReady` property shows if `use-wallet` has mounted and successfully read the connection status from the providers. These properties are useful when setting up client side access restrictions, for example, by redirecting a user if no wallet is active, as shown below.

```jsx
const { isActive, isReady } = useWallet()

useEffect(() => {
  if (isReady && isActive) {
    allowAccess()
  }

  if (isReady && !isActive) {
    denyAccess()
  }
})
```

## Provider Configuration

The `initializeProviders` functon accepts a configuration object that can be used to configure the nodes that the providers use to send transactions, as shown below.

```jsx
const walletProviders = initializeProviders([], {
  network: 'devmodenet',
  nodeServer: 'http://algod',
  nodeToken: 'xxxxxxxxx',
  nodePort: '8080'
})
```

Passing an empty array as the first argument enables all of the default providers. The `network` property should be specified as `betanet`, `testnet`, `mainnet` or the name of your local development network.

For more custom configuration options, the providers can be configured individually by creating an object and passing it to the `WalletProvider` where the key contains the provider ID, and the value calls the `init` function of the provider client. See below for an example:

```jsx
...

import {
  PROVIDER_ID,
  pera,
  myalgo,
} from "@txnlab/use-wallet";

const walletProviders = {
  [PROVIDER_ID.PERA]: pera.init({
    clientOptions: {
      shouldShowSignTxnToast: true,
    },
  }),
  [PROVIDER_ID.MYALGO]: myalgo.init({
    network: "devmodenet",
    algodOptions: ["xxxxxxxxx", "http://algod", "8080"],
    clientOptions: { disableLedgerNano: true },
  }),
};

...

<WalletProvider value={walletProviders}>
  ...
</WalletProvider>
```

## Static Imports

By default, `use-wallet` dynamically imports all of the dependencies for the providiers, as well as `algosdk`, to reduce bundle size.

Some React frameworks, like [Remix](https://remix.run/), do not support dynamic imports. To get around this, those dependencies can be imported in your application and passed to the `useWallet` provider. See below for an example.

```jsx
...

import algosdk from "algosdk";
import MyAlgoConnect from "@randlabs/myalgo-connect";
import { PeraWalletConnect } from "@perawallet/connect";
import { DeflyWalletConnect } from "@blockshake/defly-connect";
import WalletConnect from "@walletconnect/client";
import QRCodeModal from "algorand-walletconnect-qrcode-modal";

const walletProviders = {
  [PROVIDER_ID.PERA]: pera.init({
    algosdkStatic: algosdk,
    clientStatic: PeraWalletConnect,
  }),
  [PROVIDER_ID.MYALGO]: myalgo.init({
    algosdkStatic: algosdk,
    clientStatic: MyAlgoConnect,
  }),
  [PROVIDER_ID.DEFLY]: defly.init({
    algosdkStatic: algosdk,
    clientStatic: DeflyWalletConnect,
  }),
  [PROVIDER_ID.EXODUS]: exodus.init({
    algosdkStatic: algosdk,
  }),
  [PROVIDER_ID.ALGOSIGNER]: algosigner.init({
    algosdkStatic: algosdk,
  }),
  [PROVIDER_ID.WALLETCONNECT]: walletconnect.init({
    algosdkStatic: algosdk,
    clientStatic: WalletConnect,
    modalStatic: QRCodeModal,
  }),
};

export default function App() {
  ...

  return (
    <WalletProvider value={walletProviders}>
      ...
    </WalletProvider>
  );
}

```

Note that some of the providers do not require static imports to be provided. This is usually the case of providers that are browser extensions.

## Local Development

### Install dependencies

```bash
yarn install
```

### Demo in Storybook

```bash
yarn dev

```

To develop against a local version of `use-wallet` in your application, do the following:

### Build the library

```bash
yarn build
```

### Symlink the library

In the root of `use-wallet` directory, run:

```bash
yarn link
```

In the root of your application, run:

```bash
yarn link @txnlab/use-wallet
```

### Symlink React

In the root of your application, run:

```bash
cd node_modules/react
yarn link
```

In the root of `use-wallet` directory, run:

```bash
yarn link react
```

## Used By

Are you using `@txnlab/use-wallet`? We'd love to include you here. Let us know! [Twitter](https://twitter.com/NFDomains) | [Discord](https://discord.gg/7XcuMTfeZP) | [Email](mailto:admin@txnlab.dev)

- [@algoscan/use-wallet-ui](https://github.com/algoscan/use-wallet-ui)
- [@algoworldnft/algoworld-swapper](https://github.com/algoworldnft/algoworld-swapper)

Full list of [Dependents](https://github.com/TxnLab/use-wallet/network/dependents)

## License

See the [LICENSE](https://github.com/TxnLab/use-wallet/blob/main/LICENSE.md) file for license rights and limitations (MIT)
