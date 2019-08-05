class ARM_Entity:
    def __init__(self, name):
        self.name = name
        self.attributes = []
        self.primary_key = []

    def add_attribute(self, new_attribute):
        self.attributes.append(new_attribute)

    def add_primary_key(self, new_primary_key):
        self.primary_key.append(new_primary_key)
