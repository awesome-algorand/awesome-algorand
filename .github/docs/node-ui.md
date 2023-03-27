# **DISCLAIMER**
This project is not supported, and is subject to change. There are no compatibility guarantees. It was developed during a hackathon and isn't perfect. If you see any strange artifacts, try resizing the window to help the program re-orient itself.

# Algod Node UI

Terminal UI for remote Algorand node management.

![Example Screenshot](images/demo.png)

# Install
## Download
See the GitHub releases and download the binary for your platform.

## Source
Use go1.17 or later and build with `make`.

# Usage
With no options, the UI will be displayed instead of starting a service.

## Local Algod
If you're using the downloaded binary, use `./node-ui` instead of `./nodeui`
```
~$ ALGORAND_DATA=path/to/data/dir ./nodeui
```
## Remote Algod
If you're using the downloaded binary, use `./node-ui` instead of `./nodeui`
```
~$ ./nodeui -t <algod api token> -u http://<url>
```

# Run as a service

The preferred method for running the node UI is as a service running alongside algod. By passing a port using `-p` or `--tui-port` an SSH server is started and can host the UI for multiple clients.

A tool like [wishlist](https://github.com/charmbracelet/wishlist#wishlist) can be used to interactively select between multiple node deployments. In the screenshot below you can see a sample ssh config file, and the UI wishlist provides to select which nodeui to connect to.

![Wishlist Example](images/wishlist_example.png)

# Features

## Status

Realtime node status, including detailed fast-catchup progress.

## Block Explorer

Display realtime block data, drill down into a block to see all of the transactions and transaction details.

## Utilities

Start a fast catchup with the press of a key, and more (if you build it)!

## Built in documentation

[Kind of](tui/internal/bubbles/about/help.go).

# Architecture

Built using [Bubble Tea](https://github.com/charmbracelet/bubbletea). Node information is collected from the Algod REST API using the [go SDK](https://github.com/algorand/go-algorand-sdk), and from reading files on disk.

Each box on the screen is a "bubble", they manage state independently with an event update loop. Events are passed to each bubble, which have the option of consuming the event and/or passing it along to any nested bubbles. When processing the event, they may optionally add follow-up tasks which the scheduling engine would execute asynchronously. Follow-up tasks may optionally create more events which would be processed in turn using the same mechanism.

When displaying the UI, each bubble is asked to renders itself and they are finally joined together for final rendering using [lipgloss](https://github.com/charmbracelet/lipgloss). Web development aficionado may recognize this pattern as [The Elm Architecture](https://guide.elm-lang.org/architecture/).

There are some quirks to this approach. The main one is that bubbletea is a rendering engine, NOT a window manager. This means that things like window heights and widths must be self-managed. Any mismanagement leads to very strange artifacts as the rendering engine tries to fit too many, or too few lines to a fixed sized terminal.

# Contributing

Contributions are welcome! There are no plans to actively maintain this project, so if you find it useful please consider helping out.

# How to create a new release

1. Create a tag: `git tag -a v_._._ -m "v_._._" && git push origin v_._._`
2. Make sure the dist directory does not exist: `rm -rf dist`
3. Export a GitHub token with `repo` scope: `export GITHUB_TOKEN=_`
4. Install & run goreleaser: `goreleaser release`
