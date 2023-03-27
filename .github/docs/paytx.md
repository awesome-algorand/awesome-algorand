# paytx
Examples of common pay transaction scenarios using the Algorand Python SDK.

## Install Python Algorand SDK
`pip3 install py-algorand-sdk`

## To Run
`python3 pay-scenarios.py`


This will produce 3 transaction files:
1. alice_sender_testnet.tx - transaction output for scenarios 1-4
2. alice_bob_with_multisig.tx - transaction output for scenario 5 (no multisig)
3. alice_bob_no_multisig.tx - transaction output for scenario 5 (with multisig)

