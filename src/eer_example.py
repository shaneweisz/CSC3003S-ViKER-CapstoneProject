import eer
import eer_constraints
import sys


def eer_example():
    """Returns an example constructed EER Model.
    This example has a 1-to-many relationship"""
    EER = eer.EER_Model()

    entity = eer.EER_Entity("Professor")
    attribute = eer.EER_Attribute("name")
    entity.add_attribute(attribute)
    attribute2 = eer.EER_Attribute("pnum")
    entity.add_attribute(attribute2)
    constraint = eer_constraints.Identifier_Constraint(["pnum"])
    entity.add_constraint(constraint)
    EER.add_eer_entity(entity)

    ent2 = eer.EER_Entity("Department")
    ent2.add_attribute(eer.EER_Attribute("dcode"))
    ent2.add_attribute(eer.EER_Attribute("dname"))
    ent2.add_constraint(eer_constraints.Identifier_Constraint(["dcode"]))
    EER.add_eer_entity(ent2)

    rel = eer.EER_Relationship("Works",
                               "Professor", "Department",
                               ("1", "n"), ("1",),
                               False)
    EER.add_eer_relationship(rel)

    return EER


if __name__ == '__main__':
    n = sys.argv[1]
    if n == "1":
        eer_model = eer_example()
        print(eer_model)
        print(eer_model.transform_to_arm())
