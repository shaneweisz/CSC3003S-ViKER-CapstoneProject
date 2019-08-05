'''
The following function assumes the following:

1) It is a method in an EER_Model class.
2) The EER_Model class contains a list of EER_Entity and EER_Relationship
   objects.
3) An EER_Entity object has the following attributes:
        'primary_key' (list)
        'attributes' (list)
4) An EER_Relationship object has the following attributes:
        'name' (string)
        'entity1' (EER_Entity)
        'entity2' (EER_Entity)
        'multiplicity1' (string) e.g. '0..1', '1..*' etc.
        'multiplicity2' (string) e.g. '0..1', '1..*' etc.
'''


def transform_to_arm(eer):
    """Applies the set of transformation rules for EER to ARM.

    Args:
        eer (EER_Model): An object representation of an EER Model.

    Returns:
        ARM_Model: The corresponding ARM model resulting from the
                   transformation
    """
