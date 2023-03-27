# Algorand C++ SDK
This repo is providing C++ sdk on algorand chain.
=======
# 💎 Algorand SDK

## 📑 Specifications

The Algorand SDK provides developers with an easy way for devices to interact with Algorand chain.

We are doing our best to achieve those goals:

- C library, can be included into C++ projects.
- Can be easily imported into any project
- Examples provided:
  - [Unix-based OSes](examples/unix)
  - Windows (``not completed``)
- Connect to any Algorand API (local or remote provider)
- Build with CMake and Make
- Continuous Integration to maintain code quality:
  - Build static and shared library for several targets
  - Unit-Testing

At this sdk, there are some todo list to add new features:

- some bugs exists when compiling on some toolchains.  (Windows, Linux and Mac OS)
- Update some actions for building tx and requesting api , which can integrate as a thirdparty plugin easily. 
- add new functions to create wallet provider.

> ⚠️  IMPORTANT
> - The current version of the SDK is still *early*.
> - Development is ongoing and new transactions cases to be added.

## 🧭 Repository structure

```shell
.
├── CMakeLists.txt      # root CMakeLists: use it if you want to try the examples
├── examples            # examples
│   ├── unix            # Unix example to run the wallet on your machine or Raspberry Pi...
│   └── ...             # more to come
├── external            # external libraries
│   ├── mpack           # we've got mpack for example
│   └── cJson           # cJSON to parse JSON payloads
├── inc                 # public include directory: you'll need those files to use the library
│   ├── vertices.h      # for example, `vertices.h`
│   └── ...
├── src                 # 
│   ├── include         # "private" header files, used within the library
│   ├── algorand        # implementation of Vertices with Algorand. The Algorand provider is the first implemented.
│   ├── CMakeLists.txt  # CMake of the Vertices SDK, exports a package to be imported in your project, see examples' CMakeLists
│   └── ...             # source files
├── tests               # 
│   ├── src             # test sources is stored on this folder.
│   └── ...             
└── utils               # tools to make things easier, clearer, smarter :) 
    └── utils.cmake
```

## 🧰 Installation

This repository is intended to be used as an external component to your project such as a submodule.

```shell
# clone into a directory
git clone <url> [path]
# clone into a directory including its submodules
git clone --recurse-submodules <url> [path]
# clone as submodule into an optionally specified location
git submodule add <url> [path]
```


### Configuration

A config file provides an easy way to configure the SDK: [`include/vertices_config.h`](include/vertices_config.h). The file is fully documented.

### Compilation

CMake is currently used to build the library and examples (GNU Make and Visual Studio Make is on the roadmap).

#### CMake

In order to build the source using CMake in a separate directory (recommended), just enter at the command line:

```shell
mkdir build && cd build
cmake ..

# build static library: lib/libvertices.a
make vertices

# build Unix example
make unix_example
```

#### Make

👎 Soon.

## 🚀 Getting started

👉 More to come about how to import the package into your build system.

> 💡 This Algorand SDK is providing [examples](examples/) with various major SDKs. You can probably copy-paste our source code into your project 🙂.

### Examples

Full documentation is available at [docs.vertices.network](https://docs.vertices.network/).

## 📐 Tests

Make sure you have `cpputest` installed:

- Linux - `sudo apt-get install cpputest lcov`
- OSX - `brew install cpputest lcov`

From [`/tests`](/tests) you will be able to launch the unique command to run all the tests:

```shell
make all
```

Checkout the [Readme](/tests/README.md) for more information.

## 🙌 Contributing

