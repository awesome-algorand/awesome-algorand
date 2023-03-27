# AlgoKit CLI

The Algorand AlgoKit CLI is the one-stop shop tool for developers building on the Algorand network.

AlgoKit gets developers of all levels up and running with a familiar, fun and productive development environment in minutes. The goal of AlgoKit is to help developers build and launch secure, automated production-ready applications rapidly.

[Install AlgoKit](#install) | [Documentation](./docs/algokit.md)

## Capabilities

The set of capabilities supported by AlgoKit will evolve over time, but currently includes:

- Quickly run, explore and interact with an isolated local Algorand network (LocalNet)
- Building, testing and deploying [Algorand PyTEAL](https://github.com/algorand/pyteal) smart contracts

For a user guide and guidance on how to use AlgoKit, please refer to the [docs](./docs/algokit.md).

Future capabilities are likely to include:

- Quickly deploy [standardised](https://github.com/algorandfoundation/ARCs/#arcs-algorand-requests-for-comments), audited smart contracts
- Building and deploying Algorand dApps

## Guiding Principles

Algorand AlgoKit is guided by the following solution principles which flow through to the applications created by developers.

1. **Cohesive developer tool suite**: Using AlgoKit should feel professional and cohesive, like it was designed to work together, for the developer; not against them. Developers are guided towards delivering end-to-end, high quality outcomes on MainNet so they and Algorand are more likely to be successful.
2. **Seamless onramp**: New developers have a seamless experience to get started and they are guided into a pit of success with best practices, supported by great training collateral; you should be able to go from nothing to debugging code in 5 minutes.
3. **Leverage existing ecosystem**: AlgoKit functionality gets into the hands of Algorand developers quickly by building on top of the existing ecosystem wherever possible and aligned to these principles.
4. **Sustainable**: AlgoKit should be built in a flexible fashion with long-term maintenance in mind. Updates to latest patches in dependencies, Algorand protocol development updates, and community contributions and feedback will all feed in to the evolution of the software.
5. **Secure by default**: Include defaults, patterns and tooling that help developers write secure code and reduce the likelihood of security incidents in the Algorand ecosystem. This solution should help Algorand be the most secure Blockchain ecosystem.
6. **Extensible**: Be extensible for community contribution rather than stifling innovation, bottle-necking all changes through the Algorand Foundation and preventing the opportunity for other ecosystems being represented (e.g. Go, Rust, etc.). This helps make developers feel welcome and is part of the developer experience, plus it makes it easier to add features sustainably.
7. **Meet developers where they are**: Make Blockchain development mainstream by giving all developers an idiomatic development experience in the operating system, IDE and language they are comfortable with so they can dive in quickly and have less they need to learn before being productive.
8. **Modular components**: Solution components should be modular and loosely coupled to facilitate efficient parallel development by small, effective teams, reduced architectural complexity and allowing developers to pick and choose the specific tools and capabilities they want to use based on their needs and what they are comfortable with.

## Is this for me?

The target audience for this tool is software developers building applications on the Algorand network. A working knowledge of using a command line interfaces and experience using the supported programming languages is assumed.

## Contributing

This is an open source project managed by the Algorand Foundation. See the [contributing page](CONTRIBUTING.MD) to learn about making improvements to the CLI tool itself, including developer setup instructions.

# Install

## ⚠️ Beta Software ⚠️

**Work In Progress:** This tool is currently in the early stages of development, use at your own risk and please provide us feedback as you use it so we can make it better!

## Prerequisites

The key required dependency is Python 3.10+, but some of the installation options below will install that for you.

AlgoKit also has some runtime dependencies that also need to be available for particular commands.

> **Note**
> You can still install and use AlgoKit without these dependencies and AlgoKit will tell you if you are missing one for a given command.

- Git - Git is used when creating and updating projects from templates
- Docker - Docker Compose (and by association, Docker) is used to run the AlgoKit LocalNet environment, we require Docker Compose 2.5.0+

## Cross-platform installation

AlgoKit can be installed using OS specific package managers, or using the python tool [pipx](https://pypa.github.io/pipx/) see below for specific installation instructions.

- [Windows](#install-algokit-on-windows)
- [Mac](#install-algokit-on-mac)
- [Linux](#install-algokit-on-linux)
- [pipx](#install-algokit-with-pipx-on-any-os)

## Install AlgoKit on Windows

> **Note**
> This method will install the most recent python3 version [via winget](https://learn.microsoft.com/en-us/windows/package-manager/winget/). If you already have python 3.10+ installed, you may [prefer to use pipx directly instead](#install-algokit-with-pipx-on-any-os) so you can control the python version used.

1. Ensure prerequisites are installed

   - [Git](https://github.com/git-guides/install-git#install-git-on-windows) (or `winget install git.git`)
   - [Docker](https://docs.docker.com/desktop/install/windows-install/) (or `winget install docker.dockerdesktop`)
     > **Note**
     > See [our LocalNet documentation](docs/features/localnet.md#prerequisites) for more tips on installing Docker on Windows

2. Install using WinGet

   1. Install python: `winget install python.python.3.11`
   2. Restart the terminal to ensure Python and pip are available on the path

      > **Note**
      > Windows has a feature called **App Execution Aliases** that provides redirects for the Python command that guide users to the 
        Windows Store. Unfortunately these aliases can prevent normal execution of Python if Python is installed via other means, to disable them
        search for **Manage app execution aliases** from the start menu, and then turn off entries listed as 
        **App Installer python.exe** or **App Installer python3.exe**. 

   3. Install pipx: 
      ```
      pip install --user pipx
      python -m pipx ensurepath
      ```
   4. Install AlgoKit via pipx: `python -m pipx install algokit` 
   5. Restart the terminal to ensure AlgoKit is available on the path
 
3. [Verify installation](#verify-installation)

### Maintenance 
  Some useful commands for updating or removing AlgoKit in the future.
  - To update AlgoKit: `pipx upgrade algokit`
  - To remove AlgoKit: `pipx uninstall algokit`


## Install AlgoKit on Mac

> **Note**
> This method will install Python 3.10 as a dependency via Brew. If you already have python installed, you may prefer to use `pipx install algokit` as explained [here](#install-algokit-with-pipx-on-any-os).

1. Ensure prerequisites are installed

   - [Brew](https://docs.brew.sh/Installation)
   - [Git](https://github.com/git-guides/install-git#install-git-on-mac) should already be available if brew is installed
   - [Docker](https://docs.docker.com/desktop/install/mac-install/), (or `brew install --cask docker`)
      > **Note**
      > Docker requires MacOS 11+

2. Install using Brew  `brew install algorandfoundation/tap/algokit`
3. Restart the terminal to ensure AlgoKit is available on the path
4. [Verify installation](#verify-installation)

### Maintenance 
  Some useful commands for updating or removing AlgoKit in the future.
  - To update AlgoKit: `brew upgrade algokit`
  - To remove AlgoKit: `brew uninstall algokit`

## Install AlgoKit on Linux

1. Ensure prerequisites are installed

   - [Python 3.10+](https://www.python.org/downloads/)

     > **Note**
     > There is probably a better way to install Python than to download it directly, e.g. your local Linux package manager

   - [pipx](https://pypa.github.io/pipx/#on-linux-install-via-pip-requires-pip-190-or-later)
   - [Git](https://github.com/git-guides/install-git#install-git-on-linux)
   - [Docker](https://docs.docker.com/desktop/install/linux-install/)

2. Continue with step 2 in the following section to install via [pipx](#install-algokit-with-pipx-on-any-os)

## Install AlgoKit with pipx on any OS

1. Ensure desired prerequisites are installed

   - [Python 3.10+](https://www.python.org/downloads/)
   - [pipx](https://pypa.github.io/pipx/installation/)
   - [Git](https://github.com/git-guides/install-git)
   - [Docker](https://docs.docker.com/get-docker/)

2. Install using pipx `pipx install algokit`
3. Restart the terminal to ensure AlgoKit is available on the path
4. [Verify installation](#verify-installation)

### Maintenance 
  Some useful commands for updating or removing AlgoKit in the future.
  - To update AlgoKit: `pipx upgrade algokit`
  - To remove AlgoKit: `pipx uninstall algokit`


## Verify installation

Verify AlgoKit is installed correctly by running `algokit --version` and you should see output similar to:

```
algokit, version 0.2.0
```

It is also recommended that you run `algokit doctor` to verify there are no issues in your local environment and to diagnose any problems if you do have difficulties running AlgoKit. The output of this command will look similar to:

```
timestamp: 2023-01-19T01:22:07+00:00
AlgoKit: 0.2.0
AlgoKit Python: 3.11.1 (main, Dec 23 2022, 09:28:24) [Clang 14.0.0 (clang-1400.0.29.202)] (location: /Users/algokit/.local/pipx/venvs/algokit)
OS: macOS-13.1-arm64-arm-64bit
docker: 20.10.21
docker compose: 2.13.0
git: 2.37.1
python: 3.10.9 (location:  /opt/homebrew/bin/python)
python3: 3.10.9 (location:  /opt/homebrew/bin/python3)
pipx: 1.1.0
poetry: 1.3.2
node: 18.12.1
npm: 8.19.2
brew: 3.6.18

If you are experiencing a problem with AlgoKit, feel free to submit an issue via:
https://github.com/algorandfoundation/algokit-cli/issues/new
Please include this output, if you want to populate this message in your clipboard, run `algokit doctor -c`
```

Per the above output, the doctor command output is a helpful tool if you need to ask for support or [raise an issue](https://github.com/algorandfoundation/algokit-cli/issues/new).
