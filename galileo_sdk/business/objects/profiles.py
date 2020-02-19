from typing import List, Optional


class ProfileWallet:
    profilewalletid: Optional[str]
    wallet: str
    public_key: str

    def __init__(
        self, wallet: str, public_key: str, profilewalletid: Optional[str] = None
    ):
        self.profilewalletid = profilewalletid
        self.wallet = wallet
        self.public_key = public_key


class Profile:
    userid: Optional[str]
    username: Optional[str]
    mids: List[str]
    wallets: List[ProfileWallet]

    def __init__(
        self,
        userid: str = None,
        username: str = None,
        mids: List[str] = [],
        wallets: List[ProfileWallet] = [],
    ):
        self.userid = userid
        self.username = username
        self.mids = mids
        self.wallets = wallets
