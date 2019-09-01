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
                self.load_entity(root[i])

            if(root[i].attrib["type"] == "Relationship"):
                self.load_relationship(root[i])

    def load_entity(self, entity_block):
        """
        Loads an EER entity from an XML file
        Helper method for the broader load_eer()
        """
        entity = EER_Entity(entity_block.attrib["name"],
                            self.parse_bool(entity_block.attrib["weak"]))
        entity_components = len(entity_block)
        for j in range(entity_components):
            if(entity_block[j].attrib["type"] == "attr"):
                attr_name = entity_block[j].text
                multi_valued = self.parse_bool(entity_block[j].attrib["multi_valued"])
                derived = self.parse_bool(entity_block[j].attrib["derived"])
                optional = self.parse_bool(entity_block[j].attrib["optional"])
                entity.add_attribute(EER_Attribute(attr_name, multi_valued, derived, optional))
            if(entity_block[j].attrib["type"] == "identifier"):
                identifier = [entity_block[j].text]
                id_constraint = eer_constraints.Identifier_Constraint(identifier)
                entity.add_constraint(id_constraint)
            if(entity_block[j].attrib["type"] == "inheritance"):
                parent = entity_block[j].text
                disjoint = self.parse_bool(entity_block[j].attrib["disjoint"])
                covering = self.parse_bool(entity_block[j].attrib["covering"])
                inherit_constraint = eer_constraints.Inheritance_Constraint(
                    parent, disjoint, covering)
                entity.add_constraint(inherit_constraint)
        self.add_eer_entity(entity)

    def load_relationship(self, relationship_block):
        """
        Loads an EER Relationship from an XML file
        Helper method for the broader load_eer()
        """
        relationship = EER_Relationship(relationship_block.attrib["name"])
        relationship.set_entity1(relationship_block[0].text)
        relationship.set_mult1(
            (relationship_block[0].attrib["mult_left"], relationship_block[0].attrib["mult_right"]))
        relationship.set_entity2(relationship_block[1].text)
        relationship.set_mult2(
            (relationship_block[1].attrib["mult_left"], relationship_block[1].attrib["mult_right"]))
        self.add_eer_relationship(relationship)

    def parse_bool(self, value):
        """Convert from string to boolean"""
        return value == "True"

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
        for eer_entity in self.__eer_entities:
            # STEP I: If the entity is 'strong'
            if not eer_entity.is_weak():
                # STEP I_A - Table Declaration

                name = eer_entity.get_name()
                arm_entity = arm.ARM_Entity(name)
                arm_entity.add_attribute(arm.ARM_Attribute("self", "OID"))
                for eer_attr in eer_entity.get_attributes():
                    arm_attr = arm.ARM_Attribute(eer_attr.get_name(), "anyType")
                    arm_entity.add_attribute(arm_attr)  # e.g "Runtime (anyType)"

                # STEP I_B - Foreign Keys - done in the relationships section below

                # STEP I_C - Primary Key

                # Extract the identifier
                pk = eer_entity.get_identifier()
                arm_entity.add_constraint(arm_constraints.PK_Constraint("self"))
                arm_entity.add_constraint(arm_constraints.Pathfd_Constraint(pk, "self"))
                arm_model.add_arm_entity(arm_entity)
            else:
                # STEP II: If the entity is 'weak'
                # STEP II_A - Table Declaration

                name = eer_entity.get_name()
                arm_entity = arm.ARM_Entity(name)
                arm_entity.add_attribute(arm.ARM_Attribute("self", "OID"))
                for eer_attr in eer_entity.get_attributes():
                    arm_attr = arm.ARM_Attribute(eer_attr.get_name(), "anyType")
                    arm_entity.add_attribute(arm_attr)  # e.g "Runtime (anyType)"

                # STEP II_B - Foreign Keys - done in the relationships section below

                # STEP II_C - Primary Key

                # Extract the PARTIAL identifier
                pk = eer_entity.get_identifier()
                arm_entity.add_constraint(arm_constraints.PK_Constraint("self"))
                arm_entity.add_constraint(arm_constraints.Pathfd_Constraint(pk, "self"))
                arm_model.add_arm_entity(arm_entity)

        # Create the relations for relationships
        for relationship in self.__eer_relationships:
            name = relationship.get_name()
            entity1 = relationship.get_entity1()
            entity2 = relationship.get_entity2()
            mult1 = relationship.get_mult1()
            mult2 = relationship.get_mult2()

            # Check for WEAK relationship
            # If so, extend the pathfd constraint of the WEAK entity beyond the partial identifier accordinly
            if relationship.is_weak():
                # We must first find whether it is entity1 or entity2 that is WEAK
                weak_entity = entity1  # assume it is entity1, then check if it is actually entity2
                for ent in self.__eer_entities:
                    if ent.get_name() == entity2 and ent.is_weak():
                        weak_entity = entity2

                for ent in arm_model.get_arm_entities():
                    if ent.get_name() == weak_entity:
                        victim_entity = ent
                        for constraint in victim_entity.get_constraints():
                            if type(constraint) == arm_constraints.Pathfd_Constraint:
                                if constraint.get_target() == 'self':
                                    # If here, we have found the appropriate Pathfd to edit
                                    if weak_entity == entity1:
                                        constraint.set_attributes(
                                            constraint.get_attributes() + [entity2.lower()])
                                    else:
                                        constraint.set_attributes(
                                            constraint.get_attributes() + [entity1.lower()])
                        break

            # Check that multiplicities exist, before we iterate over them using 'in' in the for loop below
            if mult1 is None or mult2 is None:
                continue

            if ("n" not in mult1 and "n" not in mult2) or ("n" in mult1 and "n" not in mult2):
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
                    arm_constraints.FK_Constraint(fk_name,
                                                  fk_name,
                                                  entity2))
            elif "n" not in mult1 and "n" in mult2:
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
        underline = "\n" + "-"*len(str_repr) + "\n"  # to underline 'EER Model'
        str_repr += underline
        str_repr += "\n"
        str_repr += "\n".join(ent.__str__() for ent in self.__eer_entities)
        str_repr += "\n"
        str_repr += "\n".join(rel.__str__() for rel in self.__eer_relationships)
        return str_repr


class EER_Relationship:
    """
    A class used to represent an EER Relationship

    Attributes
    ----------
    name : str
        The name of the relationship.
    entity1 : str
        The name of the first entity in the relationship.
    entity2 : str
        The name of the second entity in the relationship.
    mult1 : 2-tuple of str
        The multiplicity for entity 1 e.g. ("0", "n")
    mult2 : 2-tuple of str
        The multiplicity for entity 2 e.g. ("1",)
    weak : bool
        If it is a weak EER Relationship
    """

    def __init__(self, name, entity1=None, entity2=None, mult1=None, mult2=None, weak=False):
        self.__name = name
        self.__entity1 = entity1
        self.__entity2 = entity2
        self.__mult1 = mult1
        self.__mult2 = mult2
        self.__weak = weak

    def set_name(self, name):
        self.__name = name

    def set_entity1(self, entity1):
        self.__entity1 = entity1

    def set_entity2(self, entity2):
        self.__entity2 = entity2

    def set_mult1(self, mult1):
        self.__mult1 = mult1

    def set_mult2(self, mult2):
        self.__mult2 = mult2

    def set_weak(self, is_weak):
        """Set whether or not the entity is weak"""
        self.__weak = is_weak

    def get_name(self):
        """Get the name of the relationship"""
        return self.__name

    def get_entity1(self):
        """Returns entity1's name"""
        return self.__entity1

    def get_entity2(self):
        """Returns entity2's name'"""
        return self.__entity2

    def get_mult1(self):
        """Returns entity1's multiplicity"""
        return self.__mult1

    def get_mult2(self):
        """Returns entity2's multiplicity'"""
        return self.__mult2

    def is_weak(self):
        """Check if it is a weak relationship"""
        return self.__weak

    def __str__(self):
        """A textual representation of an EER Relationship"""
        relationship = "RELATIONSHIP: [relationship_name = {}] [weak = {}]".format(
            self.__name, self.__weak)
        underline = "\n" + "-"*len(relationship) + "\n"
        relationship += underline
        relationship += "Entity1: [entity_name = {}] [multiplicity = {}]\n".format(
            self.__entity1, self.__mult1)
        relationship += "Entity2: [entity_name = {}] [multiplicity = {}]".format(
            self.__entity2, self.__mult2)
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

    def set_weak(self, is_weak):
        """Set whether or not the entity is weak"""
        self.__weak = is_weak

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
        identifiers = None
        for constraint in self.__constraints:
            if(type(constraint) == eer_constraints.Identifier_Constraint):
                identifiers = constraint.get_identifier()
                break
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
