class ARM_Entity:
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.primary_key = []

    def add_attribute(self, new_attribute):
        self.attributes.append(new_attribute)

    def add_primary_key(self, new_primary_key):
        self.primary_key.append(new_primary_key)

    def get_name(self):
        """Getter for name."""
        return self.name

    def get_attributes(self):
        """Getter for attributes."""
        return self.attributes

    def get_primary_key(self):
        """Getter for primary_key."""
        return self.primary_key
