import xml.etree.ElementTree as ET
import arm
import constraints

class EER:
    """
    A class used to represent an EER Model in its entirity - a list of
    EER_Entity, EER_Relationship objects and appropriate methods.

    Attributes
    ----------
    eer_entities : list of EER_Entity
        The entities that together compose the EER Model.
    eer_relations : list of EER_Relationship
        The entities that together compose the relationships between the EER Model.

    Methods
    -------
    load_eer():
        Populates the EER model object from an XML file
    transform_to_arm():
        Applies the set of transformation rules for EER to ARM.
    save_to_xml():
        Saves the EER model object as an XML file
    """

    def __init__(self):
        """
        EER model constructor.
        Creates an EER model without any entities or relationships.
        Entities must be added with the `add_eer_entity()` method.
        Relationships must be added with the `add_eer_relationship()` method.
        """
        self.eer_entities = []
        self.eer_relationships = []

    def add_eer_entity(self, new_eer_entity):
        """
        Adds an EER_Entity to the model.

        Raises:
            AssertionError:
                if `new_arm_entity` supplied is not of type `EER_Entity`
        """

        assert type(new_eer_entity) == EER_Entity
        self.eer_entities.append(new_eer_entity)

    def add_eer_relationship(self, new_eer_relationship):
        """
        Adds an EER_Relationship to the model.

        Raises:
            AssertionError:
                if `new_eer_relationship` supplied is not of type `EER_Relationship`
        """
        assert type(new_eer_relationship) == EER_Relationship
        self.eer_relationships.append(new_eer_relationship)


    def load_eer(self, filename='../EER_XML_Schema/demo.xml'):
        """
        Loads and EER model from an XML file into a python object representation
        """
        tree = ET.parse(filename)
        root = tree.getroot()

        num_entities = len(root)
        for i in range(num_entities):

            if(root[i].attrib["type"] == "Entity"):
                entity = EER_Entity(root[i].attrib["name"])
                num_attributes = len(root[i])
                for j in range(num_attributes):
                    entity.add_attribute(EER_Attribute(root[i][j].text))
                    if(root[i][j].attrib["type"] == 'pk'):
                        entity.add_primary_key(EER_Attribute(root[i][j].text))
                self.add_eer_entity(entity)


            if(root[i].attrib["type"] == "Relationship"):
                relation = EER_Relationship(root[i].attrib["name"])
                relation.entity1 = root[i][0].text
                relation.mult1 = root[i][0].attrib["multiplicity"]
                relation.entity2 = root[i][1].text
                relation.mult2 = root[i][1].attrib["multiplicity"]
                self.add_eer_relationship(relation)

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
            arm_entity = arm.ARM_Entity(name)  # construct a new ARM entity e.g "Movie"
            arm_entity.add_attribute(arm.ARM_Attribute("self", "OID"))
            for eer_attr in eer_entity.get_attributes():
                arm_attr = arm.ARM_Attribute(eer_attr.get_name(), "anyType")
                arm_entity.add_attribute(arm_attr)  # e.g "Runtime (anyType)"

            # STEP B - Foreign Keys - done in the relationships section below

            # STEP C - Primary Key
            pk = eer_entity.get_primary_key()
            arm_entity.add_constraint(constraints.PK_Constraint("self"))  # e.g. "MovieID", and recall arm's primary key is a list # noqa
            arm_entity.add_constraint(constraints.Pathfd_Constraint((pk.get_name() for pk in eer_entity.get_primary_key()), "self"))
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
                victim_entity.add_attribute(arm.ARM_Attribute(entity2, "OID"))
                victim_entity.add_constraint(constraints.FK_Constraint(entity2, entity2))
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
                victim_entity.add_attribute(arm.ARM_Attribute(entity1, "OID"))
                victim_entity.add_constraint(constraints.FK_Constraint(entity1, entity1))
            else:
                pass

        return arm_model

    def __str__(self):
        """
        A textual representation of the ARM Model.
        """
        str_repr = "EER Model:"
        underline = "\n" + "-"*len(str_repr) + "\n"  # to underline 'EER Model'
        str_repr += underline
        str_repr += "\n".join(ent.__str__() for ent in self.eer_entities)
        str_repr += "\n"
        str_repr += "\n".join(rel.__str__() for rel in self.eer_relationships)
        return str_repr

class EER_Relationship:
    """
    A class used to represent an EER Relationship
    """
    def __init__(self, name):
        self.name = name
        self.entity1=""
        self.entity2=""
        self.mult1=""
        self.mult2=""

    def get_name(self):
        return self.name

    def get_entity1(self):
        return self.entity1

    def get_entity2(self):
        return self.entity2

    def get_mult1(self):
        return self.mult1

    def get_mult2(self):
        return self.mult2

    def __str__(self):
        result = self.name + ' [RELATIONSHIP]\n'
        result += self.entity1 + " " + "(" + self.mult1 + ")\n"
        result += self.entity2 + " " + "(" + self.mult2 + ")\n"
        return result

class EER_Entity:
    """
    A class used to represent an EER Entity
    - i.e. a relation/entity in an EER model.

    Attributes
    ----------
    name : str
        The name of the entity.
    primary_keys : list
        List of primary keys
    attributes : list
        List of attributes
    foreign_keys : list
        List of foreign_keys
    weak : bool
        If it is a weak EER entity
    """
    def __init__(self, name, weak=False):
        """
        Args:
            name (str): The name of the attribute
            primary_keys (list): List of primary keys
            attributes (list): List of EER attributes
            foreign_keys (list): List of foreign_keys
            weak (bool): If it is a weak EER entity
        """
        self.name = name
        self.primary_keys = []
        self.attributes = []
        self.foreign_keys = []
        self.weak = weak

    def add_attribute(self, attribute):
        self.attributes.append(attribute)

    def add_primary_key(self, primary_key):
        self.primary_keys.append(primary_key)

    def get_name(self):
        return self.name

    def get_primary_key(self):
        return self.primary_keys

    def get_attributes(self):
        return self.attributes

    def __str__(self): #needs to be restructured to allow for more than one primary key
        result = self.name + " [ENTITY]\n"
        for key in self.primary_keys:
            result += key.name + " [pk]\n"
            for attr in self.attributes:
                if(not attr.name == key.name):
                    result += attr.name + " [attr]\n"
        return result

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
        self.name = name
        self.multi_valued = multi_valued
        self.derived = derived
        self.optional = optional

    def get_name(self):
        return self.name
