# Tealer

Tealer is a static analyzer for [Teal](https://developer.algorand.org/docs/features/asc1/) code. It parses the Teal program, and builds its CFG. The analyzer comes with a set of vulnerabilities detectors and printers allowing to quickly review the contracts.

- [Features](#features)
- [How to install](#how-to-install)
- [How to run](#how-to-run)

## Features

Run Tealer on a Teal contract:

```bash
tealer program.teal
```

For additional configuration, see the [Usage](https://github.com/crytic/tealer/wiki/Usage) documentation.

### Detectors

Num | Detectors | What it Detects | Applies To | Impact | Confidence |
--- | --- | --- | --- | --- | --- |
1 | `is-deletable` | [Deletable Applications](https://github.com/crytic/tealer/wiki/Detector-Documentation#deletable-application) | Stateful | High | High
2 | `is-updatable` | [Upgradable Applications](https://github.com/crytic/tealer/wiki/Detector-Documentation#upgradable-application) | Stateful | High | High
3 | `unprotected-deletable` | [Unprotected Deletable Applications](https://github.com/crytic/tealer/wiki/Detector-Documentation#unprotected-deletable-application) | Stateful | High | High
4 | `unprotected-updatable` | [Unprotected Upgradable Applications](https://github.com/crytic/tealer/wiki/Detector-Documentation#unprotected-updatable-application) | Stateful | High | High
5 | `group-size-check` | [Usage of absolute indexes without validating GroupSize](https://github.com/crytic/tealer/wiki/Detector-Documentation#missing-groupsize-validation) | Stateless, Stateful | High | High
6 | `can-close-account` | [Missing CloseRemainderTo field Validation](https://github.com/crytic/tealer/wiki/Detector-Documentation#missing-closeremainderto-field-validation) | Stateless | High | High
7 | `can-close-asset` | [Missing AssetCloseTo Field Validation](https://github.com/crytic/tealer/wiki/Detector-Documentation#missing-assetcloseto-field-validation) | Stateless | High | High
8 | `missing-fee-check` | [Missing Fee Field Validation](https://github.com/crytic/tealer/wiki/Detector-Documentation#missing-fee-field-validation) | Stateless | High | High
9 | `rekey-to` | [Rekeyable Logic Signatures](https://github.com/crytic/tealer/wiki/Detector-Documentation#rekeyable-logicsig) | Stateless | High | High


For more information, see

- The [Detector Documentation](https://github.com/crytic/tealer/wiki/Detector-Documentation) for information on each detector
- The [Detection Selection](https://github.com/crytic/tealer/wiki/Usage#detector-selection) to run only selected detectors. By default, all the detectors are ran.

### Printers

- Print CFG (`--print-cfg`): Export the CFG of the contract to a dot file.
- `human-summary`: Print a human-readable summary of the contract.
- `function-cfg`: Export the CFG of each subroutine in the contract, works for contracts written in version 4 or greater.
- `call-graph`: Export the call-graph of the contract to a dot file, works for contracts written in version 4 or greater.

Printers output [`dot`](https://graphviz.org/) files.
Use `xdot` to open the files  (`sudo apt install xdot`).

## How to install

### Using Git

```bash
git clone https://github.com/crytic/tealer.git && cd tealer
python3 setup.py install
```

We recommend to install the tool in a [virtualenv](https://virtualenvwrapper.readthedocs.io/en/latest/).


## TODO: Add License