class BobServer:
    PU_a = -1
    secret_key = b""
    message = ""
    
    def __init__(self, private, public):
        self.PU_b = public
        self.PR_b = private
    
    def get_public_key(self):
        return self.PU_b


class AliceServer:
    PU_b = -1
    secret_key = b""
    message = ""

    def __init__(self, private, public):
        self.PU_a = public
        self.PR_a = private

    def get_public_key(self):
        return self.PU_a

