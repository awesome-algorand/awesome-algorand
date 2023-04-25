> This resource is auto indexed by AwesomeAlgo, all credits to aqua-compiler, for more details refer to https://github.com/optio-labs/aqua-compiler

---

# Aqua-compiler

An expressive high level language for [the Algorand blockchain](https://en.wikipedia.org/wiki/Algorand) smart contracts that compiles to [TEAL](https://developer.algorand.org/docs/get-details/dapps/avm/teal/specification/) code.

This is a work in progress. Please report issues and help set the direction for this project.

## Using the Aqua command

Download the latest executable for your platform from [the releases page](https://github.com/optio-labs/aqua-compiler/releases).

Add the executable to your path. If you are on MacOS or Linux you should rename the executable from `aqua-mac` or `aqua-linux` to just be called `aqua` (so the rest of the instructions make sense).

You can also install Aqua using npm:

```bash
npm install -g aqua-compiler
```

## REPL

Running the executable with no arguments starts the REPL:

```bash
aqua
```

You can type Aqua expressions and statements at the REPL and see the TEAL code that is generated.

Trying entering expressions at the REPL prompt:

- `txn.Amount >= 1000;`
- `15 + txn.Amount >= 1000;`
- `txn.Amount <= arg[0];`
- `txn.Amount + arg[0] > 1000 && arg[1] > 30;`
- `txn.Receiver == addr ABC123;`
- `"a string" == txn.Something;`
- `return 1+2;`


## Compiling an Aqua file

To compile an Aqua file to TEAL code, input the Aqua filename:

```bash
aqua my-smart-contract.aqua
```

That prints the generated TEAL code to standard output.

Typically you'll want to capture the TEAL code to a file (so you can run it against the blockchain):

```bash
aqua my-smart-contact.aqua > my-smart-contract.teal
```

## Examples of Aqua code

See the `examples` subdirectory for various examples of Aqua code.

## Using the Aqua API

You can compile Aqua to TEAL code using Aqua's JavaScript/TypesScript API.

First install Aqua in your Node.js project:

```bash
npm install --save aqua-compiler
```

Then import Aqua's `compile` function:

```javascript
const { compile } = require("aqua-compiler");
```

Or in TypeScript:

```typescript
import { compile } from "aqua-compiler";
```

Now use `compile` to compile Aqua to TEAL:

```javascript
const aquaCode = "return 1 + 2;"
const tealCode = compiler(aquaCode);
console.log(tealCode);
```

## Testing Aqua code with Jest

One reason why you might want to use Aqua's API is to enable automated testing.

For example, here's a Jest test that compiles Aqua to TEAL:

```javascript
import { compile } from "aqua-compiler";
import { readFile } from "fs/promises";

describe("My smart contract test suite", () => {

    test("My first test", async () => {

        const tealCode = await compileAquaFile("my-smart-contract.aqua");

        // ... test that you can execute teal code against your sandbox blockchain ...
    });

    // ... other tests go here ...

});

//
// Loads and compiles an Aqua file.
//
async function compileAquaFile(fileName) {
    const fileContent = await readFile(join(tealPath, tealFileName), { encoding: "utf8" });
    return compile(fileContent);
}
```

After compiling an Aqua file to TEAL code you can then deploy that code against your sandbox Algorand blockchain.

Another way of testing that is faster and doesn't require having an actual Algorand node instance is to use [the TEAL interpreter](https://www.npmjs.com/package/teal-interpreter) to simulate the Algorand virtual machine.

A Jest test that runs Aqua code against the TEAL interpreter might look like this:

```javascript
import { compile } from "aqua-compiler";
import { readFile } from "fs/promises";
import { execute } from "teal-interpreter";

describe("My smart contract test suite", () => {

    test("My first test", async () => {

        const config = {
            // ... configure the initial state of the TEAL interpreter ...
        }
        const result = await executeAqua("my-smart-contract.aqua", config);

        // ... run expectations against the result to check that execution of the aqua code has expected results ...
        
    });

    // ... other tests go here ...

});

//
// Loads and compiles an Aqua file.
//
async function compileAquaFile(fileName) {
    const fileContent = await readFile(join(tealPath, tealFileName), { encoding: "utf8" });
    return compile(fileContent);
}

//
// Executes Aqua code against the TEAL interpreter.
//
async function executeAqua(fileName, config) {
    const tealCode = await compileAquaFile(fileName);
    return await execute(tealCode, config);
}
````



## Development

See [the development guide](docs/DEVELOPMENT.md) for instructions on development of Aqua.