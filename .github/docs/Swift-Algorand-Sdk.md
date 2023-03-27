# Swift Algorand SDK

This is a swift sdk that allows interaction with the algorand blockchain. It also supports interecting with the V2 indexer and Algo Apis

## 1 How To Install
In Xcode go to File > Swift Packages > Add Package Dependency and paste the git url of this package, make sure to choose the `main` branch and proceed


## 2 Quickstart
The swift algorand sdk currently only supports Algod and Indexer 2.0, the only thing you need to do to start using the swift-algorand-sdk after installing it in your project is to import it like below:
```swift
import swift_algorand_sdk
```
Let's try some code
```swift
var ALGOD_API_ADDR="ALGOD-API-ADDRESS";
var ALGOD_API_TOKEN="ALGOD-API-TOKEN";
var ALGOD_API_PORT="ALGOD-API-PORT"
var algodClient=AlgodClient(host: ALGOD_API_ADDR, port: ALGOD_API_PORT, token: ALGOD_API_TOKEN)
 algodClient.getStatus().execute(){nodeStatusResponse in
        if(nodeStatusResponse.isSuccessful){
            print(nodeStatusResponse.data!.lastRound)
        }else{
            print(nodeStatusResponse.errorDescription)
        }
    
    }

    algodClient.transactionParams().execute(){ paramResponse in
    if(paramResponse.isSuccessful){
        print(paramResponse.data!.lastRound)
    }else{
        print(paramResponse.errorDescription);
    }
}
```
Please do note that you can always change the APi key for the Header of either Algod or Indexer requests, for example, someone using purestake will simply add the line below to the line after initializing `AlgodClient`
```swift
algodClient.set(key: "X-API-Key")
```

Lets try a complete example of a payment transaction with purestake
```swift
var PURESTAKE_ALGOD_API_TESTNET_ADDRESS="https://testnet-algorand.api.purestake.io/ps2";
var PURESTAKE_API_KEY="YOUR-PURESTAKE-API-KEY";
var PURESTAKE_API_PORT="443";
var algodClient=AlgodClient(host: PURESTAKE_ALGOD_API_TESTNET_ADDRESS, port: PURESTAKE_API_PORT, token: PURESTAKE_API_KEY)

var mnemonic="cactus check vocal shuffle remember regret vanish spice problem property diesel success easily napkin deposit gesture forum bag talent mechanic reunion enroll buddy about attract"

 var account =  try Account(mnemonic)
    var senderAddress = account.getAddress()
    var receiverAddress = try! Address("FMBQKMGDE7LYNDHCSUPJBXNMMT3HC2TXMIFAJKGBYJQDZN4R3M554N4QTY")


        var trans =  algodClient.transactionParams().execute(){ paramResponse in
            if(!(paramResponse.isSuccessful)){
            print(paramResponse.errorDescription);
            return;
        }

    var tx = try! Transaction.paymentTransactionBuilder().setSender(senderAddress)
                .amount(10)
                .receiver(receiverAddress)
               .note("Swift Algo sdk is cool".bytes)
                .suggestedParams(params: paramResponse.data!)
                .build()

           
            var signedTransaction=account.signTransaction(tx: tx)
        
            var encodedTrans:[Int8]=CustomEncoder.encodeToMsgPack(signedTransaction)
           


            algodClient.rawTransaction().rawtxn(rawtaxn: encodedTrans).execute(){
               response in
                if(response.isSuccessful){
                    print(response.data!.txId)
                }else{
                    print(response.errorDescription)
                    print("Failed")
                }

            }
    }
```
you can further query the pending transaction by doing the below
```swift


algodClient.pendingTransactionInformation(txId: "PENDING-TRANSACTION-ID").execute(){ pendingTransactionResponse in
        if(pendingTransactionResponse.isSuccessful){
            print(pendingTransactionResponse.data!.confirmedRound)
        }else{
            print(pendingTransactionResponse.errorDescription!)
            print("Error")
        }
}
```

## Quickstart For Indexer
The indexer allow's us to query the blockchain for data and information. There are 12 indexer methods that allow this. Let's try some code

```swift
var indexerClient=IndexerClient(host: "INDEXER_API_ADDRESS", port: "API_PORT", token: "API_KEY")
  indexerClient.lookUpAssetBalances(assetId:14077815).execute(){response in
        if response.isSuccessful{
                print("success")
            print(response.data!.toJson()!)
        }else{
            print(response.errorDescription)
        }
    }

indexerClient.lookUpBlocks(roundNumber: 12471917).execute(){response in

        if response.isSuccessful{
                print("success")
            print(response.data!.toJson()!)
        }else{
            print(response.errorDescription)
        }
    }

indexerClient.searchForAccounts(assetId: 14077815).execute(){ response in
        if response.isSuccessful{
            print(response.data!.toJson()!)
        }else{
            print(response.errorDescription)
        }
    }

     indexerClient.searchForTransactions(txid:"HPS2AQU26NNVTFIJVBYYZN2P2T73AONKWCS7HPT5JUQEQMXFHMJA").execute(){ response in
        if response.isSuccessful{
            print(response.data!.toJson()!)
        }else{
            print(response.errorDescription)
            print("failure")

        }
    }


 indexerClient.lookUpAssetById(id:14077815).execute(){response in

        if response.isSuccessful{
                print("success")
            print(response.data!..toJson()!)
        }else{
            print(response.errorDescription)
            print("Error");

        }
    }

      indexerClient.searchForAssets(assetId:14077815).execute(){ response in
        if response.isSuccessful{
            print(response.data!..toJson()!)
        }else{
            print(response.errorDescription)
            print("Error");
        }
    }
```
Please feel free to check out this [IOS  showcase](https://github.com/Jesulonimi21/swift-algorand-sdk-ios-showcase#accounts-and-transactions) that shows you how to do much more with the Swift Algorand SDK
