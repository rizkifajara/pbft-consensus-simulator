from src.simulator import Simulator
from src.network import Network
from src.pbft import PBFTNode
from src.node import FaultyNode
import time


def main():
    # N is the total number of nodes
    N = 21
    # f is the total number of faulty nodes
    f = 6
    # This threshold injects some entropy into our network and drops some messages from being delivered.
    # We don't have any anti-entropy mechanism to replay lost messages.
    # A high threshold might cause consensus to halt.
    # Set it to -1 to disable this feature.
    delivery_threshold = 0.05
    # Make it True to enable logs.
    disable_logs = True

    #################

    print("===========")
    print(f"Scenario A: {N} non faulty nodes with {delivery_threshold*100}% message loss...")
    nodes = [PBFTNode(i, N, f, disable_logs) for i in range(N)]
    simulator = Simulator("PBFT", nodes, f, delivery_threshold)
    simulator.start()

    #################

    print("===========")
    print(f"Scenario B: {N} nodes are faulty...")
    nodes = [PBFTNode(i, N, f, disable_logs) for i in range(N)]
    nodes[7] = FaultyNode()
    nodes[8] = FaultyNode()
    nodes[9] = FaultyNode()
    simulator = Simulator("PBFT", nodes, f, delivery_threshold)
    simulator.start()

    print("===========")
    print(f"Scenario C: {N} nodes are faulty including the proposer...")

    nodes = [PBFTNode(i, N, f, disable_logs) for i in range(N)]
    nodes[0] = FaultyNode()
    nodes[8] = FaultyNode()
    nodes[9] = FaultyNode()
    simulator = Simulator("PBFT", nodes, f, delivery_threshold)
    simulator.start()


if __name__ == "__main__":
    main()
