# go-algorand-sdk

[![Build Status](https://travis-ci.com/algorand/go-algorand-sdk.svg?branch=master)](https://travis-ci.com/algorand/go-algorand-sdk)
[![Go Report Card](https://goreportcard.com/badge/github.com/algorand/go-algorand-sdk)](https://goreportcard.com/report/github.com/algorand/go-algorand-sdk)
[![GoDoc](https://godoc.org/github.com/algorand/go-algorand-sdk?status.svg)](https://godoc.org/github.com/algorand/go-algorand-sdk)

The Algorand golang SDK provides:

- HTTP clients for the algod (agreement) and kmd (key management) APIs
- Standalone functionality for interacting with the Algorand protocol, including transaction signing, message encoding, etc.

# Documentation

Full documentation is available [on godoc](https://godoc.org/github.com/algorand/go-algorand-sdk). You can also self-host the documentation by running `godoc -http=:8099` and visiting `http://localhost:8099/pkg/github.com/algorand/go-algorand-sdk` in your web browser.

Additional developer documentation and examples can be found on [developer.algorand.org](https://developer.algorand.org/docs/sdks/go/)

# Package overview

In `client/`, the `kmd` packages provide HTTP clients for the Key Management Daemon. It is responsible for managing spending key material, signing transactions, and managing wallets.
In `client/v2` the `algod` package contains a client for the Algorand protocol daemon HTTP API. You can use it to check the status of the blockchain, read a block, look at transactions, or submit a signed transaction.
In `client/v2` the `indexer` package contains a client for the Algorand Indexer API. You can use it to query historical transactions or make queries about the current state of the chain. 

`future` package contains Transaction building utility functions.

`types` contains the data structures you'll use when interacting with the network, including addresses, transactions, multisig signatures, etc. 

`encoding` contains the `json` and `msgpack` packages, which can be used to serialize messages for the algod/kmd APIs and the network.

`mnemonic` contains support for turning 32-byte keys into checksummed, human-readable mnemonics (and going from mnemonics back to keys).

# SDK Development

Run tests with `make docker-test`. To set up the sandbox-based test harness without standing up the go-algorand docker image use `make harness`.

# Quick Start

To download the SDK, open a terminal and use the `go get` command.

```command
go get -u github.com/algorand/go-algorand-sdk/...
```
