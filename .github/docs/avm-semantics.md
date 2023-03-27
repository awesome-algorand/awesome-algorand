> This resource is auto indexed by AwesomeAlgo, all credits to avm-semantics, for more details refer to https://github.com/runtimeverification/avm-semantics

---

KAVM &mdash; Algorand Virtual Machine and TEAL Semantics in K
=============================================================

🛠️**Work in progress**🛠️

KAVM leverages the [K Framework](https://kframework.org/) to empower Algorand smart contracts' developers with property-based testing and formal verification.

Getting Started
---------------

### Installing KAVM

For now, KAVM can only be installed from source. We intend to provide a Docker image and standalone packages for popular operating systems at a later stage. To install KAVM from source, please refer to [Working on KAVM](#working-on-kavm).

### Entry points

The semantics can be used either via the `kavm` command-line interface or programmaticaly with the `kavm` Python package.

#### `kavm` runner script

The `kavm` Python tool provides a command-line interface for the semantics:
* compiling the semantics with the LLVM and Haskell backends with `kavm kompile`
* executing concrete simulations and tests are run via `krun` and the K LLVM Backend with `kavm run`
* *Not yet implemented* proving properties by symbolic execution via `kprove` and the K Haskell Backend with `kavm prove`
* parsing TEAL programs via `kast` with `kavm kast`

See `kavm --help` for more information.

**Note**: make sure to activate the Python virtual environment build by KAVM with `. .build/venv/bin/activate` for the `kavm` script to be available.

#### `kavm` Python library

[`kavm`](./kavm) provides Python bindings to KAVM
* `kavm.algod` integrates KAVM with `py-algorand-sdk` and `algod` &mdash; the Algorand node client, making it possible to run existing deployment and testing scripts on top of KAVM.
* `kavm.__main__` is the implementation of the `kavm` command-line tool

Testing harness
---------------

### Concrete Execution Tests

The tests are located in [`tests/`](tests/).

Run `make test-avm-semantics -j8` to execute the test suite. Adjust the `-jX` option as needed to run `X` tests in parallel.

Each test has two components:
* a test scenario, `.avm-simulation` in [`tests/scenarios/`](tests/scenarios/) that defines the initial network state, the input transaction group and declares which TEAL programs it uses.
* a TEAL program `.teal`, or several programs, in [`tests/teal-sources/`](tests/teal-sources/);

Currently, a test is considered passing if the `kavm` runner script returns 0. The final state network state is not examined.

The negative test scenarios are expected to fail and have the `.fail.avm-simulation` file extension.

### Symbolic Proofs

**NOTE**: the specs have not yet been fully ported to the current semantics and are failing.
They are not checked on CI and are not called by `make test`.

The specifications are located in [`tests/specs/`](tests/specs/).

Run `make test-avm-prove` to verify the specifications.

The [`verification.md`](tests/specs/verification.k) module must be compiled with the Haskell backend and included in every spec file.
The Makefile target `test-avm-prove` ensures that the verification module is compiled properly before checking the specs.

Repository Structure
--------------------

#### K files

##### Algorand network state and AVM files

The AVM semantics source files are located in [`lib/include/kframework/avm/`](lib/include/kframework/avm/):

* [`avm-configuration.md`](lib/include/kframework/avm/avm-configuration.md) defines the top-level K configuration of the AVM:
  - AVM execution state
  - TEAL interpreter state
* [`blockchain.md`](lib/include/kframework/avm/blockchain.md) defines the Algorand network state: accounts, apps and assets.
* [`txn.md`](lib/include/kframework/avm/txn.md) defines the representation of Algorand transactions.
* [`avm-execution.md`](lib/include/kframework/avm/avm-execution.md) defines the execution flow of AVM:
  - transaction evaluation and execution process, depending on its type;
  - starting/stopping TEAL execution;
  - AVM-level panic behaviors;
  - basic syntax of simulation scenarios.
* [`avm-initialization.md`](lib/include/kframework/avm/avm-initialization.md) defines rules that initialize AVM with a specific initial network state and the supplied transaction group;
* [`avm-limits.md`](lib/include/kframework/avm/avm-limits.md) defines the constants that govern AVM execution: max transaction group size, max TEAL stack depth, etc.
* [`avm-txn-deque.md`](lib/include/kframework/avm/avm-txn-deque.md) defines an internal data structure that handles transaction execution schedule.
* [`args.md`](lib/include/kframework/avm/args.md) defines the representation of Logic Signature transaction arguments.

##### TEAL Interpreter

Transaction Execution Approval Language (TEAL) is the language that governs approval of Algorand transactions and serves as the execution layer for Algorand Smart Contracts.

The K modules describing syntax and semantics of TEAL are located in [`lib/include/kframework/avm/teal/`](lib/include/kframework/avm/teal/):

* [`teal-types.md`](lib/include/kframework/avm/teal/teal-types.md) defines basic types representing values in TEAL and various operations involving them.
* [`teal-constants.md`](lib/include/kframework/avm/teal/teal-constants.md) defines a set of integer constants TEAL uses, including transaction types and on-completion types.
* [`teal-fields.md`](lib/include/kframework/avm/teal/teal-fields.md) defines sets of fields that may be used as arguments to some specific opcodes in TEAL, such as `txn/txna` fields and `global` fields.
* [`teal-syntax.md`](lib/include/kframework/avm/teal/teal-syntax.md) defines the syntax of (textual) TEAL and the structure of its programs.
* [`teal-stack.md`](lib/include/kframework/avm/teal/teal-stack.md) defines the K representation of TEAL stack and the associated operations.
* [`teal-execution.md`](lib/include/kframework/avm/teal/teal-execution.md) defines the execution flow of the interpreter:
  - [Interpreter Initialization](lib/include/kframework/avm/teal/teal-execution.md#teal-interpreter-initialization)
  - [Execution](lib/include/kframework/avm/teal/teal-execution.md#teal-execution)
  - [Interpreter Finalization](lib/include/kframework/avm/teal/teal-execution.md#teal-interpreter-finalization)
  - [TEAL Panic Behaviors](lib/include/kframework/avm/teal/teal-execution.md#panic-behaviors)
* [`teal-driver.md`](lib/include/kframework/avm/teal/teal-driver.md) defines the semantics of the various TEAL opcodes and specifies how a TEAL program is interpreted.

Not all TEAL opcodes are supported by the semantics as of yet. See the relevant [wiki page](https://github.com/runtimeverification/avm-semantics/wiki/TEAL-opcodes-support-and-costs) for the table of supported opcodes and their execution costs. The semantics does not yet support contract-to-contract calls.

#### Python packages

`kavm`[./kavm] is a Python package that enables interoperability between KAVM and `algod` &mdash; the Algorand node daemon. `kavm` also provides a drop-in replacement for `py-algorand-sdk`, making it possible to run existing deployment and testing scripts on top of KAVM.

`kavm` uses two auxiliary scripts located in [`lib/include/kframework/avm/scripts/`](lib/include/kframework/avm/scripts/):
* [`parse-avm-simulation.sh`](lib/include/kframework/avm/scripts/parse-avm-simulation.sh) calls `kparse` to parse a simulation scenario from a `.avm-simulation` file;
* [`parse-teal-programs.sh`](lib/include/kframework/avm/scripts/parse-teal-programs.sh) calls `kparse` to parse a `;`-separated list of TEAL source codes.


Working on KAVM
---------------

### Build system

* `make deps`: build K and other dependencies.
* `make build`: compile KAVM K modules and the `kavm` tool. By default, `kompile` is called with the LLVM backend. To compile the semantics with the Haskell backend, execute `K_BACKEND=haskell make build`.
* `make test -j8`: run tests. Adjust the `-jX` option as needed to run `X` tests in parallel.

When developing, make sure to activate the Python virtual environment build by KAVM with `. .build/venv/bin/activate` for the `kavm` script to be available. The Makefile activates the environment itself when necessary.

### Managing `PATH` with `direnv`

We use [`direnv`](https://direnv.net/) to manage the environment variables such as `PATH`, see [`.envrc`](.envrc).

After installing `direnv`, run `direnv allow` to activate the settings for the project's directory.

Feel free to ignore `direnv` if you prefer your global installation of K.

### Rule Coverage

This project contains facilities to generate coverage metrics for K rewrite rules that were executed by `kavm run`. This is helpful in ensuring that the test suite contains input programs that exercise all rewrite rules in the semantics.

To generate the coverage report for the AVM simulation scenarious squite ([`tests/scenarios/`](tests/scenarios/)), run the following command:

```bash
  make clean-coverage && make test-kavm-avm-simulation && make coverage
```

This command generates a `.build/coverage.xml` file. This file contains information about the K rewrite rules that have been exercised for all tests in the ([`tests/scenarios/`](tests/scenarios/)) directory.
