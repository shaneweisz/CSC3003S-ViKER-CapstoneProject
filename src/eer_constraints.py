import eer


class Constraint:
    """
    A class used to represent a constraint in an EER_Entity.
    Acts as an abstract class - it is never itself instantiated, instead
    the Identifier_Constraint, Inheritance_Constraint etc. classes below inherit from this
    class and are themselves instantiated.
    """

    def __str__(self):
        return "Constraint object"


class Identifier_Constraint(Constraint):
    """
    A class used to represent an identifier constraint in an EER_Entity.

    Attributes
    ----------
    identifier : list of str
        The name of the EER Attribute/s that forms the identifier
    """

    def __init__(self, identifier):
        assert(type(identifier) == list)
        self.__identifier = identifier

    def get_identifier(self):
        """Getter for the identifier."""
        return self.__identifier

    def __str__(self):
        """
        String representation of the identifier constraint.
        e.g. 'identifier (self)'
        """
        return "identifier ({})".format(self.__identifier)


class Inheritance_Constraint(Constraint):
    """
    A class used to represent an inheritance constraint in an EER_Entity.

    Attributes
    ----------
    parent : str
        The name of the parent entity
    """

    def __init__(self, parent_name):
        self.__parent = parent_name

    def get_parent(self):
        """Getter for the parent."""
        return self.__parent

    def __str__(self):
        """
        String representation of the inheritance constraint.
        e.g. 'isa Person'
        """
        return "isa {}".format(self.__parent)


class Cover_Constraint(Constraint):
    """
    A class used to represent a cover constraint in an EER_Entity.

    Attributes
    ----------
    covered_by : list of str
        The name of the entities that this entity is covered by.
    """

    def __init__(self, covered_by):
        assert(type(covered_by) == list)
        self.__covered_by = covered_by

    def get_covered_by(self):
        """Getter for the covered_by."""
        return self.__covered_by

    def __str__(self):
        """
        String representation of the cover constraint.
        e.g. 'covered by (Student, Lecturer)'
        """
        cov_str = ", ".join(self.__covered_by)
        return "covered by ({})".format(cov_str)


class Disjointness_Constraint(Constraint):
    """
    A class used to represent a disjointess constraint in an EER_Entity.

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
