# algojig

Algojig is a development and testing jig for Algorand. It allows developers to run transactions and write tests starting from a known Algorand ledger state. It is suitable for testing all kinds of transactions, including application calls and logic signatures.

The ledger state is set declaratively. Transactions are evaluated to produce a block by the real Algorand node internals _without the need to run a separate node of any kind_. All signature checks, fee checks, accounting and logic evaluation is completed as usual.

## Examples

Standalone script:
```py
from algojig import JigLedger, get_suggested_params, generate_accounts
from algosdk.future.transaction import PaymentTxn

secrets, addresses = generate_accounts(2)
sp = get_suggested_params()

ledger = JigLedger()
ledger.set_account_balance(addresses[0], 1_000_000)

transactions = [
    PaymentTxn(
        sender=addresses[0],
        sp=sp,
        receiver=addresses[1],
        amt=200_000,
    ).sign(secrets[0]),
    PaymentTxn(
        sender=addresses[1],
        sp=sp,
        receiver=addresses[0],
        amt=1,
    ).sign(secrets[1]),
]
block = ledger.eval_transactions(transactions)
print(block[b'txns'])
```

Example test:
```py
    def test_fail_overspend(self):
        transactions = [
            PaymentTxn(
                sender=addresses[0],
                sp=sp,
                receiver=addresses[0],
                amt=100,
            ).sign(secrets[0]),
        ]
        with self.assertRaises(Exception) as e:
            block = self.ledger.eval_transactions(transactions)
        self.assertIn('overspend', e.exception.args[0])
```

See [tests/test_ledger.py](tests/test_ledger.py) and [examples](examples/) and for more examples.

## Tests

```
python -m unittest tests.test_ledger
```


## Requirements

Algojig relies on a binary compiled from a Go project using go-algorand. The package currently includes binaries compiled for MacOS x86_64 and arm64 architectures. Linux or Windows are currently not supported.
