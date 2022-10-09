class BobServer:
    PU_a = -1
    
    def __init__(self, private, public):
        self.PU_b = private
        self.PR_b = public
    
    def get_public_key(self):
        return self.PU_b


class AliceServer:
    PU_b = -1

    def __init__(self, private, public):
        self.PU_a = private
        self.PR_a = public

    def get_public_key(self):
        return self.PU_a

