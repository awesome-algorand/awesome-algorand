<!-- markdownlint-disable no-inline-html -->
<!-- markdownlint-disable first-line-h1 -->
<p align="center"><img  width=100%  src="https://infura-ipfs.io/ipfs/QmRVnM9EaCk3u9p42b5ppLjwxUPv54EDQihmkNyFxqKuVi"  border="0" /></p>

<p align="center">
    <a href="https://algorand.com"><img src="https://img.shields.io/badge/Powered by-Algorand-teal.svg" alt="Algorand" /></a>
    <a><img src="https://visitor-badge.glitch.me/badge?page_id=algorand.graviton&right_color=green" /></a>
</p>

# About

Graviton is a software toolkit for blackbox testing of smart contracts written in TEAL.

## [Tutorial](./graviton/README.md)

## Local Installation

The following instructions assume that you have `make` available in your local environment. In Mac OS and Linux this is most likely already available and in Windows one way to install is with [chocolatey](https://chocolatey.org/) and the command `choco install make`.

To install all dependencies:

```sh
make pip-notebooks
```

## Running Blackbox Integration Tests against a Sandbox

### Prereq - Install and Symbolically Link to the Sandbox

If you would like to use the [Makefile](./Makefile) without modification and with full functionality, you should create a symbolic link to  [the algorand sandbox repo](https://github.com/algorand/sandbox) as described here. There are many ways to accomplish this. Assuming you have cloned ***the sandbox*** into the path  `/path/to/algorand/sandbox/` and that you've `cd`'ed into the cloned `graviton` directory you should create a symbolic link as follows:

#### Linux / Mac OS

```sh
ln -s /path/to/algorand/sandbox/ sandbox
```

#### Windows 10+

```sh
mklink sandbox \path\to\algorand\sandbox
```

<!-- TODO: Re-do this using the docker image as in PyTEAL  -->
### Test the Sandbox

With your sandbox running to test that the sandbox is running properly, use the following:

```sh
make local-sandbox-test
```

### Run the Integration Tests

```sh
make integration-test
```

## Running and Testing Jupyter Notebooks

To run the notebook `notebooks/quadratic_factoring_game.ipynb` for example:

```sh
make local-notebook NOTEBOOK=notebooks/quadratic_factoring_game.ipynb
```

To non-interactively run all the jupyter notebook tests:

```sh
make notebooks-test
```

## Ensuring that all is Copacetic Before Pushing to Github

To test in your local environment that everything is looking good before pushing to Github, it is recommended that you run `make all-tests`

If you would like to simulate the github actions locally, you'll need to install [nektos act](https://github.com/nektos/act/wiki/Installation). On Mac OS with [Docker](https://docs.docker.com/desktop/mac/install/) previously installed you can use `brew install act`; on the other hand, on Linux and Windows follow the installation instructions in the nextos repo link above.

Once `act` is available you can simulate all the github actions integration tests with:

```sh
make local-gh-simulate
```
