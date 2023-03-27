# Tealang

High-level language for Algorand Smart Contracts at Layer-1 and its low-level **TEAL v6** language.
The goal is to abstract the stack-based **Algorand Virtual Machine** and provide imperative Go/JS/Python-like syntax.

## Language Features

* Integer and bytes types

* Variables and constants
```
let var1 = 1
let var2 = 0x123
const myaddr = addr"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAY5HFKQ"
```

* All binary and unary operations from **TEAL**
```
let a = (1 + 2) / 3
let b = ~a
```

* Functions
```
inline function sample1(a) {
    return a - 1
}

function sample2(a) {
    return a + 1
}

function noop() void {
    return
}

function logic() {
    return sample1(2) + sample2(3)
}
```

* Condition statements and expressions
```
function condition(a) {
    let b = if a == 1 { 10 } else { 0 }

    if b == 0 {
        return a
    }
    return 1
}
```

* Loops
```
let y= 2;
for y>0 { y=y-1 }
```

* Type checking
```
function get_string() {
    return "\x32\x33\x34"
}

function logic() {
    let a = 1
    a = get_string()  // <- type check error
    return a
}
```

* Accounts state access
```
function approval() {
    let x = accounts[1].Balance
    return 1
}
```

* Globals and txn data access
```
function logic() {
    let s = global.GroupSize
    let idx = 1
    let a = gtxn[s-1].ApplicationArgs[idx+2];
    return a != "\x01"
}
```

* Modules
```
import stdlib.const
```

* Antlr-based parser
* [syntax highlighter](https://github.com/pzbitskiy/tealang-syntax-highlighter) for vscode.

## Language guide

Check the [language documentation](GUIDE.md)!

## Usage

* Tealang to bytecode
    ```sh
    tealang mycontract.tl -o mycontract.tok
    ```

* Tealang to TEAL
    ```sh
    tealang -c mycontract.tl -o mycontract.teal
    ```
* Tealang logic one-liner to bytecode
    ```sh
    tealang -l '(txn.Sender == "abc") && global.MinTxnFee > 2000' -o mycontract.tok
    ```
* stdin to stdout
    ```sh
    cat mycontract.tl | tealang -s -r - > mycontract.tok
    ```
* Dryrun / trace
    ```sh
    tealang -s -c -d '' examples/basic.tl
    ```

## Build from sources

### Prerequisites

1. Set up **ANTLR4**
    ```sh
    make antlr-install
    ```
    Refer to the [documentation](https://www.antlr.org/) in case of problems.
2. Install runtime for Go
    ```sh
    go get -u github.com/antlr/antlr4/runtime/Go/antlr
    ```
3. Install and setup **go-algorand**
    ```sh
    make algorand-install
    ```
    Check the [Algorand README](https://github.com/algorand/go-algorand/blob/master/README.md) for detailed build instructions if encounter any issues.

### Build and test
```sh
make && make test
```

### Optionally build and run Java AST visualizer
```sh
make java-gui ARGS=examples/basic.tl
```

## Roadmap

1. Constant folding.
2. Improve errors reporting.
3. Code gen: do not use temp scratch in "assign and use" case.
4. Code gen: keep track scratch slots and mark as available after freeing with `load`.
