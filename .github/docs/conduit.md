<div style="text-align:center" align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/assets/algorand_logo_mark_white.png">
    <source media="(prefers-color-scheme: light)" srcset="docs/assets/algorand_logo_mark_black.png">
    <img alt="Shows a black Algorand logo light mode and white in dark mode." src="docs/assets/algorand_logo_mark_black.png" width="200">
  </picture>

[![CircleCI](https://img.shields.io/circleci/build/github/algorand/conduit/master?label=master)](https://circleci.com/gh/algorand/conduit/tree/master)
![Github](https://img.shields.io/github/license/algorand/conduit)
[![Contribute](https://img.shields.io/badge/contributor-guide-blue?logo=github)](https://github.com/algorand/go-algorand/blob/master/CONTRIBUTING.md)
</div>

# Algorand Conduit

Conduit is a framework for ingesting blocks from the Algorand blockchain into external applications. It is designed as modular plugin system that allows users to configure their own data pipelines for filtering, aggregation, and storage of transactions and accounts on any Algorand network.

# Getting Started

See the [Getting Started](./docs/GettingStarted.md) page.

## Building from source

Development is done using the [Go Programming Language](https://golang.org/), the version is specified in the project's [go.mod](go.mod) file. This document assumes that you have a functioning
environment setup. If you need assistance setting up an environment please visit
the [official Go documentation website](https://golang.org/doc/).

Run `make` to build Conduit, the binary is located at `cmd/conduit/conduit`.

# Configuration

See the [Configuration](./docs/Configuration.md) page.

# Develoment

See the [Development](./docs/Development.md) page for building a plugin.

# Plugin System
A Conduit pipeline is composed of 3 components, [Importers](./conduit/plugins/importers/), [Processors](./conduit/plugins/processors/), and [Exporters](./conduit/plugins/exporters/).
Every pipeline must define exactly 1 Importer, exactly 1 Exporter, and can optionally define a series of 0 or more Processors.

# Contributing

Contributions are welcome! Please refer to our [CONTRIBUTING](https://github.com/algorand/go-algorand/blob/master/CONTRIBUTING.md) document for general contribution guidelines, and individual plugin documentation for contributing to new and existing Conduit plugins.

# Common Setups

The most common usage of Conduit is to get validated blocks from a local `algod` Algorand node, and adding them to a database (such as [PostgreSQL](https://www.postgresql.org/)).
Users can separately (outside of Conduit) serve that data via an API to make available a variety of prepared queries--this is what the Algorand Indexer does.

Conduit works by fetching blocks one at a time via the configured Importer, sending the block data through the configured Processors, and terminating block handling via an Exporter (traditionally a database).
For a step-by-step walkthrough of a basic Conduit setup, see [Writing Blocks To Files](./docs/tutorials/WritingBlocksToFile.md).

# Migrating from Indexer

Indexer was built in a way that strongly coupled it to Postgresql, and the defined REST API. We've built Conduit in a way which is backwards compatible with the preexisting Indexer API and Postgresql DB.

Going forward we will continue to maintain the Indexer application, however our main focus will be enabling and optimizing a multitude of use cases through the Conduit pipeline design rather the singular Indexer pipeline.

For a more detailed look at the differences between Conduit and Indexer, see [our migration guide](./docs/tutorials/IndexerMigration.md).

# Known Issues

## Restarting Follower Nodes Multiple Times in a Row

When a follower node is restarted, the sync round is advanced to the node's ledger round. This causes a chain reaction where the node's ledger round is then advanced by `MaxAcctLookback` rounds. When this happens, the node should temporarily have access to 2 * `MaxAcctLookback` ledger state delta responses because some had been previously persisted to disk. However, if the follower node is restarted a second time before conduit has consumed the temporary ledger state delta objects, the node will become desynchronized from Conduit.

When this happens the follower node must be manually re-synchronized with Conduit. This is done by launching a new follower node or running fast catchup to move to an earlier round.
