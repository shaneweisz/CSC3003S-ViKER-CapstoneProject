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
    A class used to represent a primary key constraint in an ARM_Entity.

    Attributes
    ----------
    name : str
        The name of the foreign key
    fk : str
        The name of the ARM Attribute that forms the foreign key
    references : str
        The name of the ARM Entity that the foreign key references
    """

    def __init__(self, name, fk, references):
        self.name = name
        self.fk = fk
        self.references = references

    def get_name(self):
        """Getter for the name."""
        return self.pk

    def get_fk(self):
        """Getter for the foreign key."""
        return self.pk

    def get_references(self):
        """Getter for the table the fk references."""
        return self.pk

    def __str__(self):
        """
        String representation of the foreign key constraint.
        e.g. 'constraint dept foreign key (department) references department'
        """
        return "constraint {} foreign key ({}) references {}".format(self.name, self.fk, self.references)


class pathfd_Constraint(Constraint):
    pass
