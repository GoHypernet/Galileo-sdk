class ProfileCard:
    def __init__(self, id, user_id, stripe_payment_method_id,
                 creation_timestamp):
        """
        Object representing a user's payment profile.

        :param id: UUID of Profile Card
        :type id: str
        :param user_id: UUID of user/Profile
        :type user_id: str
        :param stripe_payment_method_id: ID of the stripe payment method
        :type stripe_payment_method_id: str
        :param creation_timestamp: Profile creation timestamp
        :type creation_timestamp: 
        """
        self.id = id
        self.user_id = (user_id, )
        self.stripe_payment_method_id = stripe_payment_method_id
        self.creation_timestamp = creation_timestamp

    def __str__(self):
        return "Profile Card: {id}".format(id=self.id)

    def __repr__(self):
        return "Profile Card"


class Profile:
    def __init__(
        self,
        user_id=None,
        username=None,
        lz_ids=[],
        stripe_customer_id=None,
        pricing_tier_id=None,
        stored_cards=None,
    ):
        """
        Object representing a user's profile.

        :param user_id: User's UUID, defaults to None
        :type user_id: str, optional
        :param username: User's username, defaults to None
        :type username: str, optional
        :param lz_ids: Landing zones attached to or owned by user, defaults to []
        :type lz_ids: list, optional
        :param stripe_customer_id: The User's stripe ID, defaults to None
        :type stripe_customer_id: str, optional
        :param pricing_tier_id: User's current pricing tier, defaults to None
        :type pricing_tier_id: TODO: str, optional
        :param stored_cards: User's payment profiles, defaults to None
        :type stored_cards: list, optional
        """ """"""

        self.user_id = user_id
        self.username = username
        self.lz_ids = lz_ids
        self.stripe_customer_id = stripe_customer_id
        self.pricing_tier_id = pricing_tier_id
        self.stored_cards = stored_cards

    def __str__(self):
        if self.username:
            return "Profile: {username}".format(username=self.username)
        return "Profile: ID {id}".format(id=self.user_id)

    def __repr__(self):
        return self.__str__()