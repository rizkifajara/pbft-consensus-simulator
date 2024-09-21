# PBFT Consensus Implementation

This repository contains a Python implementation of the Practical Byzantine Fault Tolerance (PBFT) consensus algorithm. The implementation simulates a network of nodes, including honest nodes and Byzantine (faulty) nodes, to demonstrate how PBFT achieves consensus in a distributed system.

## Features

- PBFT consensus algorithm implementation
- Simulation of honest and Byzantine nodes
- Network simulation with message passing
- View change mechanism
- Byzantine node behaviors: random, silent, and liar

## Project Structure

- `src/`
  - `consensus.py`: Contains the `PBFTConsensus` class implementing the PBFT algorithm
  - `node.py`: Defines `Node` and `ByzantineNode` classes
  - `message.py`: Defines the `Message` class for inter-node communication
  - `network.py`: Implements the `Network` class for simulating network behavior
- `main.py`: Entry point for running the PBFT simulation

## Requirements

- Python 3.7+

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/pbft-implementation.git
   cd pbft-implementation
   ```

2. (Optional) Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies (if any):
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the simulation:
