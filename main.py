class Node:
    def __init__(self, nodeId, send, dest, connections):
        self.Id = nodeId
        self.Sender = send #Valor booleano que indica se o nó está enviando
        self.Destination = dest #Valor booleano que indica se o nó está recebendo
        self.Connections = connections #Dicionário de conexões do nó

    def getCost(self, node2):
        return self.Connections[node2.Id] if self.Connections[node2.Id] is not None else -1

    def toString(self):
        return f"id: {self.Id}, Connections: {self.Connections}"

class NetworkTopology:
    def __init__(self, nodes):
        self.Nodes = nodes

    def toString(self):
        return f"Nodes: {[node.toString() for node in self.Nodes]}"

    def sendMessage(self, message):
        pass

class Message:
    def __init__(self, numberOfPackages, nodeSender, nodeDestiny):
        self.N = numberOfPackages
        self.S = nodeSender
        self.D = nodeDestiny

def createNetworkFromFile(filename):
    fileInput = open(filename)
    lines = fileInput.readlines()

    nodeSender = int(lines[0].split("->")[1].strip())
    nodeDestiny = int(lines[1].split("->")[1].strip())
    numberOfPackages = int(lines[2].split("->")[1].strip())

    nodes = []
    for line in lines:
        if lines.index(line) < 4:
            continue
        splitedLine = line.rstrip().split(' ') 
        nodeId = int(splitedLine[0].strip())
        nodeConnections = {}
        for linePosition in splitedLine:
            if splitedLine.index(linePosition) < 1:
                continue
            node2Id = int(linePosition.split(',')[0])
            connectionWeight = int(linePosition.split(',')[1])
            nodeConnections[node2Id] = connectionWeight
        isSender = nodeId == nodeSender
        isDestiny = nodeId == nodeDestiny

        nodes.append(Node(nodeId, isSender, isDestiny, nodeConnections))

    nw = NetworkTopology(nodes)
    msg = Message(numberOfPackages, nodeSender, nodeDestiny)
    return nw, msg

def main():
    network, message = createNetworkFromFile("entrada.txt")
    network.sendMessage(message)

    print(network.toString())

if __name__ == "__main__":
    main()