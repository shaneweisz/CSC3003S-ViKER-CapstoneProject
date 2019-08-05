'''
The following function assumes the following (with get_[attribute]() methods
for each class attribute):

1) This function is a method in an EER_Model class.
2) The EER_Model class contains a list of EER_Entity and EER_Relationship
   objects:
        'entities' (list)
        'relationships' (list)
3) An EER_Entity object has the following attributes:
       'name' (string)
       'primary_key' (string)
       ^^^ NOTE: NOT LIST LIKE WE'D THOUGHT - CAN ONLY BE ONE IN EER ^^^
       'attributes' (list of EER_Attributes)
       'foreign_keys' (list of strings - with the appropriate attribute's name)
       'weak' (boolean)
       'parent' (EER_Entity)
4) An EER_Attribute object has the following attributes:
            'name' (str)
            'multivalued' (bool)
            'derived' (bool)
            'optional' (bool)
4) An EER_Relationship object has the following attributes:
        'name' (string)
        'entity1' (EER_Entity)
        'entity2' (EER_Entity)
        'multiplicity1' (string) e.g. '0..1', '1..n' etc.
        'multiplicity2' (string) e.g. '0..1', '1..n' etc.
        'attributes' (list of EER_Attributes)
        ^^^ NOTE: We forgot this in class diagram - a relationship can have its
                  own attributes ^^^
'''


def transform_to_arm(eer):
    """Applies the set of transformation rules for EER to ARM.

    Args:
        eer (EER_Model): An object representation of an EER Model.

    Returns:
        ARM: The corresponding ARM model resulting from the transformation
    """
    arm = ARM()        # will store the new ARM model
    arm_entities = []  # the entities that will compose the ARM model

    # Create the relations for entities
    for entity in eer.get_entities():
        name = entity.get_name()
        arm_entity = ARM_Entity(name)  # construct a new ARM entity e.g "Movie"

        for attribute in entity.get_attributes():
            arm_entity.add_attribute(attribute)  # e.g "Runtime"

        pk = entity.get_primary_key()
        arm_entity.add_primary_key(pk)  # e.g. "MovieID"

        arm.add_arm_entity(arm_entity)

    # Create the relations for relationships
    for relationship in eer.relationships:
        name = relationship.get_name()
        entity1 = relationship.get_entity1()
        entity2 = relationship.get_entity2()
        mult1 = relationship.get_multiplicity1()
        mult2 = relationship.get_multiplicity2()

        if 'n' not in mult1 and 'n' not in mult2:
            # Then one to one relationship
            # No need for a new relation - just add foreign key to one entity
            entity1_name = entity1.get_name()
            # Search for the corresponding ARM Entity
            victim_entity = "placeholder"
            for entity in arm_entities:
                if entity.get_name() == entity1_name:
                    victim_entity = entity
            # Add foreign key - the primary key of the other entity
            victim_entity.add_attribute(entity2.get_primary_key()[0])
        else:
            # One-to-many or many-to-many
            # Need a new relation
            pass

    return arm
