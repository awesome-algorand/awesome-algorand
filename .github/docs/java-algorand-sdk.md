# java-algorand-sdk

[![Build Status](https://travis-ci.com/algorand/java-algorand-sdk.svg?branch=master)](https://travis-ci.com/algorand/java-algorand-sdk?branch=master)
[![Maven Central](https://maven-badges.herokuapp.com/maven-central/com.algorand/algosdk/badge.svg)](https://maven-badges.herokuapp.com/maven-central/com.algorand/algosdk/)

AlgoSDK is a Java library for communicating and interacting with the Algorand network. It contains a REST client for accessing `algod` instances over the web,
and also exposes functionality for generating keypairs, mnemonics, creating transactions, signing transactions, and serializing data across the network.


# Prerequisites

Java 7+ and Android `minSdkVersion` 16+

# Installation

Maven:

```xml
<dependency>
    <groupId>com.algorand</groupId>
    <artifactId>algosdk</artifactId>
    <version>2.0.0</version>
</dependency>
```

# Quickstart

This program connects to a running [sandbox](https://github.com/algorand/sandbox) private network, creates a payment transaction between two of the accounts, signs it with kmd, and reads result from Indexer.
```java
import com.algorand.algosdk.account.Account;
import com.algorand.algosdk.crypto.Address;
import com.algorand.algosdk.kmd.client.ApiException;
import com.algorand.algosdk.kmd.client.KmdClient;
import com.algorand.algosdk.kmd.client.api.KmdApi;
import com.algorand.algosdk.kmd.client.model.*;
import com.algorand.algosdk.transaction.SignedTransaction;
import com.algorand.algosdk.transaction.Transaction;
import com.algorand.algosdk.util.Encoder;
import com.algorand.algosdk.v2.client.common.AlgodClient;
import com.algorand.algosdk.v2.client.common.IndexerClient;
import com.algorand.algosdk.v2.client.common.Response;
import com.algorand.algosdk.v2.client.model.PendingTransactionResponse;
import com.algorand.algosdk.v2.client.model.PostTransactionsResponse;
import com.algorand.algosdk.v2.client.model.TransactionsResponse;

import java.io.IOException;
import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main {
    private static String token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
    private static KmdApi kmd = null;

    public static void main(String[] args) throws Exception {
        // Initialize algod/indexer v2 clients.
        AlgodClient algod = new AlgodClient("http://localhost", 4001, token);
        IndexerClient indexer = new IndexerClient("http://localhost", 8980);

        // Initialize KMD v1 client
        KmdClient kmdClient = new KmdClient();
        kmdClient.setBasePath("http://localhost:4002");
        kmdClient.setApiKey(token);
        kmd = new KmdApi(kmdClient);

        // Get accounts from sandbox.
        String walletHandle = getDefaultWalletHandle();
        List<Address> accounts  = getWalletAccounts(walletHandle);

        // Create a payment transaction
        Transaction tx1 = Transaction.PaymentTransactionBuilder()
                .lookupParams(algod) // lookup fee, firstValid, lastValid
                .sender(accounts.get(0))
                .receiver(accounts.get(1))
                .amount(1000000)
                .noteUTF8("test transaction!")
                .build();

        // Sign with KMD
        SignedTransaction stx1a = signTransactionWithKMD(tx1, walletHandle);
        byte[] stx1aBytes = Encoder.encodeToMsgPack(stx1a);

        // Sign with private key
        byte[] privateKey = lookupPrivateKey(accounts.get(0), walletHandle);
        Account account = new Account(privateKey);
        SignedTransaction stx1b = account.signTransaction(tx1);
        byte[] stx1bBytes = Encoder.encodeToMsgPack(stx1b);

        // KMD and signing directly should both be the same.
        if (!Arrays.equals(stx1aBytes, stx1bBytes)) {
            throw new RuntimeException("KMD disagrees with the manual signature!");
        }

        // Send transaction
        Response<PostTransactionsResponse> post = algod.RawTransaction().rawtxn(stx1aBytes).execute();
        if (!post.isSuccessful()) {
            throw new RuntimeException("Failed to post transaction");
        }

        // Wait for confirmation
        boolean done = false;
        while (!done) {
            Response<PendingTransactionResponse> txInfo = algod.PendingTransactionInformation(post.body().txId).execute();
            if (!txInfo.isSuccessful()) {
                throw new RuntimeException("Failed to check on tx progress");
            }
            if (txInfo.body().confirmedRound != null) {
                done = true;
            }
        }

        // Wait for indexer to index the round.
        Thread.sleep(5000);

        // Query indexer for the transaction
        Response<TransactionsResponse> transactions = indexer.searchForTransactions()
                .txid(post.body().txId)
                .execute();

        if (!transactions.isSuccessful()) {
            throw new RuntimeException("Failed to lookup transaction");
        }

        System.out.println("Transaction received! \n" + transactions.toString());
    }

    public static SignedTransaction signTransactionWithKMD(Transaction tx, String walletHandle) throws IOException, ApiException {
        SignTransactionRequest req = new SignTransactionRequest();
        req.transaction(Encoder.encodeToMsgPack(tx));
        req.setWalletHandleToken(walletHandle);
        req.setWalletPassword("");
        byte[] stxBytes = kmd.signTransaction(req).getSignedTransaction();
        return Encoder.decodeFromMsgPack(stxBytes, SignedTransaction.class);
    }

    public static byte[] lookupPrivateKey(Address addr, String walletHandle) throws ApiException {
        ExportKeyRequest req = new ExportKeyRequest();
        req.setAddress(addr.toString());
        req.setWalletHandleToken(walletHandle);
        req.setWalletPassword("");
        return kmd.exportKey(req).getPrivateKey();
    }

    public static String getDefaultWalletHandle() throws ApiException {
        for (APIV1Wallet w : kmd.listWallets().getWallets()) {
            if (w.getName().equals("unencrypted-default-wallet")) {
                InitWalletHandleTokenRequest tokenreq = new InitWalletHandleTokenRequest();
                tokenreq.setWalletId(w.getId());
                tokenreq.setWalletPassword("");
                return kmd.initWalletHandleToken(tokenreq).getWalletHandleToken();
            }
        }
        throw new RuntimeException("Default wallet not found.");
    }

    public static List<Address> getWalletAccounts(String walletHandle) throws ApiException, NoSuchAlgorithmException {
        List<Address> accounts = new ArrayList<>();

        ListKeysRequest keysRequest = new ListKeysRequest();
        keysRequest.setWalletHandleToken(walletHandle);
        for (String addr : kmd.listKeysInWallet(keysRequest).getAddresses()) {
            accounts.add(new Address(addr));
        }

        return accounts;
    }
}
```

# Documentation

Javadoc can be found at [https://algorand.github.io/java-algorand-sdk](https://algorand.github.io/java-algorand-sdk). <br />
Additional resources and code samples are located at [https://developer.algorand.org](https://developer.algorand.org).

# Cryptography

AlgoSDK depends on `org.bouncycastle:bcprov-jdk15on:1.61` for `Ed25519` signatures, `sha512/256` digests, and deserializing `X.509`-encoded `Ed25519` private keys.
The latter is the only explicit dependency on an external crypto library - all other references are abstracted through the JCA.

# Java 9+

When using cryptographic functionality, and Java9+, you may run into the following warning:
```
WARNING: Illegal reflective access by org.bouncycastle.jcajce.provider.drbg.DRBG
```
This is known behavior, caused by more restrictive language features in Java 9+, that Bouncy Castle has yet to support. This warning can be suppressed safely. We will monitor
cryptographic packages for updates or alternative implementations.

# Contributing to this Project

## build

This project uses Maven.

### **To build**
```
~$ mvn package
```

**To run the example project**
Use the following command in the examples directory, be sure to update your algod network address and the API token
parameters (see examples/README for more information):
```
~$ mvn exec:java -Dexec.mainClass="com.algorand.algosdk.example.Main" -Dexec.args="127.0.0.1:8080 ***X-Algo-API-Token***"
```

### **To test**
We are using separate version targets for production and testing to allow using JUnit5 for tests. Some IDEs, like IDEA
do not support this very well. To workaround the issue a special `ide` profile should be enabled if your IDE does not
support mixed `target` and `testTarget` versions. Regardless of IDE support, the tests can be run from the command line.
In this case `clean` is used in case an incremental build was made by the IDE with Java8.
```
~$ mvn clean test
```

There is also a special integration test environment, and shared tests. To run these use the Makefile:
```
~$ make docker-test
```

To stand up the test harness, without running the entire test suite use the Makefile:
```
~$ make harness
```
You can then run specific cucumber-based unit and integration tests directly.


## deploying artifacts

The generated pom file provides maven compatibility and deploy capabilities.
```
mvn clean install
mvn clean deploy -P github,default
mvn clean site -P github,default  # for javadoc
mvn clean deploy -P release,default
```

# Testing

Many cross-SDK tests are defined in [algorand-sdk-testing](https://github.com/algorand/algorand-sdk-testing/). Some are integration tests with additional dependencies. These dependencies are containerized in a docker file, which can be executed with `make docker-test`.

It is occasionally useful to run locally, or against alternate integration branches. To do this:
1. Install feature files for your test branch "./run_integration_tests.sh -feature-only -test-branch <branch here>"
2. Run locally with `make integration` and `make unit`, or from the IDE by running "RunCucumberUnitTest.java"

# Android Support

Significant work has been taken to ensure Android compatibility (in particular for `minSdkVersion` 16). Note that the
default crypto provider on Android does not provide `ed25519` signatures, so you will need to provide your own (e.g. `BouncyCastle`).

# Algod V2 and Indexer Code Generation
The classes `com.algorand.algosdk.v2.client.algod.\*`, `com.algorand.algosdk.v2.client.indexer.\*`, `com.algorand.algosdk.v2.client.common.AlgodClient`, and `com.algorand.algosdk.v2.client.common.IndexerClient` are generated from OpenAPI specifications in: `algod.oas2.json` and `indexer.oas2.json`.

The specification files can be obtained from:
- [algod.oas2.json](https://github.com/algorand/go-algorand/blob/master/daemon/algod/api/algod.oas2.json)
- [indexer.oas2.json](https://github.com/algorand/indexer/blob/master/api/indexer.oas2.json)

A testing framework can also be generated with: `com.algorand.sdkutils.RunQueryMapperGenerator` and the tests run from `com.algorand.sdkutils.RunAlgodV2Tests` and `com.algorand.sdkutils.RunIndexerTests`

## Regenerate the Client Code

The actual generation is done using the `generate_java.sh` script in the [generator](https://github.com/algorand/generator/) repo.

# Updating the `kmd` REST client
The `kmd` REST client has not been upgraded to use the new code generation, it is still largely autogenerated by `swagger-codegen`. [https://github.com/swagger-api/swagger-codegen]

To regenerate the clients, first, check out the latest `swagger-codegen` from the github repo. (In particular, the Homebrew version
is out of date and fails to handle raw byte arrays properly). Note OpenAPI 2.0 doesn't support unsigned types. Luckily we don't have any
uint32 types in algod, so we can do a lossless type-mapping fromt uint64->int64 (Long) -> BigInteger:

```
curl http://localhost:8080/swagger.json | sed -e 's/uint32/int64/g' > temp.json
swagger-codegen generate -i temp.json -l java -c config.json
```

`config.json` looks like:
```json
{
  "library": "okhttp-gson",
  "java8": false,
  "hideGenerationTimestamp": true,
  "serializableModel": false,
  "supportJava6": true,
  "invokerPackage": "com.algorand.algosdk.{kmd or algod}.client",
  "apiPackage": "com.algorand.algosdk.{kmd or algod}.client.api",
  "modelPackage": "com.algorand.algosdk.{kmd or algod}.client.model"
}
```

Make sure you convert all `uint32` types to `Long` types.

The generated code (as of April 2019) has one circular dependency involving
`client.Pair`. The `client` package depends on `client.auth`, but `client.auth`
uses `client.Pair` which is in the `client` package. One more problem is that
`uint64` is not a valid format in OpenAPI 2.0; however, we need to send large
integers to the `algod` API (`kmd` is fine). To resolve this, we do the
following manual pass on generated code:

- Move `Pair.java` into the `client.lib` package
- Find-and-replace `Integer` with `BigInteger` (for uint64), `Long` (for uint32), etc. in `com.algorand.algosdk.algod` and subpackages (unnecessary for algod)
- Run an `Optimize Imports` operation on generated code, to minimize dependencies.

Note that msgpack-java is good at using the minimal representation.
