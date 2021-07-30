class CargoBay:
    def __init__(
        self,
        name,
        storage_id,
        storage_type,
        creation_timestamp,
    ):
        """
        CarboBay Object

        :param name: Human readable name of the Cargo Bay
        :param storage_id: UUID of the Cargo Bay
        :param storage_type: The storage technology used by the Corgo Bay (i.e. Tardigrade)
        :param creation_timestamp: Time the Universe was created
        """
        self.storage_id = storage_id
        self.storage_type = storage_type
        self.name = name
        self.creation_timestamp = creation_timestamp

    def __str__(self):
        return "CargoBay: {name}".format(name=self.name)

    def __repr__(self):
        return self.__str__()