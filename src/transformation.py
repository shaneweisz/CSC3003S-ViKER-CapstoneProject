from constraints import PK_Constraint, FK_Constraint

'''
The following function assumes the following (with get_[attribute]() methods
for each class attribute):

1) This function is a method in an EER_Model class.
2) The EER_Model class contains a list of EER_Entity and EER_Relationship
   objects:
        'entities' (list of EER_Entity)
        'relationships' (list of EER_Relationships)
3) An EER_Entity object has the following attributes:
       'name' (string)
       'primary_key' (list)
       'attributes' (list of EER_Attribute)
       ^^^ THIS MUST INCLUDE THE PRIMARY KEY ABOVE ^^^
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
        'entity1' (string : name)
        'entity2' (string : name)
        'multiplicity1' (string) e.g. '1', 'n' etc.
        'multiplicity2' (string) e.g. '1', 'n' etc.
        'attributes' (list of EER_Attributes)
        ^^^ NOTE: We forgot this in class diagram - a relationship can have its
                  own attributes ^^^
'''


def transform_to_arm(self):
    """Applies the set of transformation rules for EER to ARM.

    Returns:
        ARM: The ARM model resulting from the transformation from the
             EER model given by `self`.
    """
    arm = ARM()        # will store the new ARM model
    arm_entities = []  # the entities that will compose the ARM model

    # Create the relations for entities
    for entity in self.entities:
        # STEP A - Table Declaration

        name = entity.get_name()
        arm_entity = ARM_Entity(name)  # construct a new ARM entity e.g "Movie"
        arm_entity.add_attribute("self", "OID")
        for attr_name in entity.get_attributes():
            arm_attr = new ARM_Attribute(attr_name, "anyType")
            arm_entity.add_attribute(arm_attr)  # e.g "Runtime (anyType)"

        # STEP B - Foreign Keys - done in the relationships section below

        # STEP C - Primary Key
        pk = entity.get_primary_key()
        arm_entity.add_constraint(PK_Constraint("self"))  # e.g. "MovieID", and recall arm's primary key is a list # noqa
        arm_entity.add_constraint(Pathfd_Constraint(entity.get_primary_key(), "self"))
        arm.add_arm_entity(arm_entity)

    # Create the relations for relationships
    for relationship in eer.relationships:
        name = relationship.get_name()
        entity1 = relationship.get_entity1()
        entity2 = relationship.get_entity2()
        mult1 = relationship.get_multiplicity1()
        mult2 = relationship.get_multiplicity2()

        if (mult1 == "1" and mult2 == "1") or (mult1 == "n" and mult2 == "1"):
            # Then one to one, or many-to-one relationship
            # No need for a new relation - just add foreign key to first entity

            # Find the ARM_Entity object corresponding to the name entity1
            victim_entity = "placeholder"
            for ent in arm_entities:
                if ent.get_name() == entity1:
                    victim_entity = ent

            assert victim_entity != "placeholder"  # checking a victim entity has been found
            # Add foreign key - the name of the other entity
            victim_entity.add_attribute(entity2, "OID")
            victim_entity.add_constraint(FK_Constraint(entity2, entity2))
        else if mult1 == "1" and mult2 == "n":
            # One-to-many relationship
            # Add foreign key to the entity on the n side of the relationship

            # Find the ARM_Entity object corresponding to the name entity2
            victim_entity = "placeholder"
            for ent in arm_entities:
                if ent.get_name() == entity2:
                    victim_entity = ent

            assert victim_entity != "placeholder"  # checking a victim entity has been found
            # Add foreign key - the name of the other entity
            victim_entity.add_attribute(entity1, "OID")
            victim_entity.add_constraint(FK_Constraint(entity1, entity1))
        else:
            pass

    return arm
