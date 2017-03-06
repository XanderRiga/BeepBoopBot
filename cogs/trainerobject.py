class TrainerObject(object):
    """An object to store trainer codes"""

    def __init__(self, trainercode, description):
        """Return a new Car object."""
        self.trainercode = trainercode
        self.description = description

    def toString(self):
        string = "Trainer Code: " + self.trainercode + "\nDescription: " + self.description
        return string

    def __hash__(self):
        return hash(self.trainercode)

    def __eq__(self, other):
        return self.trainercode == other.trainercode