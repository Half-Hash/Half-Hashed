
<p align=center>
  <a href="https://github.com/Half-Hash/Half-Hashed">
    <img alt="Half Hashed" src="https://raw.githubusercontent.com/Half-Hash/Half-Hashed/main/client/client/src/media/HH-logo-wide.png">
  </a>
</p>

This is a simple implementation of a blockchain as a database using Python and JavaScript. It includes classes for the blockchain, blocks, and transactions. The implementation also includes proof-of-work mining and transaction validation.

This is a continuation of our project submitted to [SFHacks 2024](https://devpost.com/software/half-hashed).

## Features

- **Blockchain Class**: Manages the chain of blocks, including adding new blocks, mining blocks, and validating the chain.
- **Block Class**: Represents individual blocks in the blockchain, containing transactions and a reference to the previous block.
- **Transaction Class**: Represents transactions within the blockchain, including sender, recipient, amount, timestamp, data, and hash.
- **Proof of Work (PoW)**: Blocks are mined using a proof-of-work algorithm, requiring computational effort to validate transactions and create new blocks.
- **Transaction Validation**: Transactions are validated to ensure integrity and authenticity.
- **Persistence**: The blockchain data is saved to a file for persistence across sessions.

## Installation

1. Clone the repository:

```
git clone https://github.com/Koshelenkoa/sf-hacks24.git
```

2. Navigate to the project directory:

```
cd blockchain
```

## Usage

1. Run the main script to start the blockchain server which listens for connections on the specified port:

```
python demo.py
```

3. Start local webserver that interfaces with local copy of blockchain

```
cd ../client/client
npm start
```

## API Endpoints

- `/mine_block`: Mine a new block in the blockchain.
- `/add_transaction`: Add a new transaction to the pending transactions pool.
- `/get_chain`: Get the full chain of blocks.
- `/is_valid`: Check if the blockchain is valid.
- `/connect_node`: Connect a new node to the network.
- `/replace_chain`: Replace the current chain with the longest valid chain in the network.

## Authors
- [Ronin Morata](https://github.com/rpmorata)
- [Anastasia Koshelenko](https://github.com/Koshelenkoa)
- [Jason Tang](https://github.com/basonbang)
