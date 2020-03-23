class ProfileWallet:
    def __init__(self, wallet, public_key, profilewalletid=None):
        self.profilewalletid = profilewalletid
        self.wallet = wallet
        self.public_key = public_key


class Profile:
    def __init__(
        self, userid=None, username=None, mids=[], wallets=[],
    ):
        self.userid = userid
        self.username = username
        self.mids = mids
        self.wallets = wallets
