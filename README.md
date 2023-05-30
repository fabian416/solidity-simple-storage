# Solidity Simple Storage

## Description

This project is a simple Solidity contract that allows users to store and 
retrieve a favorite number, as well as add people with their favorite 
numbers. 

In addition, it demonstrates key concepts of working with Ethereum 
blockchain, such as constructing, signing, and sending transactions. While 
this project has been tested on a testnet, it is designed to work 
seamlessly on the Ethereum mainnet as well.

## Setup

1. Clone this repository.
2. Install dependencies with `pip install -r requirements.txt`.
3. Provide your private key and Infura project ID as environment 
variables.
4. Run `python3 deploy.py`.

## Usage

The deployment script does the following:

1. Compiles the Solidity contract.
2. Deploys the contract to the Ethereum network (the network is determined 
by the Infura project ID).
3. Once the contract is deployed, it retrieves the favorite number 
(initially zero).
4. Stores a new favorite number.
5. Retrieves the new favorite number.

## License

This project is licensed under the terms of the MIT license.

