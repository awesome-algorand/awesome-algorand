
### @blockshake/defly-connect

JavaScript SDK for integrating [Defly Wallet](https://defly.app) to web applications. For more detailed information, please check our [Defly Manual](https://docs.defly.app/app/overview/).

This is a fork of the Pera connect JavaScript SDK, for more details visit [Pera connect](https://github.com/perawallet/connect) on GitHub.

### Quick Start

Let's start with installing `@blockshake/defly-connect`

```
npm install --save @blockshake/defly-connect
```

```jsx
// Connect handler
deflyWallet
  .connect()
  .then((newAccounts) => {
    // Setup the disconnect event listener
    deflyWallet.connector?.on("disconnect", handleDisconnectWalletClick);

    setAccountAddress(newAccounts[0]);
  })
  .reject((error) => {
    // You MUST handle the reject because once the user closes the modal, deflyWallet.connect() promise will be rejected.
    // For the async/await syntax you MUST use try/catch
    if (error?.data?.type !== "CONNECT_MODAL_CLOSED") {
      // log the necessary errors
    }
  });
```

If you don't want the user's account information to be lost by the dApp when the user closes the browser with user’s wallet connected to the dApp, you need to handle the reconnect session status. You can do this in the following way.

```jsx
// On the every page refresh
deflyWallet.reconnectSession().then((accounts) => {
  // Setup the disconnect event listener
  deflyWallet.connector?.on("disconnect", handleDisconnectWalletClick);

  if (accounts.length) {
    setAccountAddress(accounts[0]);
  }
});
```

After that you can sign transaction with this way

```jsx
// Single Transaction
try {
  const signedTxn = await deflyWallet.signTransaction([singleTxnGroups]);
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

It's enabled by default but in some cases, you may not need the toast message (e.g. you already have signing guidance for users). To disable it, use the shouldShowSignTxnToast option:

## Methods

#### `DeflyWalletConnect.connect(): Promise<string[]>`

Starts the initial connection flow and returns the array of account addresses.

#### `DeflyWalletConnect.reconnectSession(): Promise<string[]>`

Reconnects to the wallet if there is any active connection and returns the array of account addresses.

#### `DeflyWalletConnect.disconnect(): Promise<void | undefined>`

Disconnects from the wallet and resets the related storage items.

#### `DeflyWalletConnect.platform: DeflyWalletPlatformType`

Returns the platform of the active session. Possible responses: _`mobile | null`_

#### `DeflyWalletConnect.isConnected: boolean`

Checks if there's any active session regardless of platform. Possible responses: _`true | false`_

#### `DeflyWalletConnect.signTransaction(txGroups: SignerTransaction[][], signerAddress?: string): Promise<Uint8Array[]>`

Starts the sign process and returns the signed transaction in `Uint8Array`

### Customizing Style

You can override the z-index using the `.defly-wallet-connect-modal` class so that the modal does not conflict with another component on your application.

```scss
.defly-wallet-connect-modal {
  // The default value of z-index is 10. You can lower and raise it as much as you want.
  z-index: 11;
}
```

### Your app name on Defly Wallet

By default, the connect wallet drawer on Defly Wallet gets the app name from `document.title`.

In some cases, you may want to customize it. You can achieve this by adding a meta tag to your HTML between the `head` tag.

```html
<meta name="name" content="My dApp" />
```

### Contributing

All contributions are welcomed! To get more information about the details, please read the [contribution](./CONTRIBUTING.md) guide first.
