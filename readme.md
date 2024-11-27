# PBFT Consensus Implementation

This repository contains a Python implementation of the Practical Byzantine Fault Tolerance (PBFT) consensus algorithm. The implementation simulates a network of nodes, including honest nodes and Byzantine (faulty) nodes, to demonstrate how PBFT achieves consensus in a distributed system.

## Features

- PBFT consensus algorithm implementation
- Simulation of honest and Faulty nodes
- Network simulation with arbitrary message loss
- View change mechanism

## Project Structure

- `src/`
  - `pbft.py`: Contains the `PBFTNode` class implementing the PBFT algorithm
  - `node.py`: Defines `Node` and `FaultyNode` classes
  - `message.py`: Defines the `Message` class for inter-node communication
  - `network.py`: Implements the `Network` class for simulating network behavior
- `main.py`: Entry point for running the PBFT simulation

## Requirements

- Python 3.7+

## Setup

Clone the repository:
   ```
   git clone https://github.com/yourusername/pbft-implementation.git
   cd pbft-implementation
   ```

## Usage

Run the simulation:
```
python3 main.py
```

This will start a simulation of the PBFT consensus process with a mix of honest and Byzantine nodes.

## Customization

You can modify the following parameters in `main.py`:
- `N`: Total number of nodes in the network
- `f`: Threshold for the faulty nodes in the network

## Understanding the Output

The simulation output shows the progress of each node through the consensus phases:
- IDLE: Initial state
- PRE-PREPARE: Primary node proposes a value
- PREPARE: Nodes acknowledge the proposed value
- COMMIT: Nodes commit to the value
- DECIDED: Consensus reached on the value

Byzantine nodes may behave differently:
- Random: Randomly corrupt messages
- Silent: Don't participate in the consensus
- Liar: Intentionally send conflicting messages

## Limitations

This is a simplified simulation of PBFT and has some limitations:
- No actual cryptographic signatures for message authentication
- Simplified network model
- Basic view change mechanism
- No optimization for performance in large networks

## Future Improvements

Potential areas for enhancement include:
- Implementing cryptographic signatures
- More sophisticated Byzantine behaviors
- Advanced view change protocol
- Performance optimizations for larger networks
- Visualization of the consensus process

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgements

This implementation is based on the PBFT algorithm as described in the paper "Practical Byzantine Fault Tolerance" by Miguel Castro and Barbara Liskov.