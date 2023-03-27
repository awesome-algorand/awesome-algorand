![Pera Connect Cover Image](https://user-images.githubusercontent.com/54077855/179966121-bd9295c3-5f61-4203-b13f-851434e72d35.png)

## @perawallet/connect

JavaScript SDK for integrating [Pera Wallet](https://perawallet.app) to web applications. For more detailed information, please check our [Pera Connect Docs](https://docs.perawallet.app/references/pera-connect/).

[![](https://img.shields.io/npm/v/@perawallet/connect?style=flat-square)](https://www.npmjs.com/package/@perawallet/connect) [![](https://img.shields.io/bundlephobia/min/@perawallet/connect?style=flat-square)](https://www.npmjs.com/package/@perawallet/connect)

## Getting Started

[Learn how to integrate with your JavaScript application](#guide)

[Learn how to Sign Transactions](#sign-transaction)

[Try it out using CodeSandbox](#example-applications)

## Example Applications

<details>
  <summary>Expand details</summary>
  
- [Using React Hooks](https://codesandbox.io/s/perawallet-connect-react-demo-zlvokc)

- [Using React Hooks with React@18](https://codesandbox.io/s/perawallet-connect-react-18-demo-tig2md)

- [Using Vue3](https://codesandbox.io/s/perawallet-connect-vue3-demo-yiyw4b)

- [Using Svelte](https://codesandbox.io/s/perawallet-connect-svelte-demo-ys1m4x)

- [Using Next.js](https://codesandbox.io/s/perawallet-connect-next-js-demo-ryhbdb)

- [Using Nuxt.js](https://codesandbox.io/s/perawallet-connect-nuxt-js-demo-s65z58)

- [Vanilla JS](https://codesandbox.io/s/perawallet-connect-vanillajs-demo-s5pjeo)
</details>

## Quick Start

Let's start with installing `@perawallet/connect`

```
npm install --save @perawallet/connect
```

```jsx
// Connect handler
peraWallet
  .connect()
  .then((newAccounts) => {
    // Setup the disconnect event listener
    peraWallet.connector?.on("disconnect", handleDisconnectWalletClick);

    setAccountAddress(newAccounts[0]);
  })
  .reject((error) => {
    // You MUST handle the reject because once the user closes the modal, peraWallet.connect() promise will be rejected.
    // For the async/await syntax you MUST use try/catch
    if (error?.data?.type !== "CONNECT_MODAL_CLOSED") {
      // log the necessary errors
    }
  });
```

If you don't want the user's account information to be lost by the dApp when the user closes the browser with user’s wallet connected to the dApp, you need to handle the reconnect session status. You can do this in the following way.

```jsx
// On the every page refresh
peraWallet.reconnectSession().then((accounts) => {
  // Setup the disconnect event listener
  peraWallet.connector?.on("disconnect", handleDisconnectWalletClick);

  if (accounts.length) {
    setAccountAddress(accounts[0]);
  }
});
```

After that you can sign transaction with this way

```jsx
// Single Transaction
try {
  const signedTxn = await peraWallet.signTransaction([singleTxnGroups]);
} catch (error) {
  console.log("Couldn't sign Opt-in txns", error);
}
```

## Options

| option                   | default | value                                 |          |
| ------------------------ | ------- | ------------------------------------- | -------- |
| `chainId`                | `4160`  | `416001`, `416002`, `416003` , `4160` | optional |
| `shouldShowSignTxnToast` | `true`  | `boolean`                             | optional |

#### **`chainId`**

Determines which Algorand network your dApp uses.

**MainNet**: 416001

**TestNet**: 416002

**BetaNet**: 416003

**All Networks**: 4160

#### **`shouldShowSignTxnToast`**

<img width="422" alt="Group 48096937" src="https://user-images.githubusercontent.com/54077855/202682828-9ac57b62-58c1-4a83-af3b-e1b7ffad2d89.png">

It's enabled by default but in some cases, you may not need the toast message (e.g. you already have signing guidance for users). To disable it, use the shouldShowSignTxnToast option:

## Methods

#### `PeraWalletConnect.connect(): Promise<string[]>`

Starts the initial connection flow and returns the array of account addresses.

#### `PeraWalletConnect.reconnectSession(): Promise<string[]>`

Reconnects to the wallet if there is any active connection and returns the array of account addresses.

#### `PeraWalletConnect.disconnect(): Promise<void | undefined>`

Disconnects from the wallet and resets the related storage items.

#### `PeraWalletConnect.platform: PeraWalletPlatformType`

Returns the platform of the active session. Possible responses: _`mobile | web | null`_

#### `PeraWalletConnect.isConnected: boolean`

Checks if there's any active session regardless of platform. Possible responses: _`true | false`_

#### `PeraWalletConnect.signTransaction(txGroups: SignerTransaction[][], signerAddress?: string): Promise<Uint8Array[]>`

Starts the sign process and returns the signed transaction in `Uint8Array`

## Customizing Style

You can override the z-index using the `.pera-wallet-modal` class so that the modal does not conflict with another component on your application.

```scss
.pera-wallet-modal {
  // The default value of z-index is 10. You can lower and raise it as much as you want.
  z-index: 11;
}
```

## Your app name on Pera Wallet

By default, the connect wallet drawer on Pera Wallet gets the app name from `document.title`.

In some cases, you may want to customize it. You can achieve this by adding a meta tag to your HTML between the `head` tag.

```html
<meta name="name" content="My dApp" />
```

## Contributing

All contributions are welcomed! To get more information about the details, please read the [contribution](./CONTRIBUTING.md) guide first.
