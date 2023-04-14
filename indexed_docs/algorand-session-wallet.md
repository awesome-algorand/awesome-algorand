> This resource is auto indexed by AwesomeAlgo, all credits to algorand-session-wallet, for more details refer to https://github.com/barnjamin/algorand-session-wallet

---

# algorand-session-wallet

*PRs welcome*

example: https://github.com/barnjamin/algorand-session-wallet-example

```sh
npm -i algorand-session-wallet
```

```js
const sw = new SessionWallet("TestNet", "algosigner-wallet")
if(!sw.connect()) return alert("Couldnt connect")

//...

const accts = sw.accountList()

//...

sw.signTxn([txnblobs])

//...

sw.disconnect()

```
