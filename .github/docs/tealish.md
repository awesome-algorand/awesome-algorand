![Tealish, A readable language for Algorand, Powered by Tinyman](img/tealish_header.png)

<p align="center">
<img  src="https://visitor-badge.glitch.me/badge?page_id=tinymanorg.tealish&right_color=teal" />
<a href="https://github.com/tinymanorg/tealish/actions/workflows/tests.yml"><img src="https://github.com/tinymanorg/tealish/actions/workflows/tests.yml/badge.svg?branch=main" /></a>
<a href="https://tealish.readthedocs.io/en/latest/"><img src="https://img.shields.io/badge/Read-Docs-gold.svg" /></a>
</p>

---

Tealish is a readable language for the Algorand Virtual Machine. It enables developers to write TEAL in a procedural style optimized for readability.

Tealish transpiles to Teal rather than compiling directly to AVM bytecode. The produced Teal is as close to handwritten idiomatic Teal as possible.
The original source Tealish (including comments) is included as comments in the generated Teal.
The generated Teal is intended to be readable and auditable.
The generated Teal should not be surprising - the Tealish writer should be able to easily imagine the generated Teal.

Tealish is not a general purpose programming language. It is designed specifically for writing contracts for the AVM, optimizing for common patterns.

## Status
Tealish has been used to write large production contracts but it is not currently considered Production Ready for general use. It may have unexpected behavior outside of the scenarios it has been used for until now.

## Docs

https://tealish.readthedocs.io/

## Installation

`pip install tealish`

## Minimal Example
A simple example demonstrating assertions, state, if statements and inner transactions:

```python
#pragma version 6

if Txn.OnCompletion == UpdateApplication:
    assert(Txn.Sender == Global.CreatorAddress)
    exit(1)
end

assert(Txn.OnCompletion == NoOp)

int counter = app_global_get("counter")
counter = counter + 1
app_global_put("counter", counter)

if counter == 10:
    inner_txn:
        TypeEnum: Pay
        Receiver: Txn.Sender
        Amount: 10000000
    end
elif counter > 10:
    exit(0)
end

exit(1)
```

## Compiling

```
    tealish compile examples/minimal_example/counter_prize.tl
```
This will produce [`counter_prize.teal`](examples/minimal_example/build/counter_prize.teal) in the [`build`](examples/minimal_examplebuild/) subdirectory.

## Editor Support

A VS Code extension for syntax highlighting of Tealish & TEAL is available [here](https://www.dropbox.com/s/zn3swrfxkyyelpi/tealish-0.0.1.vsix?dl=0)


## Starter Template

```python
#pragma version 7

if Txn.ApplicationID == 0:
    # Create app
    exit(1)
end

switch Txn.OnCompletion:
    NoOp: main
    OptIn: opt_in
    CloseOut: close_out
    UpdateApplication: update_app
    DeleteApplication: delete_app
end

block opt_in:
    # Disallow Opt In
    exit(0)
end

block close_out:
    # Disallow Closing Out
    exit(0)
end

block update_app:
    # Only allow the Creator to update the app
    exit(Txn.Sender == Global.CreatorAddress)
end

block delete_app:
    # Only allow the Creator to delete the app
    exit(Txn.Sender == Global.CreatorAddress)
end

block main:
    switch Txn.ApplicationArgs[0]:
        "method_a": method_a
        "method_b": method_b
        "method_c": method_c
    end

    block method_a:
        # some statements here
        exit(1)
    end

    block method_b:
        # some statements here
        exit(1)
    end

    block method_c:
        # some statements here
        exit(1)
    end
end
```

## Design Goals
Tealish is designed first and foremost to be a more readable version of Teal.
The biggest difference between Teal and Tealish is the stack is made implicit in Tealish instead of being explicit as in Teal.

Readability is achieved by the following:
- Multiple operations on a single line
- Semantic names for scratch slots (variables)
- Aliases for values on stack
- Named constants
- High level language concepts (if/elif/else, loops, switches)
- A simple style convention

Safety Features:
- Readability
- Named scratch slots
- Scoped scratch slots
- Type checking

Any Teal opcode can be used in Tealish in a procedural style. Additionally there is syntactic sugar for some common operations.
When explicit stack manipulation is required raw Teal can be used inline within a Tealish program.

Tealish is a procedural language, executed from top to bottom. Statements can exist inside blocks or at the top level.
The first statement of a program is the entry point of the program. The program can exit on any line.
Execution can branch from one block to another using `jump` or `switch` statements.

Blocks are used to define scopes. Variables, Functions and Blocks are scoped to the block they are defined in and are available to any nested blocks.

Blocks are not functions:
- they do not take arguments
- they do not have independent stack space
- they are not re-entrant

Functions are used to define reusable pieces of functionality. They can take arguments and return values. They can read variables from the scope in which they are defined but they may not assign to variables outside their local scope. Functions may have side effects through the use of state manipulation or inner transactions.

