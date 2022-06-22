from header import Header

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
        header = Header("Network", id, message.D, -1, -1, -1, None)
        pck.AddHeader(header)

        self.Packages.append(pck)
        print("[REDE] - Pacote adicionado à camada de rede.\n")


class LinkLayer:
    '''
    Camada de enlace.
    '''
    def __init__(self, PhysicalLayer):
        self.Backoff = 0
        self.WayAccess = True
        self.PhysicalLayer = PhysicalLayer
        self.PackageRead = []

class PhysicalLayer:
    '''
    Camada física.
    '''
    def __init__(self, x, y, mac, reach, energy):
        self.X = x
        self.Y = y
        self.Mac = mac
        self.Neighborhood = []
        self.PackageckSent = []
        self.PackageReceived = []
        self.PackageSaved = []
        self.Reach = reach
        self.Energy = energy