class Message:
    def __init__(self, messageData, nodeSender, nodeDestiny, t):
        self.M = messageData
        self.S = nodeSender
        self.D = nodeDestiny
        self.Headers = []
        self.T = t

    def AddHeader(self, header):
        print(f"[MESNAGEM] - Adicionando cabeçalho da camada {header.Layer} na mensagem.")
        self.Headers.append(header)

    def GetNetworkHeader(self):
        header = next(x for x in self.Headers if x.Layer == "Network")
        print(f"[MENSAGEM] - Cabeçalho da camada de rede => ID: {header.Id}")
        return header
    
    def GetLinkHeader(self):
        header = next(x for x in self.Headers if x.Layer == "Link")
        print(f"[MENSAGEM] - Cabeçalho da camada de enlace => ID: {header.Id}")
        return header

    def RefreshSequence(self, sequence):
        for header in self.Headers:
            if (header.Layer == "Network"):
                header.Sequence = sequence

    def ToString(self):
        return f"Mac de Origem: {self.S}, Mac de Destino: {self.D}, Conteudo: {self.M}."
