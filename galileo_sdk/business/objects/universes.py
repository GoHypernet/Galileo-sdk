class Universe:
    def __init__(
        self,
        universe_id,
        name,
        creation_timestamp,
    ):
        """
        Universe Object

        :param universe_id: UUID of the Universe
        :param name: Human readable name of the Universe
        :param creation_timestamp: Time the Universe was created
        """
        self.universe_id = universe_id
        self.name = name
        self.creation_timestamp = creation_timestamp

    def __str__(self):
        return "Universe: {universe_name}".format(universe_name=self.name)

    def __repr__(self):
        return self.__str__()