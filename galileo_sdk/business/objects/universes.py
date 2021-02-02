class Universe:
    def __init__(
        self,
        universe_id,
        name,
        creation_timestamp,
    ):
        """
        Universe Object

        :param mission_id: UUID of the Universe
        :param name: Human readable name of the Universe
        :param creation_timestamp: Time the Universe was created
        """
        self.universe_id = universe_id
        self.name = name
        self.creation_timestamp = creation_timestamp