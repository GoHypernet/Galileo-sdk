class ProfileWallet:
    def __init__(self, wallet, public_key, profilewalletid=None):
        self.profilewalletid = profilewalletid
        self.wallet = wallet
        self.public_key = public_key


class ProfileCard:
    def __init__(self, id, user_id, stripe_payment_method_id, creation_timestamp):
        self.id = id
        self.user_id = (user_id,)
        self.stripe_payment_method_id = stripe_payment_method_id
        self.creation_timestamp = creation_timestamp


class Profile:
    def __init__(
        self,
        userid=None,
        username=None,
        lz_ids=[],
        wallets=[],
        stripe_customer_id=None,
        pricing_tier_id=None,
        stored_cards=None,
    ):
        self.userid = userid
        self.username = username
        self.lz_ids = lz_ids
        self.wallets = wallets
        self.stripe_customer_id = stripe_customer_id
        self.pricing_tier_id = pricing_tier_id
        self.stored_cards = stored_cards
