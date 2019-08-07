from arm_attribute import ARM_Attribute


class ARM_Entity:
    """
    A class used to represent an ARM Entity
    - i.e. a relation/entity in an ARM model.

    Attributes
    ----------
    name : str
        The name of the entity.
    attributes : list of ARM_Attribute
        The attributes of the entity - including primary key attributes.
    primary_key : list of str
        The names of the attributes that form the primary key.
    """

    def __init__(self, name):
        """
        Entity constructor.
        Creates an ARM Entity without any attributes.
        Attributes must be added with the `add_attribute()` method.
        """
        self.name = name
        self.attributes = []
        self.primary_key = []

    def add_attribute(self, new_attribute):
        """Adds an ARM_Attribute to the entity.

        Raises:
            AssertionError:
                if `new_attribute` supplied is not of type `ARM_Attribute`
        """
        assert type(new_attribute) == ARM_Attribute
        self.attributes.append(new_attribute)

    def add_primary_key(self, new_primary_key):
        """Adds one of the entity's attributes to its primary key.

        Raises:
            AssertionError:
                if `new_primary_key` supplied is not the `name` of one of this
                entity's attributes
        """
        assert new_primary_key in [attr.get_name() for attr in self.attributes]
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

    def __str__(self):
        """
        String representation of the entity.
        e.g. 'Actor(__ActorID__ (anyType), Name (anyType), Age (int))'
        """
        non_key_attributes = [attr.__str__() for attr in self.attributes
                              if attr.get_name() not in self.primary_key]
        attributes_str = ", ".join(non_key_attributes)
        pk_str = ", ".join(("__" + pk.get_name() + "__"
                            + " (" + pk.get_data_type() + ")")
                           for pk in self.attributes
                           if pk.get_name() in self.primary_key)
        return "{}({}, {})".format(self.name, pk_str, attributes_str)
