from arm_entity import ARM_Entity


class ARM:
    """
    A class used to represent an ARM Model in its entirity - a list of
    ARM_Entity objects and appropriate methods.

    Attributes
    ----------
    arm_entities : list of ARM_Entity
        The entities that together compose the ARM Model.

    Methods
    -------
    load_arm():
        Populates the ARM model object from an XML file
    transform_to_eer():
        Transforms the ARM and returns the corresponding EER model object
    save_to_xml():
        Saves the ARM model object as an XML file

    """

    def __init__(self):
        """
        ARM model constructor.
        Creates an ARM model without any entities.
        Entities must be added with the `add_arm_entity()` method.
        """
        self.arm_entities = []

    def add_arm_entity(self, new_arm_entity):
        """Adds an ARM_Entity to the model.

        Raises:
            AssertionError:
                if `new_arm_entity` supplied is not of type `ARM_Entity`
        """

        assert type(new_arm_entity) == ARM_Entity
        self.arm_entities.append(new_arm_entity)

    def get_arm_entities(self):
        """Getter for arm entities."""
        return self.arm_entities

    def __len__(self):
        """ Returns the number of entities that the model consists of. """
        return len(self.arm_entities)

    def __str__(self):
        """
        A textual representation of the ARM Model.

        e.g.
        ARM Model:
        ----------
        Movie(__MovieID__ (anyType), Name (string), Director (anyType))
        Actor(__ActorID__ (anyType), Name (anyType), Age (int), Sex (anyType))
        """
        str_repr = "ARM Model:"
        underline = "-"*len(str_repr) + "\n"  # to underline 'ARM Model:'
        str_repr = underline + str_repr + "\n" + underline
        str_repr += "\n".join(ent.__str__() for ent in self.arm_entities)
        return str_repr
