# AlgoML

AlgoML (*Algorand Modelling Language*) is a DSL for specifying Algorand smart contracts, which compiles into TEAL scripts.
AlgoML allows to specify stateful contracts in a declarative style; its compiler implements several static checks to rule out common programming errors in lower-level languages like TEAL.
We illustrate the expressiveness of AlgoML through a [series of use cases](#algoml-use-cases), including DeFi contracts and games.

AlgoML contracts have a global state, which can be updated through clauses of the form:
```java
@precondition1
...
@preconditionK
foo(x1,...,xn) {
  // state update
  ...
}
```
This clause defines a contract function ``foo`` which is enabled whenever all the preconditions are respected. Executing ``foo`` results in a state update, specified in the function body. Preconditions may have various forms: for instance, they can be predicates on the contract state, or checks that certain transactions belong to the group wherein the function is called.

On a lower level, an AlgoML program models two contracts: a stateful application, and a stateless contract account. The stateful application is in charge of all of the contract logic, while the stateless contract acts as an escrow, which holds funds and releases them according to the logic of the stateful contract.

Examples of AlgoML preconditions are:
```java 
@assert exp 
```
This precondition holds only when the boolean expression `exp` evaluates to true.

```java
@round (from,to)$curr_round
```
This precondition holds when the function is called from round `from` (included) to round `to` (excluded). The optional part `$curr_round` binds the variable `curr_round` to the actal round where the clause is executed.

```java
@newtok amt of $tok -> escrow
```
This precondition holds when a new token of `amt` units is minted, and all its units are stored in the contract. The variable `tok` is bound to the token identifier.

```java
@pay (min,max)$amt of tok : sender -> receiver
``` 
This precondition holds when a number of units of token `tok` in the range `(min,max)` are transferred from `sender` to `receiver`. The variable `amt` is bound to the actual amount of transferred units. The token `tok` can be ALGO or an ASA. The parameters `sender` and `receiver` can be arbitrary accounts, or the special accounts `caller` (the account which is calling the function) and `escrow` (the escrow which is handling the contract funds).

```java
@gstate oldstate -> newstate
```
This holds when the current contract state is `oldstate`. After executing the function, the state takes a transition to `newstate`.

We discuss the design of the AlgoML compiler in a [dedicated subpage](src).

## AlgoML by examples: tinybond

We illustrate some of the AlgoML features by applying it to implement a simple bond.
The contract issues bonds, in the form of ASAs, and allows users to redeem them with interests after a maturity date.
Users can buy bonds in two time periods:
* the standard sale period, where the bond value equals the amount of invested ALGOs (1 bond = 1 ALGO); 
* the presale period, where bonds are sold at a discounted price (1 bond = preSaleRate/100 ALGO).
After the maturity date, users can redeem bonds for ALGOs, at the exchange rate 1 bond = interestRate/100 ALGO.

The global state of the contract consists of the following variables. All of them are fixed at contract creation, with the only exception of `maxDep`, which is made mutable by the modifier `mut`:  
```java
glob token COUPON	// the ASA used to represent the bond
glob int interestRate   // interest rate (e.g., 150 means 1.5 multiplication factor, i.e. 50% interest rate)
glob int preSaleRate    // discount rate for the presale (e.g., 150 means that 100 ALGOs buy 150 bond units)
glob int preSale	// start of the presale period
glob int sale		// start of the sale period
glob int saleEnd	// end of the sale period
glob int maturityDate	// maturity date
glob mut int maxDep	// upper bound to ALGOs that can be deposited to preserve liquidity
```

Each account joining the contract has also a local state, composed by a single mutable variable:
```java
loc mut int preSaleAmt
```

Contract creation is modelled by the following clause:
```java
@newtok $budget of $COUPON -> escrow	// creates a new token
@assert preSale < sale 			// the presale period starts before the sale period
@assert sale < saleEnd 			// the sale period starts before it ends
@assert saleEnd < maturityDate		// the maturity date happens after the sale period has ended
Create tinybond(int preSale, int sale, int saleEnd, int maturityDate,int interestRate, int preSaleRate) {
	glob.preSale = preSale
	glob.sale = sale
	glob.saleEnd = saleEnd
	glob.maturityDate = maturityDate
	glob.interestRate = interestRate
	glob.preSaleRate = preSaleRate
	glob.COUPON = COUPON
	glob.maxDep = budget
}
```
The `Create` modifier means that the effect of the clause is to create and initialize the contract.
The `@newtok` precondition requires that the caller mints some units of a new token synchronously with the contract creation
(i.e., in the same atomic group of transactions where `tinybond` is called). 
The name `$COUPON` refers to the identifier of the new token, while `$budget` is the number of minted token units.
The `@assert` preconditions ensure that the presale period terminates before the sale period, and that the maturity date falls beyond the sale period.
The function body just initializes the variables in the global state with the actual parameters. 

The following clause allow investors join the presale. This operation does not require to meet any preconditions. The `OptIn` modifier enables these users to have a local state in the contract. The function body initializes the `preSaleAmt` variable of the local state to zero.
```java
OptIn joinPresale() {
	loc.preSaleAmt = 0
}
```

The following clause allows users to buy bonds in the presale period. The effect of the function is just to set the number of bought units in the 
local state of the investor. The actual transfer of tokens will be finalised in the sale period (see the next clause).
```java
@round (glob.preSale, glob.sale)		// presale period
@pay $amt of ALGO : caller -> escrow		// transfer ALGOs to the contract to reserve bond units
@assert amt * glob.preSaleRate / 100 <= glob.maxDep
deposit() {
	loc.preSaleAmt += amt * glob.preSaleRate / 100
	glob.maxDep -= amt * glob.preSaleRate / 100
}
```

The following clause allows users to buy bonds in the regular sale period. If the user has previously bought some units in the presale, they will receive the bought amount here. 
```java
@round (glob.sale, glob.saleEnd)		// sale period
@pay $inAmt of ALGO : caller -> escrow		// transfer additional ALGOs to the contract to buy bond units
@pay $outAmt of glob.COUPON : escrow -> caller	// transfer bond units from the contract to the caller
@assert inAmt + loc.preSaleAmt == outAmt	// outAmt is the actual number of transferred bond units
deposit() {
	loc.preSaleAmt = 0
}
```

After the maturity date has passed, users that bought bonds in the sale/presale period will be able to sell them at an interest rate of `glob.interestRate`/100. 
```java
@round (glob.maturityDate, )			
@pay $inAmt of glob.COUPON : caller -> escrow	// the caller transfer bond units to the contract...
@pay $outAmt of ALGO : escrow -> caller		// ... and redeems ALGOs with interests
@assert outAmt == inAmt * glob.interestRate / 100
redeem() {}
```

To compile the tinybond contract, follow the instructions in the [Using the AlgoML compiler](#using-the-algoml-compiler) section. For more information on how the contract is compiled, see the [How an AlgoML contract is compiled](/src/README.md) section.


## AlgoML use cases

Further AlgoML use cases are presented in the [contracts](contracts) folder:
- [Automated Market Makers](contracts/amm)
- [Blind auction](contracts/blind-auction)
- [Chain-based Ponzi scheme](contracts/chain-ponzi)
- [Crowdfunding](contracts/crowdfund)
- [Escrow](contracts/escrow)
- [King of the Algo Throne](contracts/kotat)
- [2-players lottery](contracts/lottery)
- [Morra game](contracts/morra)
- [Tinybond](contracts/tinybond)
- [Vaults](contracts/vaults)
- [Voting](contracts/voting)

## Building AlgoML

1\. Clone the AlgoML repository
```
git clone https://github.com/petitnau/algoml
```
2\. [Install opam](https://ocaml.org/docs/install.html#OPAM) 

3\. Install dune
```
opam install dune
```
4\. Install AlgoML dependencies
```
opam install . --deps-only
```
5\. Build the source
```
dune build
```
6\. Create AlgoML contracts! Syntax highlighting is supported on [vscode](https://marketplace.visualstudio.com/items?itemName=RobertoPettinau.algoml-lang) 


## Using the AlgoML compiler

To compile an AlgoML file into TEAL scripts, the following command can be used:
```console
dune exec ./amlc.exe /path/to/input.aml [-o outprefix]
```
The compiler will output three files in the folder where the command is launched:
* `output_approval.teal`, the TEAL code of the stateful contract;
* `output_escrow.teal`, the TEAL code of the stateless contract used as escrow;
* `output_clear.teal`, the TEAL code run upon a clearstate operation.

For example, to compile the tinybond contract, enter the following command from the algoml folder:
```console
dune exec ./amlc.exe contracts/tinybond/tinybond.aml
```

## Future developments

AlgoML is a work in progress towards safer programming of smart contracts in Algorand.
Possible future developments include:
* an executable formal specification of AlgoML semantics;
* more informative error messages from the AlgoML compiler;
* a type-safe mechanism for the commit-reveal pattern (now programmers must use low-level primitives like `sha256hash`, `get_int`, etc.)
* a client-side DSL to program the behaviour of users interacting with AlgoML contracts. Static cross-checks on the client and contract code could ensure that the client enjoys desirable behavioural properties, like e.g. deadlock-freedom and wealth preservation;
* a verification tool to check relevant properties of AlgoML contracts. For instance, we would like to ensure that a contract has always at least one enabled clause, that no assets are frozen forever, and so on;
* a proof of correctness of the AlgoML compiler, showing that all the possible executions of the TEAL code produced by the compiler are coherent with the behaviour of the source AlgoML specification.

## Disclaimer

The project is not audited and should not be used in a production environment.

## Credits

AlgoML has been designed by Roberto Pettinau and [Massimo Bartoletti](https://blockchain.unica.it/) from the University of Cagliari, Italy.
