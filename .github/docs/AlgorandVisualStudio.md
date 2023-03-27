# **Algorand for Visual Studio**

A warm welcome to Algorand for Visual Studio!

This is a set of extensions to Microsoft's flagship developer tool, Visual Studio 2022, produced with the aim of making development on Algorand a simple, intuitive, familiar experience.

Professional software engineers from a range of backgrounds, such as C# game developers, line-of-business systems consultants will now be able to create Algorand applications easily using tools they are familiar with.

On this page you will find **[getting started](#getting-started)** instructions for developers, details on the functional areas and **[capabilities](#capabilities)** , and the **[project roadmap](#roadmap)**.

The current version is an Alpha release aimed at garnering feedback, bugs, requirements and any other modifications to general direction.  Do expect bugs, breaking changes, and shifts in direction. 

*DISCLAIMER: DO NOT USE THIS VERSION FOR PRODUCTION CODE. WE ARE NOT LIABLE FOR ANYTHING.*

## USING THE TEMPLATES

After creating a project using a template here, please **Update Nuget Packages** and then **Unload and Reload the project in VS**.

## UPDATE (February 2023)

The latest version at 1.6 now includes the following changes. 
- Smart Signatures and re-use of the ABI routing pattern in smart signatures to set arguments and determine which TEAL method is executed.
- Complex types for read access. It is now possible to send structs using ABIStruct decorators and read them in the smart contract or signature.
- More array types for read access. Previously byte arrays were the only supported array type. Now other array types are supported while currently the other array types are read only. 
- App.json and ARC4 support remains partially compatible, though the roadmap is updated.

## UPDATE (November 2022)

The latest version at 1.4 now includes the following changes. Documentation will be updated shortly to reflect the below.
- A new template allowing direct use of the Sandbox without having to manipulate private keys. Just create the project, start the sandbox and it's ready to go.
- Support for floating point decimal. The ``decimal``type can now be used. (The generated TEAL is quite expensive.) Conversion from integer types are permitted and conversion from decimal to ulong.
- Integer ``Pow`` and ``Sqrt`` are now added.
- IDE support for generating smart contract *references* for contract to contract calls.
- Support for accessing contract state through contract *references*.
- A prototype version of a new ``App.json`` is available, where export to and code generation of proxies/references from a json representation of the app is now supported by the IDE. This ``app.json`` format is under development and will eventually work fully with the Beaker project.

## Documentation Structure

- Contract Development
    - [Contracts as Classes](./ContractDevelopment/ContractsAsClasses.md)
    - [C# Guidelines](./ContractDevelopment/CSharpGuidelines.md)
    - [Predefined methods and properties](./ContractDevelopment/PredefinedFunctions.md)
    - [Deployment](./ContractDevelopment/Deployment.md)
    - [Smart Contracts](./ContractDevelopment/SmartContracts.md)
    - [Smart Signatures](./ContractDevelopment/SmartSignatures.md)
- IDE
    - [IDE Support](./IDE/IDE.md)
- Optimisers
    - [Optimisers and Framework](./Optimisers/Optimisers.md)
- Transactions
    - [Contract to Contract Calls](./Transactions/ContractToContract.md)
    - [Inner Transactions](./Transactions/InnerTransactions.md)
    - [Entity References](./Transactions/TransactionReferences.md)
- Project Templates
    - [Console Template](./ProjectTemplates/Console.md)
    - [MAUI Template](./ProjectTemplates/MAUI.md)
    - [Web Template](./ProjectTemplates/Web.md)
    - [Console for Sandbox](./ProjectTemplates/ConsoleForSandbox.md)
    - [Smart Signature](./ProjectTemplates/ConsoleSmartSignature.md)





## **Getting Started**

### Installing the VSIX Visual Studio Extension

From within Visual Studio 2022, click Extensions -> Manage Extensions

![image](https://user-images.githubusercontent.com/33515470/160580048-8b42952d-b10b-4d35-bc83-d467c025048d.png)

Type in Algorand for VS into the search bar to find the VSIX Visual Studio extension. 

![image](https://user-images.githubusercontent.com/33515470/160686148-9f94d448-0d5f-43b5-92f1-556c22172860.png)

Select the Algorand for VS extension, and click Download to install.

You will most likely be prompted to restart VS to get the extension installed:

![image](https://user-images.githubusercontent.com/33515470/160686465-f563e962-3ca1-41bf-95ca-aa4ea785e190.png)

After closing, you will be prompted to modify with the current preview extension:

![image](https://user-images.githubusercontent.com/33515470/160686748-8e5edd4d-6d96-4ed1-9f5e-c88dab6819f8.png)

An updating progress bar might take a while:


![image](https://user-images.githubusercontent.com/33515470/160686888-0f758aee-7cf2-453e-89ce-7f7338d99d2e.png)



Party time, close the following then open VS again.

![image](https://user-images.githubusercontent.com/33515470/160687019-ec247410-3224-49b5-a74b-d366837ed005.png)

### Your first .NET project for Algorand

The easiest way to start is by using a Visual Studio project template. All the following templates assume you have access to an Algorand node. There are a number of ways of getting a node, such as using a service like PureStake. Our preferred approach is to develop with a local Algorand sandbox. To install a local sandbox please follow the guidance [here](https://github.com/algorand/sandbox) .

#### Using the sandbox accounts
The sandbox automatically generates three pre-funded accounts for you. For the following templates you will need to identify these accounts and then get the mnemonic representation of the private key.

From the terminal execute the following command to get the accounts:

         ./sandbox goal account list

For each one of the listed accounts execute this command to view the mnemonic:

         ./sandbox goal account export -a <address from above list>

Make a copy of the mnemonics for later use in the templates.

![image](https://user-images.githubusercontent.com/33515470/191034404-4d32d857-ccee-4603-aa6c-6642867fccbc.png)

#### Using the sandbox accounts automatically

If you want a project that just works out of the box with a local Sandbox, without
the flexibility of editing account mnemonics, please use the Console Application for Sandbox.

This uses KMD in the Sandbox node to use the predefined developer Account automatically.

#### Using a testnet account

For a shortcut if Sandbox isn't yet installed and you need to get up and running quicker, Algorand
has provided training nodes on Testnet. You can use this in the following way:

1. Get a TestNet account at myalgo.com 
![image](https://user-images.githubusercontent.com/33515470/221985989-6aa1f833-1757-416e-862d-b228cf7b6366.png)

2. Copy off the Account address and fund it at the [dispenser](https://dispenser.testnet.aws.algodev.network/)
3. Change the boilerplate code to use the following Testnet node and token:
``var httpClient = HttpClientConfigurator.ConfigureHttpClient(@"https://academy-algod.dev.aws.algodev.network/", "2f3203f21e738a1de6110eba6984f9d03e5a95d7a577b34616854064cf2c0e7b ");``

#### Using the templates

The current version includes three main types of project:

- MAUI Solution with Smart Contracts
- Web Application with Smart Contracts
- Console Application with Smart Contracts
- Console Application for Sandbox with Smart Contracts
- Console Application for Smart Signatures

All the projects include boilerplate for connecting to Algorand nodes.

The console and web applications include various examples of smart contract usage. The MAUI solution includes two sub-templates, one a native client and guidance on how to connect and deploy smart contracts, and the other a reverse proxy to prevent Algorand node access tokens being stored in the native client.

Please follow the guidance in each of the links below to continue:

- [Maui](./ProjectTemplates/MAUI.md)
- [Web](./ProjectTemplates/Web.md)
- [Console](./ProjectTemplates/Console.md)
- [Console for Sandbox](./ProjectTemplates/ConsoleForSandbox.md)
- [Smart Signature](./ProjectTemplates/ConsoleSmartSignature.md)





## **Capabilities**

### C# Compiler

**[For guidance on basic Smart Contract development please click here](./ContractDevelopment/SmartContracts.md)**

Once the extension is installed, you will have access to project templates with a Code Analyzer ("Algorand for Visual Studio") and a shared library ("Algorand for Visual Studio.Core"). The shared library offers some base classes, one of which is called SmartContract.

Any classes that inherit from SmartContract will be the subject of Code Analysis. The Code Analyzer permits a subset of the C# language and .NET framework to be used. It also places some expectations on structure, such as limiting scratch variables to local variables, and modifies byte arrays to be value types.

The Code Analyzer first checks if the basic C# is without error. If there are no diagnostic errors in the underlying C# then it continues with a check for conformity to Algorand Smart Contract compilation expectations. Any additional errors, such as use of unsupported types or misplaced scratch variables, are added to the diagnostics output. Finally, if there are no errors, the C# is compiled to TEAL.

The TEAL is output into a class that implements the ICompiledContract interface. This contains metadata about the application, such as the number of global and local ulongs/byte slices, and the code for the Approval and ClearState programs. 

The template projects are integrated with the Algorand2 .NET SDK. A Utility class is included in the template projects that recognises ICompiledContract and allows Deploy, Compile and Execute to be called. 



### ABI and Smart Contracts as Classes

**[For details on ABI methods and contracts-as-classes please click here](./ContractDevelopment/ContractsAsClasses.md)**

Algorand for Visual Studio supports client to contract calling and contract to contract calling, with some support for Algorand ABI. 

At the moment the compatibility with ARC-4 is limited. Further compatibility with other tools like Beaker may be added incrementally in the future.

This is an example of a smart contract using ABI methods and state:

```csharp
namespace Algorand for Visual Studio.Test.TestContracts 
{
    public class AppCallScenarioTests : SmartContract    
    {
        [Storage(StorageType.Global)]
        public int CallCounter; 
        
        protected override int ApprovalProgram() 
        {
            //NOTE: "pre-" code can be invoked here before the ABI method selector.
            CallCounter++;

            //handle "ABI" methods or exit cleanly (eg: on App Create).
            InvokeSmartContractMethod();

            //NOTE: "post" code can be invoked but compiler must warn on any Log invocation

            return 1;
        }

        [SmartContractMethod(OnCompleteType.NoOp, "Ret10" )]
        public int ReturnTheInteger10()
        {
            return 10;
        }

        [SmartContractMethod(OnCompleteType.NoOp, "RetTx1")]
        public byte[] ReturnSomeTxInfo(in TransactionReference tx, in SugarSupplierContract contractRef)
        {
            return tx.Note;
        }

        protected override int ClearStateProgram()
        {
            return 1;
        }
    }   
}

```

### ABI and Smart Signatures as Classes

Smart Signatures are authored like this and applied to Transactions using their proxy equivalents, called "Signers" or "Generators."

```csharp
     internal class BasicSignature : SmartSignature
    {
        public override int Program()
        {
            InvokeSmartSignatureMethod();
            return 0; //fail if no smart signature method found
        }

        [SmartSignatureMethod("Auth")]
        public int AuthorisePaymentWithNote(PaymentTransactionReference ptr, bool allowEmptyNote, decimal x)
        {
            if (x < 10.0M) return 0;
            if (ptr.RekeyTo != ZeroAddress) return 0;
            if (ptr.CloseRemainderTo != ZeroAddress) return 0;

            string txTypeCheck = "pay";
            if (ptr.TxType != txTypeCheck.ToByteArray()) return 0;

            byte[] note = ptr.Note;
            if (!allowEmptyNote && note.Length == 0) return 0;

            return 1;
        }
    }
```

**[Please click here for details on Smart Signatures](./ProjectTemplates/ConsoleSmartSignature.md).**


### Inner Transactions

Algorand for Visual Studio  supports being able to invoke arbitrary transactions from within a Smart Contract. 

Because of the way TEAL handles grouped inner transactions, the C# compiler has to enforce special restrictions on how these are used. 

**[Please click here for details on Inner Transactions](./Transactions/InnerTransactions.md).**

### Contract to Contract Calls

While Inner Transaction application call transactions can be constructed to call another Smart Contract from within a Smart Contract, this is not the most convenient way of implementing contract to contract calls. 

The ABI support allows references to be constructed as ```SmartContractReference``` classes. These can then be used to invoke the ABI methods on another smart contract, in a contract-as-class style.

**[For click here for guidance on Contract to Contract calls](./Transactions/ContractToContract.md).**

### IDE Support

This version of Algorand for Visual Studio introduces various IDE extensions to help with code generation and smart contract authoring.

IDE support remains on the roadmap too as the ARC4 and Application spec matures.

**[Please click here to see the IDE guidance](./IDE/IDE.md).**


### Optimisers and Optimisation Framework

**[Please see Optimisers](./Optimisers/Optimisers.md)** for details on including the default optimisers into your project and how to extend and add your own.

This version adds a framework for including optimisers into your project. 

It also includes a small number of default optimisers using the peep-hole technique that deal with byte array initialisation program size cost.



### Realtime code analysis

As code is edited, SmartContract classes are analysed for conformity to the expectations of the TEAL compiler, which operates on a subset of C#. For example, in the following SmartContract, a field is declared that is neither Local storage nor Global. It is handled by the compiler as a scratch variable, but a warning is generated that, different to normal C# compilation, the ClearStateProgram will not be able to see values put into that field by the ApprovalProgram or vice versa:

![image](https://user-images.githubusercontent.com/33515470/160593405-d93930a7-3be0-4c12-99e2-fe16788e6fbf.png)


If there are base C# errors, the compiler and analyzer will avoid the remainder of that smart contract. 

This is recognisable by error E002 as below:


![image](https://user-images.githubusercontent.com/33515470/160665059-5f67c8cd-5195-4327-a114-2f8d60f194a5.png)



### Realtime compilation

As code is edited, each SmartContract class is compiled to produce an ICompiledContract. The namespaces are (currently) the source file name and source class name. 

To view the actual code, navigate to the Analyzers section of the project like this:

![image](https://user-images.githubusercontent.com/33515470/160593899-2be8537e-ece2-4be8-b760-674fa676f8ef.png)

Expand the Algorand for Visual Studio section and scroll down past the list of Diagnostics:

![image](https://user-images.githubusercontent.com/33515470/160594032-13e18961-c209-425f-a2c8-be89923e7ed5.png)

Expand the folder Algorand for Visual Studio.SourceGenerator.TealGenerator to view the generated contracts:

![image](https://user-images.githubusercontent.com/33515470/160594170-34fe3ff5-75c8-47db-a6f5-8e2a66b60c47.png)

Opening one example:

![image](https://user-images.githubusercontent.com/33515470/160594262-c4e86de3-525e-451a-ad0f-4d6855a4eb30.png)

ConditionalLogic1 was a SmartContract class in the file ConditionalLogic. This approach to naming the outputs should most likely change in future versions, with perhaps some configurability.


### Templates

Project templates are included, offering skeleton architectures and educational code to get up and running quickly. 



## **Roadmap**

If you want to know what's coming up or why some C# construct does not yet seem to be available, this section attempts to provide answers. Here you will find the project 'roadmap', but *without* a timeline - it is expected that priorities will shift depending on feedback. If you DO have feedback, please add an Issue into this repo. Any kind of feedback is fine, whether it be a suggestion, a bug, a discussion, feel free to relay what you want.

### IDE Add Optimisers function

Optimisers must be included by manually copying a DLL to the right place at
the moment. The IDE will be extended to include an Add Optimisers function
and will allow optimisers to be selected from a list.

### Closer ABI support and Application spec files.

Right now a variation of the ARC-4 is used to encode ABI arguments and send
them to Smart Contracts. 

This was done as a way of facilitating updates to complex types and arrays. 

It is possible that in the future the AVM will support complex types natively somehow,
perhaps through the use of opcodes or encoding/decoding mechanisms to an
agreed runtime type format.

The App.json export is also specific to the C# tooling, though it is an approximation
of the ARC32 proposal, which is still in very early days.

As this area matures the encoding and support will improve.

It is expected that new functions will be needed to allow C# contract developers
to connect to an ARC4 ABI spec based on Contract.json. This kind of functionality
can be added incrementally.

### App.json type exports

Right now when producing an App.json, any custom ``ABIStruct`` types are left as 
C# types and omitted from the json. ARC32, even though it is early, proposes a format
for defining and referencing types. App.json can be made to include new types based on the 
C# type definitions and exported for 3rd party use.

This kind of functionality will be added incrementally along with the closer ABI/App spec work.

### Array and complex type updates

A lot of time was spent recently settling on a direction for the encoding, so for now 
the tooling only allows read operations on complex types and array, apart from byte arrays which can be read/written.

Update functionality will be added later, as the encoding now makes it easy for this to achieve.

### Box storage

This will be added in the near future as a State type for complex/simple types.

### Scratch Variables

Scratch variables can be accessed in the current contract, but there is no mechanism yet of referencing scratch variables in a SmartContractReference for a grouped transaction. In future those reference classes will contain fields that represent exposed Scratch Variable positions.

### State management

*App_local_del* and *app_global_del* are not yet supported, but will be!


### C#

Some constructs are not supported yet.

Declaration of a Smart Contract as a nested class is not yet available.

.NET Collections will be gradually introduced.

Fixed point arithmetic.

Multidimensional and jagged arrays?

Unary operators on array accessors, eg:

```csharp
myArray[0]++;
```

### Additional Optimisers

New optimisers will be added over time, as part of this project or if supplied by the community.

### Debugger

A complete debugger for TEAL will be offered.

### Formal Analysis

C# Code Analyzers allow existing formal analytical tools to work over C# syntax programs. For example, C# PEX or IntelliTest allows automatic test case generation. We will aim for C# semantic equivalence with the TEAL output so that existing tools can be applied. Later we will add new tools that check for Smart Contract security specific cases and in real time issue diagnostic warnings.

### VS for Mac

VS for Mac support can be added. VS 2022 for Mac has been rewritten and extension support is not well documented but should be possible.

