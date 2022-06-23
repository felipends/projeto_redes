import random
from header import Header
from networkTopology import Network
from message import Message

class NetworkLayer:
    '''
    Camada de rede.
    '''
    def __init__(self, linkLayer):
        self.LinkLayer = linkLayer
        self.Packages = []
        self.RREQS = []
        self.WaitRoutes = []
        self.Routes = []

    def AddPackageToNetwork(self, message):
        print("[REDE] - Camada de rede inicializada")
        id = self.LinkLayer.PhysicalLayer.Mac
        pck = message
        header = Header("Network", id, message.D, -1, -1, None)
        pck.AddHeader(header)

        self.Packages.append(pck)
        print("[REDE] - Pacote adicionado à camada de rede.")

    def SendPackage(self):
        id = self.LinkLayer.PhysicalLayer.Mac
        print("[REDE] - Pacote mapeado na camada de rede.")
        print(f"[REDE] - Preparando para enviar mensagem do Nó {id}")
        if(self.Packages != []):
            package = self.Packages[0]
            header = package.GetNetworkHeader()
            seq = None
            print(f"[REDE] - Nó que envia {id}, nó que recebe {package.Headers[0].DMac}")

            for route in self.Routes:
                if(route.Receiver == package.Headers[0].DMac):
                    print("[REDE] - Rota para este destino encontrada!\n")
                    seq = route.Sequence
                    if (package.Headers[0].DMac in self.WaitRoutes):
                        self.WaitRoutes.remove( package.Headers[0].DMac)
                        print("[REDE] - Pacote entregue!\n")

            if(seq != None):
                print("[REDE] - Rotas já existem.")
                package.RefreshSequence(seq)
                self.Packages.pop(0)

                for i, mac in enumerate(package.Headers[0].Sequence):
                    id = self.LinkLayer.PhysicalLayer.Mac
                    print(f"[REDE] - Transmitindo do roteador - {mac}.")
                    if(mac == id):
                        next_node = header.Sequence[i-1]
                        print(f"\tNext Node: {next_node}.")
                        break
                print("[REDE] - Enviando pacote para camada de enlace.")
                self.LinkLayer.AddPackage(package, next_node)
                id = self.LinkLayer.PhysicalLayer.Mac
                Network.Senders.append(id)
                print("[REDE] - Nó que envia adicionado à lista de nós que enviam.")

            elif not header.DMac in self.WaitRoutes:
                print(f"[REDE] - Roteador {header.DMac} não está na lista de espera da rota.")
                self.WaitRoutes.append(package.Headers[0].DMac)

                print(f"[REDE] - Roteador {header.DMac} Adicionado à lista de espera em RREQ\n")
                self.RREQ(header.DMac)

        print(f"[ENLACE] - Camada de enlace começa envio de pacote.")
        self.LinkLayer.SendPackage()

    def RREQ(self, DMac):
        print("[REDE] - Inicializando RREQ.")

        id = self.LinkLayer.PhysicalLayer.Mac
        seq = []
        seq.append(id)
        seqNum = random.randint(1, 50) 
        print(f"[REDE] - Id do request: {seqNum}\n")

        self.RREQS.append(seqNum)
        print(f"[REDE] - Request {seqNum} adicionado a lista de RREQ da camada de rede.\n")

        header = Header("Network", id, DMac, 0, seqNum, seq)
        print("[REDE] - Criando pacote RREQ...\n")
        pck = Message("", 1, None, None)
        pck.AddHeader(header)
        msg = "Enviando RREQ "

        print(f"\tPacote {id}, Mensagem: {msg}")
        print("[REDE] - Enviando RREQ para camada de enlace.")
        self.LinkLayer.AddPackage(pck, -1)

    def PrintPackage(self, msg, id, DMac):
        print("\tID: ", id, "Mensagem: ", msg, ", Destino: ", DMac)


    def RecievePackage(self):
        self.LinkLayer.ReceivePackage()

        if len(self.LinkLayer.PackageRead) > 0:
            pckg = self.LinkLayer.PackageRead.pop(0)
            header = pckg.GetNetworkHeader()

            if header.Req == -1:
                # Pacote é de dados
                id = self.LinkLayer.PhysicalLayer.Mac
                if(header.DMac == id):
                    # Pacote é destinado ao nó em questão
                    msg = "Pacote de dados: "
                    print(f"[REDE] - Pacote {id} Info: ", "Mensagem: ", msg, " ", pckg.ToString())
                else:
                    msg = "Chegada de pacote de dados mas não é pra mim"
                    self.PrintPackage(msg, self.LinkLayer.PhysicalLayer.Mac, 0)

                    msg2 = "Enviando pacote de dados para o nó seguinte"
                    self.PrintPackage(msg2, self.LinkLayer.PhysicalLayer.Mac, 0)

                    for i, mac in enumerate(pckg.Headers[0].Sequence):
                        id = self.LinkLayer.PhysicalLayer.Mac
                        if(mac == id):
                            next_node = header.Sequence[i-1]
                            break

                    pckg.Headers.pop(1)
                    self.LinkLayer.AddPackage(pckg, next_node)

                    id = self.LinkLayer.PhysicalLayer.Mac
                    Network.Senders.append(id)

            elif header.Req == 0:
                # Pacote é RREQ
                msg = "Chegada de pacote RREQ"
                print(f"[REDE] - Nó {self.LinkLayer.PhysicalLayer.Mac} recebe pacote. Info:", msg, ", Numero de sequencia: ", header.NumPack)
               
                if not header.NumPack in self.RREQS:
                    # Nó não recebeu RREQ
                    self.RREQS.append(header.NumPack)
                    header.Sequence.append(self.LinkLayer.PhysicalLayer.Mac)

                    if header.DMac == self.LinkLayer.PhysicalLayer.Mac:
                        # RREQ é para o nó corrente
                        msg = "RREQ chegou ao destino"
                        self.PrintPackage(msg, self.LinkLayer.PhysicalLayer.Mac, 0)
                        route = header.Sequence
                        destination = route[0]
                        sequence_route = route
                        sequence_route.reverse()
                        self.RREP(destination, sequence_route, route)
                        Network.Senders.append(self.LinkLayer.PhysicalLayer.Mac)

                    else:
                        print(f"[REDE] - Nó {self.LinkLayer.PhysicalLayer.Mac} não é o destino do RREQ.")
                        print(" [REDE] - Pacote é dicionado a camada de enlace para retransmissão")
                        self.LinkLayer.AddPackage(pckg, -1)
                        Network.Senders.append(self.LinkLayer.PhysicalLayer.Mac)

                else:
                    msg = "RREQ já recebido por nó."
                    print(f"[REDE] - Nó {self.LinkLayer.PhysicalLayer.Mac} recebe pacote. Info:", msg, ", Numero de sequencia: ", header.NumPack)

            elif header.Req == 1:
                # Pacote é RREP
                msg = "Pacote é RREP."
                print(f"[REDE] - Nó {self.LinkLayer.PhysicalLayer.Mac} recebe pacote. Info:", msg, ", Numero de sequencia: ", header.Sequence)

                if header.DMac == self.LinkLayer.PhysicalLayer.Mac:
                    # RREP é para o nó corrente
                    msg = f"Nó {self.LinkLayer.PhysicalLayer.Mac} é o destino do pacote RREQ."
                    self.PrintPackage(msg, self.LinkLayer.PhysicalLayer.Mac, header.DMac)
                    msg2 = "Enviando dados"
                    self.PrintPackage(msg2, self.LinkLayer.PhysicalLayer.Mac, header.DMac)
                    packageMessage = pckg.M
                    route = Route(header.Sequence[0], packageMessage)
                    self.Routes.append(route)
                    Network.Senders.append(self.LinkLayer.PhysicalLayer.Mac)
                else:
                    msg = f"Nó {self.LinkLayer.PhysicalLayer.Mac} não é destino do RREP."
                    self.PrintPackage(msg, self.LinkLayer.PhysicalLayer.Mac, 0)
                    for i, mac in enumerate(header.Sequence):
                        if mac == self.LinkLayer.PhysicalLayer.Mac:
                            next_host = header.Sequence[i+1]
                            next_pck = pckg
                            pckg.Headers.pop(1)
                            self.LinkLayer.AddPackage(next_pck, next_host)
                            Network.Senders.append(self.LinkLayer.PhysicalLayer.Mac)
                            break

    def RREP(self, DMac, seq, route):
        print("[REDE] - Inicializando RREP.")

        id = self.LinkLayer.PhysicalLayer.Mac
        header = Header("Network", id, DMac, 1, -1, seq)
        print("\tCriando pacote RREP.")
        pkg = Message(route, None, None, 1)
        pkg.AddHeader(header)
        msg = "Sending RREP"
        print(f"[REDE]- Pacote {id} => Info: ", "Mensagem: ", msg, " destinatario: ", DMac)
        for i, mac in enumerate(header.Sequence):
            # Define uma rota para o RREP
            if(mac == id):
                next_node = header.Sequence[i+1]
                next_pkg = pkg
                print("[REDE] - Adicionando pacote RREP para camada de enlace.")
                self.LinkLayer.AddPackage(next_pkg, next_node)
                break                       

class LinkLayer:
    '''
    Camada de enlace.
    '''
    def __init__(self, PhysicalLayer):
        self.Backoff = 0
        self.WayAccess = True
        self.PhysicalLayer = PhysicalLayer
        self.PackageRead = []

    def AddPackage(self, Package, DMac):
        print("[ENLACE] - Camada de enlace inicializada!")
        print("[ENLACE] - Adicionando pacote à camada de enlace.")
        header = Header("Link", self.PhysicalLayer.Mac, DMac, -1, -1, -1)
        Package.AddHeader(header)
        print("[ENLACE] - Adicionando pacote para lista de pacotes enviada para camada física.")
        self.PhysicalLayer.PackagesSent.append(Package)

    def ReceivePackage(self):
        print(f'[ENLACE] - {self.PhysicalLayer.Mac}: Origem')

        if len(self.PhysicalLayer.PackageReceived) > 1:
            # Colisão detectada
            self.PhysicalLayer.PackageReceived.clear()
            print(f"\tColisão detectada no Nó {self.PhysicalLayer.Mac}")

        elif len(self.PhysicalLayer.PackageReceived) == 1:
                Package = self.PhysicalLayer.PackageReceived.pop(0)
                header = Package.GetLinkHeader()

                if(header.DMac == self.PhysicalLayer.Mac):
                    self.PackageRead.append(Package)
                elif(header.DMac == -1):
                    self.PackageRead.append(Package)

    def WayAccessIsFree(self):
        # Verifica se acesso ao meio está liberado.
        print("[ENLACE] - Verficando se acesso ao meio está liberado.")
        if len(self.PhysicalLayer.PackageReceived) == 0:
            print("[ENLACE] - Acesso ao meio liberado")
            return True
        else:
            print("[ENLACE] - Acesso ao meio bloqueado")
            return False

    def SendPackage(self):
        print("[ENLACE] - Pacote chegou na camada de enlace.")
        self.WayAccess = self.WayAccessIsFree()

        if self.WayAccess:
            if len(self.PhysicalLayer.PackagesSent) > 0:
                print("[ENLACE] - Verificando tempo de backoff:")
                if self.Backoff == 0:
                    print("\t[ENLACE] - Fora do tempo de backoff.")
                    print("[ENLACE] - Enviando pacote para meio físico.")
                    self.PhysicalLayer.SendPackage()
                else:
                    print(f"[ENLACE] - Nó {self.PhysicalLayer.Mac} está no tempo de backoff.")
                    Network.NextSenders.append(self.PhysicalLayer.Mac)
                    self.Backoff = (self.Backoff - 1)
        else:
            if len(self.PhysicalLayer.PackagesSent) > 0:
                if(self.Backoff == 0):
                    self.Backoff = random.randint(1, 3)
                    print("\tID: ", self.PhysicalLayer.Mac, " está em backoff, valor: ", self.Backoff)
                    Network.NextSenders.append(self.PhysicalLayer.Mac)

class PhysicalLayer:
    '''
    Camada física.
    '''
    def __init__(self, x, y, mac, reach, energy):
        self.X = x
        self.Y = y
        self.Mac = mac
        self.Neighborhood = []
        self.PackagesSent = []
        self.PackageReceived = []
        self.PackageSaved = []
        self.Reach = reach
        self.Energy = energy

    def SendPackage(self):
        print("[FISICA] - Pacote chegou à camada física.")
        self.FindNeighbors()
        for node in self.Neighborhood:
            print("[FISICA] - Realiza broadcast para nós vizinhos")
            node.Network.LinkLayer.PhysicalLayer.ReceivePackage(self.PackagesSent[0])

        print("[FISICA] - Salvando pacote na camada de redes")
        self.PackageSaved.append(self.PackagesSent.pop(0))

    def FindNeighbors(self):
        print(f'[FISICA] - Encontrando vizinhos do nó {self.Mac}.')
        self.Energy -= 1 
        print(f"Energia do nó {self.Mac} consumida, energia atual: {self.Energy}.")
        nodes = len(Network.Nodes)
        for i in Network.Nodes:
            if(Network.Nodes[i].Id != self.Mac):
                if(Network.Nodes[self.Mac].isNeighbor(Network.Nodes[i])):
                    if(Network.Nodes[i] not in self.Neighborhood):
                        print(f"Nó destino encontrado! {Network.Nodes[i].Id}")
                        self.Neighborhood.append(Network.Nodes[i])

    def ReceivePackage(self, package):
        print("[FISICA] - Pacote recebido.")
        Network.Macs.append(self.Mac)

        print(f"[FISICA] - Nó {self.Mac} recebeu o pacote!")
        self.PackageReceived.append(package)

class Route:
    def __init__(self, receiver, seq):
        self.Receiver = receiver
        self.Sequence = seq