import math
from layers import NetworkLayer
from layers import LinkLayer
from layers import PhysicalLayer
from networkTopology import NetworkTopology, Network
from message import Message
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
        self.Network = NetworkLayer(LinkLayer(PhysicalLayer(x, y, nodeId, reach, energy)))
    
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
    nw = NetworkTopology()
    nw.Nodes = nodes
    msg = Message(messageText, nodeSender, nodeDestiny, None)
    return nw, msg

def main():
    print("[INICIO] - Lendo arquivo para configurar rede.")
    n, message = createNetworkFromFile("entrada.txt")
    Network.Nodes = n.Nodes
    print("[INICIO] - Arquivo lido e rede configurada!")
    print(Network.toString())
    t = 0
    while t < 20:
        print(f"[MENSAGEM] - Nó de origem: {message.S}, Nó de destino: {message.D}, conteudo: {message.M}")
        if t == 0:
            Network.sendMessage(message)
            Network.Senders.append(message.S)
        print(f"[MAIN] - Lista de nós que enviam: {Network.Senders}")
        if len(Network.NextSenders) > 0:
            for mac in Network.NextSenders:
                Network.Senders.append(mac)
        del Network.NextSenders[:]

        print(f"[MAIN] - Lista de nós que recebem: {Network.Macs}")
        for mac in Network.Macs:
            Network.Nodes[mac].Network.RecievePackage()
        del Network.Macs[:]

        print(f"[MAIN] - Nós que enviam: {Network.Senders}.")
        for mac in  Network.Senders:
            print(f"[MAIN] - Nó {Network.Nodes[mac].Id} se prepara para enviar pacote para camada de rede.")
            Network.Nodes[mac].Network.SendPackage()
        del Network.Senders[:]

        # atualiza tempo
        t = t+1

if __name__ == "__main__":
    main()