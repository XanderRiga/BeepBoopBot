class TrainerObject(object):
    """An object to store trainer codes"""

    def __init__(self, trainercode, author, description):
        """Return a new Car object."""
        self.trainercode = trainercode
        self.author = author
        self.description = description

    def toString(self):
        string = "Trainer Code: " + self.trainercode + "\nAuthor: " + self.author + "\nDescription: " + self.description
        return string
