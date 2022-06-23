class NetworkTopology:
    def __init__(self):
        self.Nodes = []
        self.Packages = []
        self.Macs = []
        self.Senders = []
        self.NextSenders = []

    def toString(self):
        return f"Nós: {[self.Nodes[node].toString() for node in self.Nodes]}"

    def sendMessage(self, message):
        self.Nodes[message.S].AddPackage(message)

Network = NetworkTopology()