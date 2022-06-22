import math
from layers import *
from layers import LinkLayer
from layers import PhysicalLayer
class Node:
    '''
    Classe que simula um Hospedeiro.
    '''
    def __init__(self, nodeId, x, y, reach, energy, send, dest):
        self.Id = nodeId #Equivalente ao endereço mac
        self.X = x
        self.Y = y
        self.Reach = reach
        self.Energy = energy
        self.Sender = send #Valor booleano que indica se o nó está enviando
        self.Destination = dest #Valor booleano que indica se o nó está recebendo
        self.Network = NetworkLayer(LinkLayer(PhysicalLayer(x, y, id, reach, energy)))
    
    def isNeighbor(self, node) -> bool:
        a = (self.X - node.X)**2
        b = (self.Y - node.Y)**2
        euclidean = math.sqrt(a + b)
        if(euclidean <= self.Reach):
            return True
        else:
            return False

    def AddPackage(self, message):
        print("[HOST] - Criando pacote na camada de rede.")
        print(f"[HOST] - Pacote: {message.ToString()}.")
        self.Network.AddPackageToNetwork(message)
    
    def toString(self):
        return f"id: {self.Id}, posX,Y: ({self.X},{self.Y}), reach: {self.Reach}, energy: {self.Energy}"

class NetworkTopology:
    def __init__(self, nodes):
        self.Nodes = nodes

    def toString(self):
        return f"Nós: {[self.Nodes[node].toString() for node in self.Nodes]}"

    def sendMessage(self, message):
        self.Nodes[message.S].AddPackage(message)

class Message:
    def __init__(self, messageText, nodeSender, nodeDestiny):
        self.M = messageText
        self.S = nodeSender
        self.D = nodeDestiny
        self.Headers = []

    def AddHeader(self, header):
        print(f" [MESNAGEM] - Adicionando cabeçalho da camada {header.Layer} na mensagem.")
        self.Headers.append(header)

    def ToString(self):
        return f"Mac de Origem: {self.S}, Mac de Destino: {self.D}, Conteudo: {self.M}."

def createNetworkFromFile(filename):
    fileInput = open(filename)
    lines = fileInput.readlines()

    nodeSender = int(lines[0].split("->")[1].strip())
    nodeDestiny = int(lines[1].split("->")[1].strip())
    messageText = str(lines[2].split("->")[1].strip())
    
    print("[INICIO] - Definindo Nós da rede.")
    nodes = {}
    for line in lines:
        if lines.index(line) < 4:
            continue
        splitedLine = line.rstrip().split(' ') 
        nodeId = int(splitedLine[0].strip())
        nodeX = int(splitedLine[1].split(',')[0])
        nodeY = int(splitedLine[1].split(',')[1])
        nodeReach = int(splitedLine[2])
        nodeEnergy = int(splitedLine[3])

        isSender = nodeId == nodeSender
        isDestiny = nodeId == nodeDestiny

        nodes[nodeId] = Node(nodeId, nodeX, nodeY, nodeReach, nodeEnergy, isSender, isDestiny)
    print(f"[INICIO] - Rede definida com {len(nodes)} nós.")
    nw = NetworkTopology(nodes)
    msg = Message(messageText, nodeSender, nodeDestiny)
    return nw, msg

def main():
    print("[INICIO] - Lendo arquivo para configurar rede.")
    network, message = createNetworkFromFile("entrada.txt")
    print("[INICIO] - Arquivo lido e rede configurada!")
    print(network.toString())
    print(f"[MENSAGEM] - Nó de origem: {message.S}, Nó de destino: {message.D}, conteudo: {message.M}")
    network.sendMessage(message)

if __name__ == "__main__":
    main()