import arm


class Constraint:
    """
    A class used to represent an constraint in an ARM_Entity.
    Acts as an abstract class - it is never itself instantiated, instead
    the PK_Constraint, FK_Constraint etc. classes below inherit from this
    class and are themselves instantiated.
    """

    def __str__(self):
        return "Constraint object"


class PK_Constraint(Constraint):
    """
    A class used to represent a primary key constraint in an ARM_Entity.

    Attributes
    ----------
    pk : str
        The name of the ARM Attribute that forms the primary key
    """

    def __init__(self, pk):
        self.pk = pk

    def get_pk(self):
        """Getter for the primary key."""
        return self.pk

    def __str__(self):
        """
        String representation of the primary key constraint.
        e.g. 'primary key (self)'
        """
        return "primary key ({})".format(self.pk)


class FK_Constraint(Constraint):
    """
    A class used to represent a foreign key constraint in an ARM_Entity.

    Attributes
    ----------
    fk : str
        The name of the ARM Attribute that forms the foreign key
    references : str
        The name of the ARM Entity that the foreign key references
    """

    def __init__(self, fk, references):
        self.fk = fk
        self.references = references

    def get_fk(self):
        """Getter for the foreign key."""
        return self.fk

    def get_references(self):
        """Getter for the table the fk references."""
        return self.references

    def __str__(self):
        """
        String representation of the foreign key constraint.
        e.g. 'foreign key (department) references department'
        """
        return "foreign key ({}) references {}".format(self.fk, self.references)


class Pathfd_Constraint(Constraint):
    """
    A class used to represent a pathfd constraint in an ARM_Entity.

    Attributes
    ----------
    attributes : list
        The attributes that together determine `target`
    target : str
        The name of the attribute that is determined by the fd
    """

    def __init__(self, attributes, target):
        self.attributes = attributes
        self.target = target

    def get_attributes(self):
        """Getter for the attribues."""
        return self.attributes

    def get_target(self):
        """Getter for the target."""
        return self.target

    def __str__(self):
        """
        String representation of the pathfd constraint.
        e.g. 'pathfd (pnum) -> self'
        """
        attr_str = ", ".join(self.attributes)
        return "pathfd ({}) -> {}".format(attr_str, self.target)
