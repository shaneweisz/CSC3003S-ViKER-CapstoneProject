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

    def __init__(self, parent_name, disjoint, covering):
        """
        Disjoint and covering are booleans declaring whether the
        relationship meets those constraints
        """
        self.__parent = parent_name
        self.__disjoint = disjoint
        self.__covering = covering

    def get_parent(self):
        """Getter for the parent."""
        return self.__parent

    def is_disjoint(self):
        return self.__disjoint

    def is_covering(self):
        return self.__covering

    def __str__(self):
        """
        String representation of the inheritance constraint.
        e.g. 'isa Person'
        """
        return "isa {}".format(self.__parent)
