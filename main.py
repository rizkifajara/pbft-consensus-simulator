from src.node import Node, ByzantineNode
from src.network import Network
from src.consensus import PBFTConsensus
import time

def main():
    total_nodes = 7
    honest_nodes = [Node(i, total_nodes) for i in range(4)]
    byzantine_nodes = [
        ByzantineNode(4, total_nodes, 'random'),
        ByzantineNode(5, total_nodes, 'silent'),
        ByzantineNode(6, total_nodes, 'liar')
    ]
    nodes = honest_nodes + byzantine_nodes
    network = Network(nodes)

    for node in nodes:
        node.set_network(network)
        node.consensus = PBFTConsensus(node)

    honest_nodes[0].consensus.start_consensus("Hello, World!")
   
    for round in range(50):
        print(f"\nRound {round + 1}")
        for node in nodes:
            node.process_messages()
            node.consensus.check_consensus_status()
            print(f"Node {node.id} ({type(node).__name__}) - Phase: {node.consensus.phase}, Value: {node.consensus.current_value}")
        
        if all(node.consensus.phase == "DECIDED" for node in honest_nodes):
            print("\nConsensus reached!")
            break
        
        time.sleep(0.1)
    
    print("\nFinal states:")
    for node in nodes:
        print(f"Node {node.id} ({type(node).__name__}) - Final state: {node.consensus.phase}, Value: {node.consensus.current_value}")

if __name__ == "__main__":
    main()