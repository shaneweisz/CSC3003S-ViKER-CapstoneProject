import xml.etree.ElementTree as ET
import arm
import arm_constraints
import eer_constraints


class EER_Model:
    """
    A class used to represent an EER Model in its entirity - a list of
    EER_Entity, EER_Relationship objects and appropriate methods.

    Attributes
    ----------
    eer_entities : list of EER_Entity
        The entities that together compose the EER Model.
    eer_relationships : list of EER_Relationship
        The entities that together compose the relationships between the EER Model.

    Core Methods
    -------
    load_eer():
        Populates the EER model object from an XML file
    transform_to_arm():
        Applies the set of transformation rules for EER to ARM.
    """

    def __init__(self):
        """
        EER model constructor.
        Creates an EER model without any entities or relationships.
        Entities must be added with the `add_eer_entity()` method.
        Relationships must be added with the `add_eer_relationship()` method.
        """
        self.__eer_entities = []
        self.__eer_relationships = []

    def add_eer_entity(self, new_eer_entity):
        """
        Adds an EER_Entity to the model.

        Raises:
            AssertionError:
                if `new_arm_entity` supplied is not of type `EER_Entity`
        """

        assert type(new_eer_entity) == EER_Entity
        self.__eer_entities.append(new_eer_entity)

    def add_eer_relationship(self, new_eer_relationship):
        """
        Adds an EER_Relationship to the model.

        Raises:
            AssertionError:
                if `new_eer_relationship` supplied is not of type `EER_Relationship`
        """
        assert type(new_eer_relationship) == EER_Relationship
        self.__eer_relationships.append(new_eer_relationship)

    def load_eer(self, filename='../EER_XML_Schema/demo.xml'):
        """
        Loads and EER model from an XML file into a python object representation
        """
        tree = ET.parse(filename)
        root = tree.getroot()

        num_elements = len(root)
        for i in range(num_elements):
            if(root[i].attrib["type"] == "Entity"):
                entity = EER_Entity(root[i].attrib["name"])
                num_attributes = len(root[i])
                for j in range(num_attributes):
                    entity.add_attribute(EER_Attribute(root[i][j].text))

                self.add_eer_entity(entity)

            if(root[i].attrib["type"] == "Relationship"):
                relation = EER_Relationship(root[i].attrib["name"])
                relation.entity1 = root[i][0].text
                relation.mult1 = root[i][0].attrib["multiplicity"]
                relation.entity2 = root[i][1].text
                relation.mult2 = root[i][1].attrib["multiplicity"]
                self.add_eer_relationship(relation)

            if(root[i].attrib["type"] == "Constraint"):
                if(root[i][0].text == 'identifier'):
                    entity_name = root[i][1].text
                    self.find_entity(entity_name).add_identifier(EER_Attribute(root[i][2].text)) #Add identifier method no longer exists

    # def load_entity(self, entity):
    #     if(entity.attrib["weak"] == "True"):
    #         entity = EER_Entity(root[i].attrib["name"], True)
    #     else:
    #         entity = EER_Entity(root[i].attrib["name"], False)

    def find_entity(self, entity_name):
        """
        Used to find an entity that matches an entity name
        """
        for entity in self.eer_entities:
            if(entity_name == entity.get_name()):
                return entity

    def transform_to_arm(self):
        """Applies the set of transformation rules for EER to ARM.

        Returns:
            ARM: The ARM model resulting from the transformation from the
                 EER model given by `self`.
        """
        arm_model = arm.ARM_Model()        # will store the new ARM model

        # Create the relations for entities
        for eer_entity in self.eer_entities:
            # STEP A - Table Declaration

            name = eer_entity.get_name()
            arm_entity = arm.ARM_Entity(name)
            arm_entity.add_attribute(arm.ARM_Attribute("self", "OID"))
            for eer_attr in eer_entity.get_attributes():
                arm_attr = arm.ARM_Attribute(eer_attr.get_name(), "anyType")
                arm_entity.add_attribute(arm_attr)  # e.g "Runtime (anyType)"

            # STEP B - Foreign Keys - done in the relationships section below

            # STEP C - Identifier
            pk = eer_entity.get_identifier()
            arm_entity.add_constraint(arm_constraints.PK_Constraint("self"))  # e.g. "MovieID", and recall arm's identifier is a list # noqa
            arm_entity.add_constraint(arm_constraints.Pathfd_Constraint(
                (id.get_name() for id in eer_entity.get_identifiers()), "self"))
            arm_model.add_arm_entity(arm_entity)

        # Create the relations for relationships
        for relationship in self.eer_relationships:
            name = relationship.get_name()
            entity1 = relationship.get_entity1()
            entity2 = relationship.get_entity2()
            mult1 = relationship.get_mult1()
            mult2 = relationship.get_mult2()

            if (mult1 == "1" and mult2 == "1") or (mult1 == "n" and mult2 == "1"):
                # Then one to one, or many-to-one relationship
                # No need for a new relation - just add foreign key to first entity

                # Find the ARM_Entity object corresponding to the name entity1
                # This corresponds to the `n` side of the many-to-one relationship
                victim_entity = "placeholder"
                for ent in arm_model.get_arm_entities():
                    if ent.get_name() == entity1:
                        victim_entity = ent  # found the ARM entity to add the foreign key to

                assert victim_entity != "placeholder"  # checking a victim entity has been found
                # Add foreign key - the name of the other entity
                fk_name = entity2.lower()
                victim_entity.add_attribute(arm.ARM_Attribute(fk_name, "OID"))
                victim_entity.add_constraint(
                    arm_constraints.FK_Constraint(fk_name, fk_name, entity2))
            elif mult1 == "1" and mult2 == "n":
                # One-to-many relationship
                # Add foreign key to the entity on the n side of the relationship

                # Find the ARM_Entity object corresponding to the name entity2
                # This corresponds to the `n` side of the one-to-many relationship
                victim_entity = "placeholder"
                for ent in arm_entities:
                    if ent.get_name() == entity2:
                        victim_entity = ent

                assert victim_entity != "placeholder"  # checking a victim entity has been found
                # Add foreign key - the name of the other entity
                fk_name = entity1.lower()
                victim_entity.add_attribute(arm.ARM_Attribute(fk_name, "OID"))
                victim_entity.add_constraint(constraints.FK_Constraint(fk_name, fk_name, entity1))
            else:
                pass

        return arm_model

    def get_eer_entities(self):
        """Returns the list of EER Entities contained in the model"""
        return self.__eer_entities

    def get_eer_relationships(self):
        """Returns the list of EER Relationships contained in the model"""
        return self.__eer_relationships

    def __str__(self):
        """
        A textual representation of the EER Model.
        """
        str_repr = "EER Model:"
        # underline = "\n" + "-"*len(str_repr) + "\n"  # to underline 'EER Model'
        # str_repr += underline
        # str_repr += "\n".join(ent.__str__() for ent in self.eer_entities)
        # str_repr += "\n"
        # str_repr += "\n".join(rel.__str__() for rel in self.eer_relationships)
        return str_repr


class EER_Relationship:
    """
    A class used to represent an EER Relationship

    Attributes
    ----------
    name : str
        The name of the relationship.
    entity1 : tuple
        entity1 with its associated multiplicity
    entity2 : tuple
        entity2 with its associated multiplicity
    weak : bool
        If it is a weak EER Relationship
    """

    def __init__(self, name, entity1, entity2, weak=False):
        assert(type(entity1) == tuple)
        assert(type(entity2) == tuple)
        self.__name = name
        self.__entity1 = entity1
        self.__entity2 = entity2
        self.__weak = weak

    def get_name(self):
        """Get the name of the relationship"""
        return self.__name

    def get_entity1(self):
        """Returns entity1 with it's associated multiplicity"""
        return self.__entity1

    def get_entity2(self):
        """Returns entity2 with it's associated multiplicity"""
        return self.__entity2

    def is_weak(self):
        """Check if it is a weak relationship"""
        return self.__weak

    def __str__(self):
        """A textual representation of an EER Relationship"""
        relationship = "RELATIONSHIP: [relationship_name = {}] [weak = {}]".format(self.__name, self.__weak)
        underline = "\n" + "-"*len(relationship) + "\n"
        relationship += underline
        relationship += "Entity1: [entity_name = {}] [multiplicity = {}]\n".format(self.__entity1[0], self.__entity1[1])
        relationship += "Entity2: [entity_name = {}] [multiplicity = {}]".format(self.__entity2[0], self.__entity2[1])
        return relationship

class EER_Entity:
    """
    A class used to represent an EER Entity
    - i.e. a relation/entity in an EER model.

    Attributes
    ----------
    name : str
        The name of the entity.
    constraints : list of Constraint objects
        List of constraints on the entity
    attributes : list
        List of attributes
    weak : bool
        If it is a weak EER entity
    """

    def __init__(self, name, weak=False):
        """
        Attributes:
            name (str): The name of the attribute
            weak (bool): If it is a weak EER entity
            attributes (list): List of EER attributes
            constraints (list): List of constraints
        """
        self.__name = name
        self.__weak = weak
        self.__attributes = []
        self.__constraints = []

    def get_name(self):
        """Returns the entity name"""
        return self.__name

    def is_weak(self):
        """Check if the entity is weak"""
        return self.__weak

    def add_attribute(self, attribute):
        """Add an attribute to the entity"""
        self.__attributes.append(attribute)

    def get_attributes(self, index=-1):
        """
        Returns a list of all the attributes unless an index is supplied,
        in which case on the attribute at that index is returned
        """
        if(index == -1):
            return self.__attributes
        return self.__attributes[index]

    def add_constraint(self, constraint):
        """Add a constraint on the entity"""
        assert(len(self.__constraints) <= 2)
        self.__constraints.append(constraint)

    def get_identifier(self):
        """
        Get the identifier(s) constraint on the entity
        Returns a str list in format ["identifier1", "identifier2", etc...]
        """
        for constraint in self.__constraints:
            identifiers = []
            if(type(constraint) == eer_constraints.Identifier_Constraint):
                identifiers = constraint.get_identifier()
            return identifiers

    def is_inherited_from(self):
        """
        Checks if the entity has any children
        Returns True if it has children, otherwise False
        """
        has_children = False
        for constraint in self.__constraints:
            if(type(constraint) == eer_constraints.Inheritance_Constraint):
                has_children = True
        return has_children

    def get_inheritance_constraint(self):
        """
        Returns the Inheritance Constraint object associated with this entity1
        NOTE - this method should only be called after checking if the entity is
        inherited from by calling the is_inherited_from() method first
        """
        assert(self.is_inherited_from())
        for constraint in self.__constraints:
            if(type(constraint) == eer_constraints.Inheritance_Constraint):
                return constraint

    def __str__(self):
        """A textual representation of an EER Entity"""
        entity = "ENTITY: [entity_name = {}] [weak = {}]".format(self.__name, self.__weak)
        underline = "\n" + "-"*len(entity) + "\n"
        entity += underline
        for attribute in self.__attributes:
            entity += str(attribute) + "\n"
        for constraint in self.__constraints:
            entity += str(constraint) + "\n"
        return entity

class EER_Attribute:
    """
    A class used to represent an attribute of an EER Entity.

    Attributes
    ----------
    name : str
        The name of the attribute.
    multi_valued : bool
        Whether or not the attribute has multiple values
    derived : bool
        Whether or not the attribute is derived
    optional : bool
        Whether or not the attribute is optional
    """

    def __init__(self, name, multi_valued=False, derived=False, optional=False):
        """
        Args:
            name (str): The name of the attribute.
            multi_valued (bool): whether or not the attribute has multiple values.
            derived (bool): whether or not the attribute is derived.
            optional (bool): whether or not the attribute is optional.
        """
        self.__name = name
        self.__multi_valued = multi_valued
        self.__derived = derived
        self.__optional = optional

    def get_name(self):
        """Returns the attribute name"""
        return self.__name

    def is_multi_valued(self):
        """Check if the attribute has multiple values"""
        return self.__multi_valued

    def is_derived(self):
        """Check if the attribute is derived"""
        return self.__derived

    def is_optional(self):
        """Check if the attribute is optional"""
        return self.__optional

    def __str__(self):
        """A textual representation of an EER Attribute"""
        return "Attribute: [attr_name = {}] [multi-valued = {}] [derived = {}] [optional = {}]".format(self.__name, self.__multi_valued, self.__derived, self.__optional)
