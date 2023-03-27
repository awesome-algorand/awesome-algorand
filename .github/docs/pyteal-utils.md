# pyteal-utils

*EXPERIMENTAL WIP*

There is no guarantee to the API of this repository. It is subject to change without a tagged release.

This repository is meant to contain PyTEAL utility methods common in many Smart Contract programs.

## Contents

- [pyteal-utils](#pyteal-utils)
  - [Contents](#contents)
  - [Utils](#utils)
    - [Inline Assembly](#inline-assembly)
    - [Iter](#iter)
    - [Math](#math)
    - [Storage](#storage)
    - [Strings](#strings)
    - [Transactions](#transactions)
  - [Contributing](#contributing)
  - [Prerequisites](#prerequisites)
    - [Set up your PyTEAL environment](#set-up-your-pyteal-environment)

## Utils

### Inline Assembly

- `InlineAssembly` - Can be used to inject TEAL source directly into a PyTEAL program

### Iter

- `accumulate`
- `iterate` - Provides a convenience method for calling a method n times

### Math

- `odd` - Returns 1 if `x` is odd
- `even` - Returns 1 if `x` is even
- `factorial` - Returns `x! = x * x-1 * x-2 * ...`
- `wide_factorial` - Returns `x! = x * x-1 * x-2 * ...`
- `wide_power`
- `exponential` - Approximates `e ** x` for `n` iterations
- `log2`
- `log10` - Returns log base `10` of the integer passed
- `ln` - Returns natural log of `x` of the integer passed
- `pow10` - Returns `10 ** x`
- `max` - Returns the maximum of 2 integers
- `min` - Returns the minimum of 2 integers
- `div_ceil` - Returns the result of division rounded up to the next integer
- `saturation` - Returns an output that is the value of _n_ bounded to the _upper_ and _lower_ saturation values

### Storage

- `GlobalBlob` - Class holding static methods to work with the global storage of an application as a binary large object
- `LocalBlob` - Class holding static methods to work with the local storage of an application as a binary large object
- `global_must_get` - Returns the result of a global storage MaybeValue if it exists, else Assert and fail the program
- `global_get_else` - Returns the result of a global storage MaybeValue if it exists, else return a default value
- `local_must_get` - Returns the result of a loccal storage MaybeValue if it exists, else Assert and fail the program
- `local_get_else` - Returns the result of a local storage MaybeValue if it exists, else return a default value

### Strings

- `atoi` - Converts a byte string representing a number to the integer value it represents
- `itoa` - Converts an integer to the ascii byte string it represents
- `witoa` - Converts an byte string interpreted as an integer to the ascii byte string it represents
- `head` - Gets the first byte from a bytestring, returns as bytes
- `tail` - Returns the string with the first character removed
- `suffix` - Returns the last n bytes of a given byte string
- `prefix` - Returns the first n bytes of a given byte string
- `rest`
- `encode_uvarint` - Returns the uvarint encoding of an integer

### Transactions

- `assert_common_checks` - Calls all txn checker assert methods
- `assert_min_fee` - Checks that the fee for a transaction is exactly equal to the current min fee
- `assert_no_rekey` - Checks that the rekey_to field is empty, Assert if it is set
- `assert_no_close_to` - Checks that the close_remainder_to field is empty, Assert if it is set
- `assert_no_asset_close_to` - Checks that the asset_close_to field is empty, Assert if it is set

Common inner transaction operations

- `pay`
- `axfer`

## Contributing

As [PyTEAL](https://github.com/algorand/pyteal) user, your contribution is extremely valuable to grow PyTEAL utilities!

Please follow the [contribution guide](https://github.com/algorand/pyteal-utils/blob/main/CONTRIBUTING.md)!

## Prerequisites

- [poetry](https://python-poetry.org/)
- [pre-commit](https://pre-commit.com/)
- [py-algorand-sdk](https://github.com/algorand/py-algorand-sdk)
- [pyteal](https://github.com/algorand/pyteal)
- [pytest](https://docs.pytest.org/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Algorand Sandbox](https://github.com/algorand/sandbox)

### Set up your PyTEAL environment

1. Set up the [sandbox](https://github.com/algorand/sandbox) and start it (`dev` mode recommended): `./sandbox up dev`
2. Clone this repo: `git clone https://github.com/algorand/pyteal-utils.git` and `cd` into the `pyteal-utils` directory
3. Install Python dependecies: `poetry install`
4. Activate a virual env: `poetry shell`
5. Configure pre-commit hooks: `pre-commit install`
