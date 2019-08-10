import xml.etree.ElementTree as ET

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
        # self.eer_relations = []

    def add_eer_entity(self, new_eer_entity):
        """
        Adds an EER_Entity to the model.

        Raises:
            AssertionError:
                if `new_arm_entity` supplied is not of type `EER_Entity`
        """

        assert type(new_eer_entity) == EER_Entity
        self.eer_entities.append(new_eer_entity)

    #Relationship code, to be implemented
    # def add_eer_relationship(self, new_eer_relationship):
    #     """
    #     Adds an EER_Relationship to the model.
    #
    #     Raises:
    #         AssertionError:
    #             if `new_eer_relationship` supplied is not of type `EER_Relationship`
    #     """
    #     assert type(new_eer_relationship) == EER_Relationship
    #     self.eer_entities.append(new_eer_entity)


    def load_eer(self, filename='../EER_XML_Schema/demo.xml'):
        """
        TO DO
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
                self.add_eer_entity(entity)

            #Relationship code, to be implemented
            # if(root[i].attrib["type"] == "Relationship"):
            #     print("\nRelationship:", root[i].attrib["name"])
            #     for j in range(2): #Loop through 2 multiplicities
            #         print("Multiplicity:", root[i][j].attrib["multiplicity"], root[i][j].text)

    def transform_to_arm(self):
        """
        """

    def save_to_xml(self):
        """
        TO DO
        """

#Relationship code, to be implemented
# class EER_Relationship:
#     """
#     """

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
