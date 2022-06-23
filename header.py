class Header:
    def __init__(self, layer, sMac, dMac, req, numPack, sequence):
        self.Id = 1 
        self.Layer = ""
        self.SMac = -1
        self.DMac = -1
        self.NumPack = []
        self.Req = -1
        self.Sequence = []

        if(layer == "Link"):
            self.Layer = "Link"
            self.SMac = sMac
            self.DMac = dMac

        if(layer == "Network"):
            self.Layer = "Network"
            self.DMac = dMac
            self.Req = req
            self.NumPack = numPack
            self.Sequence = sequence