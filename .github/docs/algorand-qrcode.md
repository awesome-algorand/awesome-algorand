[<img title="Algorand QR Code Generator (Banner art by Stasya Tikhonova, curtsey of Algorand)" src="./examples/images/algorand-qrcode-banner.jpg">](https://developer.algorand.org/solutions/algorand-qr-code-generator-javascript/)

# Algorand QR Code Generator V3.1.9
[![NPM](https://img.shields.io/npm/v/algorand-qrcode.svg)](https://www.npmjs.com/package/algorand-qrcode) [![JavaScript Style Guide](https://img.shields.io/badge/code_style-standard-brightgreen.svg)](https://standardjs.com)
[![npm](https://img.shields.io/static/v1?label=license&message=MIT&color=green&style=flat-square)](https://github.com/emg110/algorand-qrcode/blob/master/license)

New version 3 is a complete re-write of the Algorand QRCode generation tool. Simpler and more effective!

Breaking changes: The way to import and some of options have changed , please consult this readme.

<div style="display:block; text-align:center; align-items:center; margin:auto">
  <img style="display:block; margin:auto; cursor:pointer; text-align:center; align-items:center;" title="Generated QR example" src="./examples/images/generated-qr.png" height="auto" width="150">
</div>

<p style="text-align:center; display:block; background-color:#4fcdf0; font-size:0.7em">algorand://AMESZ5UX7ZJL5M6GYEHXM63OMFCPOJ23UXCQ6CVTI2HVX6WUELYIY262WI?label=emg110@gmail.com</p>

## Demo

###  [Live Demo](https://emg110.github.io/algorandqrcode/)

## Links

###  [Algorand Developers Portal Publication](https://developer.algorand.org/solutions/algorand-qr-code-generator-javascript/)

###  [Algorand Dev Hours Presentation](https://cutt.ly/SnkO7Xl)

###  [Algorand Dev Hours Presentation Video on YouTube](https://www.youtube.com/watch?v=RzP3y42Lf4o)


## News

> ##  Version 3.0.0 is out!

> ###  Now completely supports any modern web framework

> ### Modern JS Module in both Node and Browser



## Technical notes

- Amount is in MicroAlgos
  
- Algorand URI reference specification: [Algorand payment prompts specification](https://developer.algorand.org/docs/reference/payment_prompts/).
  
- Requires NodeJS version later than 10. 
  
 

## Table of contents


- [Highlights](#highlights)
- [Algorand URI's ABNF Grammar](#algorand-uri-abnf-grammar)
- [Installation](#installation)
- [Usage](#usage)
- [Error correction level](#error-correction-level)
- [Mentioned Trademarks](#mentioned-trademarks)
- [Credits](#credits)
- [License](#license)



## Highlights
- Supports NodeJS and Browser.
- Supports RFC 3986 and Algorand URI ABNF Grammar.
- CLI utility.
- Save QR code as valid SVG image or text

## Algorand URI ABNF Grammar

```javascript
    algorandurn     = "algorand://" algorandaddress [ "?" algorandparams ]
    algorandaddress = *base32
    algorandparams  = algorandparam [ "&" algorandparams ]
    algorandparam   = [ amountparam / labelparam / noteparam / assetparam  ]
    amountparam     = "amount=" *digit
    labelparam      = "label=" *qchar
    assetparam      = "asset=" *digit
    note            = "note=" *qchar
```

## Installation and use


```shell
npm install --save algorand-qrcode
```
and then 

```shell
import algoqrcode from "algorand-qrcode/lib/bundle.min.js"
```

or, install it globally to use `qrcode` cli command to generate Algorand URI qrcode images in your terminal.

```shell
npm install -g algorand-qrcode
```
and then 

```shell
algoqrcode [options]
```

## Usage

### Browser and Frameworks (react...) use

```javascript
import algoqrcode from "algorand-qrcode/lib/bundle.min.js";
const MyQrCodeComponent = (props)=>{
  let qrcode = algoqrcode({wallet:props.wallet, label:props.label})
  let scg = qrcode.svg()
  return svg
}
 
      
```

### CLI

```
Usage: qrcode [options]

Algorand options:
  -m, --amount Amount (in Micro Algos) of Algorand transaction          [number]
  -w, --wallet Destination Wallet address (Algorand account address)      [string]
  -l, --label Label of Algorand transaction                             [string]
  -a, --asset Algorand asset id (in case of Algorand ASA transfer)      [string]
  -n, --note note                                                       [string]

QR Code options:
              
  -e, --ecl     Error correction level           [choices: "L", "M", "Q", "H"]



Renderer options:
  -o, --output        Output type           [choices: "file", "svg", "terminal"]
  -w, --wallet        Destination wallet                                [number]
  -p, --padding       Padding around QRcode                             [number]
  -b, --background    Light color                                       [string]
  -c, --color         Dark color                                        [string]
  -s, --size          QRcode image width and height (px)                [number]
  -f, --file          Output file                                       [string]


Options:

  -h, --help    Show help                                              [boolean]
  --version     Show version number                                    [boolean]

Examples:
    - Send 1 Algo transaction:
    node qrcode -w "AMESZ5UX7ZJL5M6GYEHXM63OMFCPOJ23UXCQ6CVTI2HVX6WUELYIY262WI" -m 1000000 -s 128 -n "This is an Algo payment transaction QR Code"

    - Save Algorand contact label as svg image:
    node qrcode -w "AMESZ5UX7ZJL5M6GYEHXM63OMFCPOJ23UXCQ6CVTI2HVX6WUELYIY262WI" -l "emg110@gmail.com" -o file -f sample.svg 

```


### NodeJS
Import the module `algorand-qrcode` for your NodeJS module

```javascript
        import algoqrcode from 'algorand-qrcode'
        let qrcode = algoqrcode({
            wallet: "AMESZ5UX7ZJL5M6GYEHXM63OMFCPOJ23UXCQ6CVTI2HVX6WUELYIY262WI",
            label: "Test Label",
            output: "svg",
            size:256
        })
        let svg = qrcode.svg()
        console.log(svg)
```

## Error correction level
Error correction capability allows to successfully scan a QR Code even if the symbol is dirty or damaged.
Four levels are available to choose according to the operating environment.

Higher levels offer a better error resistance but reduce the symbol's capacity.<br>
If the chances that the QR Code symbol may be corrupted are low (for example if it is showed through a monitor)
is possible to safely use a low error level such as `Low` or `Medium`.

Possible levels are shown below:

| Level            | Error resistance |
|------------------|:----------------:|
| **L** (Low)      | **~7%**          |
| **M** (Medium)   | **~15%**         |
| **Q** (Quartile) | **~25%**         |
| **H** (High)     | **~30%**         |

The percentage indicates the maximum amount of damaged surface after which the symbol becomes unreadable.

Error level can be set through `options.ecl` property.<br>
If not specified, the default value is `M`.



#### QR Code options

    
##### `errorCorrectionLevel`
  Type: `String`<br>
  Default: `M`

  Error correction level.<br>
  Possible values are `low, medium, quartile, high` or `L, M, Q, H`.


#### Algorand URI params

##### `wallet`
  Type: `String`<br>

  Wallet address for Algorand transaction.

##### `amount`
  Type: `Number`<br>

  Amount of Algorand transaction in MicroAlgos or Standard Asset Unit.
  
##### `label`
  Type: `String`<br>

  Label of Algorand transaction.

##### `asset`
  Type: `String`<br>

  Asset Id of Algorand transaction if used. If not specified , Algo will be used as fungible token.
  
##### `note`
  Type: `String`<br>

  note  field content of Algorand transaction.


#### Renderers options

##### `ecl`
  Type: `String`<br>
  Default: `M`

  Define the error correction level.

##### `padding`
  Type: `Number`<br>
  Default: `5`

  Define how much wide the quiet zone should be.

##### `size`
  Type: `Number`<br>
  Default: `128`

  Width and height.


##### `color`
Type: `String`<br>
Default: `#000000ff`

Color of dark module. Value must be in hex format (RGBA).<br>
Note: dark color should always be darker than `color.light`.

##### `background`
Type: `String`<br>
Default: `#ffffffff`

Color of light module. Value must be in hex format (RGBA).<br>


## License
[MIT](https://github.com/emg110/algorand-qrcode/blob/master/license)


## Credits
> Special appreciations to  [Sheghzo](https://github.com/sheghzo/).


  
> The idea for this lib was inspired by: Algorand developers portal Article [Payment Prompts with Algorand Mobile Wallet](https://developer.algorand.org/articles/payment-prompts-with-algorand-mobile-wallet/ ) ,from Jason Paulos.


## Mentioned Trademarks
"QR Code" curtsey of :<br>
[<img title="DENSO WAVE Incorporated" src="https://milliontech.com/wp-content/uploads/2017/01/Denso-Wave-Logo-300x102.png" height="auto" width="128">](https://www.denso-wave.com)


"Algorand" curtsey of:<br>
[<img title="Algorand Technologies" src="https://www.algorand.com/assets/media-kit/logos/full/png/algorand_full_logo_black.png" height="auto" width="128">](https://algorand.com)

