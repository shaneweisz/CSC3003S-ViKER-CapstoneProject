import arm_constraints


class ARM_Model:
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
        Applies the set of transformation rules for ARM to EER.
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
        underline = "\n" + "-"*len(str_repr) + "\n"  # to underline 'ARM Model'
        str_repr += underline
        str_repr += "\n".join(ent.__str__() for ent in self.arm_entities)
        return str_repr


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
    constraints : list of Constraint
        The constraints of the entity - such as a PK_Constraint,
        FK_Constraint etc.
    """

    def __init__(self, name):
        """
        Constructs an ARM Entity without any attributes.
        Attributes must be added with the `add_attribute()` method.
        Constraints must be added with the `add_constraint()` method.

        Args:
            name (str): The name of the entity.
        """
        self.name = name
        self.attributes = []
        self.constraints = []

    def add_attribute(self, new_attribute):
        """Adds an ARM_Attribute to the entity.

        Raises:
            AssertionError:
                if `new_attribute` supplied is not of type `ARM_Attribute`
        """
        assert type(new_attribute) == ARM_Attribute
        self.attributes.append(new_attribute)

    def add_constraint(self, new_constraint):
        """Adds a Constraint to the entity.

        Raises:
            AssertionError:
                if `new_constraint` supplied is not of type `Constraint`
        """
        assert isinstance(new_constraint, arm_constraints.Constraint)
        self.constraints.append(new_constraint)

    def get_name(self):
        """Getter for name."""
        return self.name

    def get_attributes(self):
        """Getter for attributes."""
        return self.attributes

    def get_constraints(self):
        """Getter for constraints."""
        return self.constraints

    def __str__(self):
        """
        String representation of the entity.
        e.g.
        'Professor:
            Attributes:
                self OID
                pnum INT
                pname STRING
                office STRING
                department OID
            Constraints:
                primary key (self)'
        """
        str_repr = "{}:\n".format(self.name)
        str_repr += "  Attributes:\n"
        for attr in self.attributes:
            str_repr += "      {}\n".format(attr.__str__())
        str_repr += "  Constraints:\n"
        for con in self.constraints:
            str_repr += "      {}\n".format(con.__str__())
        return str_repr


class ARM_Attribute:
    """
    A class used to represent an attribute of an ARM Entity.

    Attributes
    ----------
    name : str
        The name of the attribute.
    data_type : str
        The data type of the attribute - defaulted to anyType.
    """

    def __init__(self, name, data_type="anyType"):
        """
        Args:
            name (str): The name of the attribute.
            data_type (str): Optional data type of the attribute.
                             Defaults to 'anyType' if no alternative provided.
        """
        self.name = name
        self.data_type = data_type

    def get_name(self):
        """Getter for name."""
        return self.name

    def get_data_type(self):
        """Getter for data type."""
        return self.data_type

    def __str__(self):
        """
        String representation of the attribute - its name and data type.
        e.g. 'age (INT)'
        """
        return "{} ({})".format(self.name, self.data_type)
