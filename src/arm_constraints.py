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
    name : str
        The name for the foreign key
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
        return self.name

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
        return "constraint {} foreign key ({}) references {}".format(self.name,
                                                                     self.fk,
                                                                     self.references)


class Inheritance_Constraint(Constraint):
    """
    A class used to represent an inheritance constraint in an ARM_Entity.

    Attributes
    ----------
    parent : str
        The name of the parent entity
    """

    def __init__(self, parent):
        self.parent = parent

    def get_parent(self):
        """Getter for the parent."""
        return self.parent

    def __str__(self):
        """
        String representation of the inheritance constraint.
        e.g. 'isa Person'
        """
        return "isa {}".format(self.parent)


class Cover_Constraint(Constraint):
    """
    A class used to represent a cover constraint in an ARM_Entity.

    Attributes
    ----------
    covered_by : list of str
        The name of the entities that this entity is covered by.
    """

    def __init__(self, covered_by):
        self.covered_by = covered_by

    def get_covered_by(self):
        """Getter for the covered_by."""
        return self.covered_by

    def __str__(self):
        """
        String representation of the cover constraint.
        e.g. 'covered by (Student, Lecturer)'
        """
        cov_str = ", ".join(self.covered_by)
        return "covered by ({})".format(cov_str)


class Disjointness_Constraint(Constraint):
    """
    A class used to represent a disjointess constraint in an ARM_Entity.

    Attributes
    ----------
    disjoint_with : list of str
        The name of the entities that this entity is disjoint with.
    """

    def __init__(self, disjoint_with):
        self.disjoint_with = disjoint_with

    def get_disjoint_with(self):
        """Getter for the disjoint_with."""
        return self.disjoint_with

    def __str__(self):
        """
        String representation of the disjointness constraint.
        e.g. 'disjoint with (Student, Lecturer)'
        """
        dis_str = ", ".join(self.disjoint_with)
        return "disjoint with ({})".format(dis_str)


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
