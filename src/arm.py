class ARM:
    def __init__(self):
        self.arm_entities = []

    def add_arm_entity(self, new_arm_entity):
        self.arm_entities.append(new_arm_entity)

    def get_arm_entities(self):
        """Getter for arm entities."""
        return self.arm_entities

    def __len__(self):
        return len(self.arm_entities)

    def __str__(self):
        """A textual representation of the ARM Model."""
        return "\n".join(self.arm_entities)
