# tealinspector

As a developer error like below is not descriptive,

```python
AlgodHTTPError: TransactionPool.Remember: transaction T4EVC7YANLFGBO5KJRIDEAYZBN3KKJC2B7VFRY4ZFMTSZOPTHBTQ: logic eval error: assert failed pc=1328. Details: pc=1328, opcodes===
&&
assert
```

This package gets the lines from the "pc".

## Install the dependency

```python
pip install tealinspector
```

## Use in CLI

```python
tealinspector --network mainnet --application_id 942781578 --program_counter 1328
```

Additionally,
- `--network` is optional. The default value is `mainnet`.
- `--line_count` parameter can be passed. The default value is `25`.

### Output

```python
Line: 594
569 &&
570 gtxn 4 Fee
571 global MinTxnFee
572 intc 10 // 9
573 *
574 ==
575 &&
576 gtxn 4 NumAppArgs
577 intc_0 // 1
578 ==
579 &&
580 gtxna 4 Assets 0
581 bytec_2 // "global_list_asset"
582 app_global_get
583 ==
584 &&
585 gtxna 4 Accounts 1
586 bytec_1 // "global_list_owner"
587 app_global_get
588 ==
589 &&
590 gtxna 4 Accounts 2
591 bytec 8 // addr KQMEN76UOQEHGXPBXUMRGW3KFI7Z57IFXBXWO77HAXYKMISCZF5CAOOITI
592 ==
593 &&
594 assert <----------
```

## About

Developed by [Hipo](https://hipolabs.com).
Licensed under MIT.
