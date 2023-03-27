> This resource is auto indexed by AwesomeAlgo, all credits to arc69, for more details refer to https://github.com/algokittens/arc69

---


# NOTE: THIS REPOSITORY IS NO LONGER MAINTAINED, FOR THE OFFICIAL SPEC SEE THE ALGORAND FOUNDATION GITHUB:

https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0069.md

---
arc: 69
title: Community Algorand Standard Asset Parameters Conventions for Digital Media Tokens
status: Living Standard
---

# Community Algorand Standard Asset Parameters Conventions for Digital Media Tokens

## Summary

We introduce community conventions for the parameters of Algorand Standard Assets (ASAs) containing digital media.

## Abstract

The goal of these conventions is to make it simpler to display the properties of a given ASA. This ARC differs from [ARC3](https://github.com/algorandfoundation/ARCs/blob/main/ARCs/arc-0003.md) by focusing on optimization for fetching of digital media, as well as the use of onchain metadata. Furthermore, since asset configuration transactions are used to store the metadata, this ARC can be applied to existing ASAs.

While mutability helps with backwards compatibility and other use cases, like leveling up an RPG character, some use cases call for immutability. In these cases, the ASA manager MAY remove the manager address, after which point the Algorand network won't allow anyone to send asset configuration transactions for the ASA. This effectively makes the latest valid ARC-69 metadata immutable.
 

## Specification

The key words "**MUST**", "**MUST NOT**", "**REQUIRED**", "**SHALL**", "**SHALL NOT**", "**SHOULD**", "**SHOULD NOT**", "**RECOMMENDED**", "**MAY**", and "**OPTIONAL**" in this document are to be interpreted as described in [RFC-2119](https://www.ietf.org/rfc/rfc2119.txt).

An ARC-69 ASA has an associated JSON Metadata file, formatted as specified below, that is stored on-chain in the most recent asset configuration transaction.

### ASA Parameters Conventions

The ASA parameters should follow the following conventions:

* *Unit Name* (`un`): no restriction. 
* *Asset Name* (`an`): no restriction.
* *Asset URL* (`au`): a URI pointing to digital media file. This URI:
    * **SHOULD** be persistent.
    * **SHOULD** link to a file small enough to fetch quickly in a gallery view.
    * **MUST** follow [RFC-3986](https://www.ietf.org/rfc/rfc3986.txt) and **MUST NOT** contain any whitespace character.
    * **SHOULD** specify media type with `#` fragment identifier at end of URL. This format **MUST** follow: `#i` for images, `#v` for videos, `#a` for audio, `#p` for PDF, or `#h` for HTML/interactive digital media.  If unspecified, assume Image.
    * **SHOULD** use one of the following URI schemes (for compatibility and security): *https* and *ipfs*:
        * When the file is stored on IPFS, the `ipfs://...` URI **SHOULD** be used. IPFS Gateway URI (such as `https://ipfs.io/ipfs/...`) **SHOULD NOT** be used.
    * **SHOULD NOT** use the following URI scheme: *http* (due to security concerns).
* *Asset Metadata Hash* (`am`): the SHA-256 digest of the full resolution media file as a 32-byte string (as defined in [NIST FIPS 180-4](https://doi.org/10.6028/NIST.FIPS.180-4))
    * **OPTIONAL**
* *Freeze Address* (`f`): 
    * **SHOULD** be empty, unless needed for royalties or other use cases
* *Clawback Address* (`c`): 
    * **SHOULD** be empty, unless needed for royalties or other use cases


There are no requirements regarding the manager account of the ASA, or the reserve account. However, if immutability is required the manager address **MUST** be removed.

### JSON Metadata File Schema

```json
{
    "title": "Token Metadata",
    "type": "object",
    "properties": {
        "standard": {
            "type": "string",
            "value": "arc69",
            "description": "(Required) Describes the standard used."
        },
        "description": {
            "type": "string",
            "description": "Describes the asset to which this token represents."
        },
        "external_url": {
            "type": "string",
            "description": "A URI pointing to an external website. Borrowed from Open Sea's metadata format (https://docs.opensea.io/docs/metadata-standards)."
        },
        "media_url": {
            "type": "string",
            "description": "A URI pointing to a high resolution version of the asset's media."
        },
        "properties": {
            "type": "object", 
            "description": "Properties following the EIP-1155 'simple properties' format. (https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1155.md#erc-1155-metadata-uri-json-schema)"
        },
        "mime_type": {
            "type": "string",
            "description": "Describes the MIME type of the ASA's URL (`au` field)."
        },
        "attributes": {
            "type": "array",
            "description": "(Deprecated. New NFTs should define attributes with the simple `properties` object. Marketplaces should support both the `properties` object and the `attributes` array). The `attributes` array follows Open Sea's format: https://docs.opensea.io/docs/metadata-standards#attributes"
        }
    }
}
```
The `standard` field is **REQUIRED** and **MUST** equal "arc69". All other fields are **OPTIONAL**. If provided, the other fields **MUST** match the description in the JSON schema.

The URI field (`external_url`) is defined similarly to the Asset URL parameter `au`.
However, contrary to the Asset URL, the `external_url` does not need to link to the digital media file.



#### MIME Type

In addition to specifying a data type in the ASA's URL (`au` field) with a URI fragment (ex: `#v` for video), the JSON Metadata schema also allows indication of the URL's MIME type (ex: `video/mp4`) via the `mime_type` field.



#### Examples

##### Basic Example

An example of an ARC-69 JSON Metadata file for a song follows. The properties array proposes some **SUGGESTED** formatting for token-specific display properties and metadata.

```json
{
  "standard": "arc69",
  "description": "arc69 theme song",
  "external_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "mime_type": "video/mp4",
  "properties": {
    "Bass":"Groovy", 
    "Vibes":"Funky", 
    "Overall":"Good stuff"
  }
}
```

An example of possible ASA parameters would be:

* *Asset Name*: `ARC69 theme song` for example.
* *Unit Name*: `69TS` for example.
* *Asset URL*: `ipfs://QmWS1VAdMD353A6SDk9wNyvkT14kyCiZrNDYAad4w1tKqT#v`
* *Metadata Hash*: the 32 bytes of the SHA-256 digest of the high resolution media file.
* *Total Number of Units*: 1
* *Number of Digits after the Decimal Point*: 0

#### Mutability

##### Rendering

Clients SHOULD render an ASA's latest ARC69 metadata. Clients MAY render an ASA's previous ARC69 metadata for changelogs or other historical features.

##### Updating ARC69 metadata

Managers MAY update an ASA's ARC69 metadata. To do so, they MUST send a new `acfg` transaction with the entire metadata represented as JSON in the transaction's `note` field.

##### Making ARC69 metadata immutable

Managers MAY make an ASA's ARC69 immutable. To do so, they MUST remove the ASA's manager address with an `acfg` transaction.

##### ARC69 attribute deprecation

The initial version of ARC69 followed the [Open Sea attributes format](https://docs.opensea.io/docs/metadata-standards#attributes). As illustrated below:
```
"attributes": {
"type": "array",
"description": "Attributes following Open Sea's attributes format (https://docs.opensea.io/docs/metadata-standards#attributes)."
}
```
This format is now deprecated. New NFTs **SHOULD** use the simple `properties` format, since it significantly reduces the metadata size.

To be fully compliant with the ARC69 standard, both the `properties` object and the `attributes` array **SHOULD** be supported. 

## Rationale

These conventions take inspiration from [Open Sea's metadata standards](https://docs.opensea.io/docs/metadata-standards) and [EIP-1155](https://github.com/ethereum/EIPs/blob/master/EIPS/eip-1155.md#erc-1155-metadata-uri-json-schema) to facilitate interoperobility. 

The main differences are highlighted below:

* Asset Name, Unit Name, and URL are specified in the ASA parameters. This allows applications to efficienty display meaningful information, even if they aren't aware of ARC-69 metadata.
* MIME types help clients more effectively fetch and render media.
* All asset metadata is stored onchain.
* Metadata can be either mutable or immutable.

## Copyright

Copyright and related rights waived via [CC0](https://creativecommons.org/publicdomain/zero/1.0/).
