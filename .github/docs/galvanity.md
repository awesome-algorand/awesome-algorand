> This resource is auto indexed by AwesomeAlgo, all credits to galvanity, for more details refer to https://github.com/shmutalov/galvanity

---

[![build](https://github.com/shmutalov/galvanity/actions/workflows/build.yml/badge.svg)](https://github.com/shmutalov/galvanity/actions/workflows/build.yml)

# Galvanity

Galvanity is Algorand vanity address generator written in Go

# Usage

`galvanity [search-type] <pattern>`

`search-type` is matching function to search for the pattern, it can be:
 - `exact`    - search exact pattern (full address string)
 - `starts`   - search address which starts with given pattern
 - `ends`     - search address which ends with given pattern
 - `contains` - search address which contains given pattern at any place

`pattern` is correct [**BASE32** / RFC 4648](https://datatracker.ietf.org/doc/html/rfc4648) hash string, alphabet is `A-Z` and `2-7`

# Examples

`galvanity starts ALGO` - program will try to find generated addresses which starts with `ALGO` in their name

Output will be like:

```
$ ./galvanity starts ALGO
Pattern to find: ALGO
Search type: starts
Matching started...
Processed: 1 MH Speed: 182.17 KH/s Time elapsed: 5.49 s
Processed: 2 MH Speed: 181.41 KH/s Time elapsed: 11.00 s

==== ==== ====
Found ADDR: ALGO2INGB7XUD3TCMEUELGPDTKXWSGBFIQSIRVN66NI3WMCSLSUNBST6NM
PUB: [2 204 237 33 166 15 239 65 238 98 97 40 69 153 227 154 175 105 24 37 68 36 136 213 190 243 81 187 48 82 92 168]
PK: [170 178 173 195 190 49 191 72 18 228 194 93 111 103 224 161 130 42 175 183 87 151 87 40 209 252 159 58 197 48 218 152 2 204 237 33 166 15 239 65 238 98 97 40 69 153 227 154 175 105 24 37 68 36 136 213 190 243 81 187 48 82 92 168]
MNEMONIC: fetch replace gift brief lazy mutual calm seed two oval usual claw fence type sad nuclear april dwarf wrist prepare media method short above movie
==== ==== ====

Processed: 3 MH Speed: 181.87 KH/s Time elapsed: 16.50 s
Processed: 4 MH Speed: 181.97 KH/s Time elapsed: 22.00 s
Processed: 5 MH Speed: 182.19 KH/s Time elapsed: 27.48 s

==== ==== ====
Found ADDR: ALGOFQER73JZZEOBUOS37WNFF2X7EFISER2XWLHVBU2QWFLI4BZTA7TDNE
PUB: [2 204 226 192 145 254 211 156 145 193 163 165 191 217 165 46 175 242 21 18 36 117 123 44 245 13 53 11 21 104 224 115]
PK: [62 251 166 51 66 159 151 245 71 131 129 134 140 155 136 252 120 41 61 23 181 162 181 44 25 253 180 1 183 128 196 148 2 204 226 192 145 254 211 156 145 193 163 165 191 217 165 46 175 242 21 18 36 117 123 44 245 13 53 11 21 104 224 115]
MNEMONIC: guitar orbit border vintage connect word boss light move hotel dust more fancy soon post pencil note gorilla leader brave host cage plate above tag
==== ==== ====

Processed: 6 MH Speed: 181.98 KH/s Time elapsed: 32.98 s
Processed: 7 MH Speed: 182.55 KH/s Time elapsed: 38.46 s
Processed: 8 MH Speed: 181.96 KH/s Time elapsed: 43.95 s
Processed: 9 MH Speed: 182.45 KH/s Time elapsed: 49.43 s

==== ==== ====
Found ADDR: ALGOYTE6VC4PAAKHDO4IKCKZB3L5KET7T4S6V5747AQGLS4NPU6D7APLBQ
PUB: [2 204 236 76 158 168 184 240 1 71 27 184 133 9 89 14 215 213 18 127 159 37 234 247 252 248 32 101 203 141 125 60]
PK: [108 67 32 160 34 64 106 12 220 162 31 15 38 5 254 175 190 127 200 192 248 186 5 115 178 232 106 27 110 233 63 86 2 204 236 76 158 168 184 240 1 71 27 184 133 9 89 14 215 213 18 127 159 37 234 247 252 248 32 101 203 141 125 60]
MNEMONIC: horn library exotic acquire stand adapt black cabbage sea behind yellow turtle youth craft ship road gaze six inmate repeat switch where rapid able scorpion
==== ==== ====


==== ==== ====
Found ADDR: ALGOQL4QIQJQCEENXABSWUY7UEKFJQFP72HL7GGNQVE4P4URBD5AIXTH7M
PUB: [2 204 232 47 144 68 19 1 16 141 184 3 43 83 31 161 20 84 192 175 254 142 191 152 205 133 73 199 242 145 8 250]
PK: [171 138 166 41 73 128 127 94 197 226 200 196 212 150 106 28 98 173 28 184 20 183 197 204 175 5 252 70 18 241 113 101 2 204 232 47 144 68 19 1 16 141 184 3 43 83 31 161 20 84 192 175 254 142 191 152 205 133 73 199 242 145 8 250]
MNEMONIC: fever olive network afraid yellow fiscal bike similar obtain forget crystal canyon food already place require obvious sand actress hurt cause labor clog about axis
==== ==== ====

```

As you see, found addresses are:
1. `ALGO2INGB7XUD3TCMEUELGPDTKXWSGBFIQSIRVN66NI3WMCSLSUNBST6NM`
2. `ALGOFQER73JZZEOBUOS37WNFF2X7EFISER2XWLHVBU2QWFLI4BZTA7TDNE`
3. `ALGOYTE6VC4PAAKHDO4IKCKZB3L5KET7T4S6V5747AQGLS4NPU6D7APLBQ`
4. `ALGOQL4QIQJQCEENXABSWUY7UEKFJQFP72HL7GGNQVE4P4URBD5AIXTH7M`

It is infinity process, to stop you may send CTRL+C to the program.

Speed is `~180 000 address checks per second` on my `AMD Ryzen 7 2700x`. 

# Build

To build the Galvanity, you need to download and install the Go compiler (I tested with 1.15 version).

Then just run the following command in the source code directory:

```
go build
```

After successful build, it will produce `galvanity` (or `galvanity.exe` on Windows OS) named binary file

# Pre-built binaries

Check pre-built binaries at [**build-action**](https://github.com/shmutalov/galvanity/actions/workflows/build.yml) page, select the latest successful build, scroll down and download the needed artifacts.

# Roadmap

- [ ] Add the `threads` parameter
- [ ] Implement the GPU-side generator

# Donations

I accept donations to `DONATEYMDVCMPY2KKHTCTR2OAKLFQAJNGXRDXMJ7GJYXEZCHCNCHF4JABE`

# License

Galvanity is distributed under the terms GNU General Public License (Version 3).

See [LICENSE](./LICENSE) for details.