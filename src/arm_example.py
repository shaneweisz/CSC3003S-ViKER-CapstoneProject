from arm import ARM_Model, ARM_Entity, ARM_Attribute
import arm_constraints


def arm_example():
    """Returns an example constructed ARM Model."""
    arm_model = ARM_Model()

    ent = ARM_Entity("Professor")
    ent.add_attribute(ARM_Attribute("self", "OID"))
    ent.add_attribute(ARM_Attribute("pnum", "INT"))
    ent.add_attribute(ARM_Attribute("pname", "STRING"))
    ent.add_attribute(ARM_Attribute("office", "STRING"))
    ent.add_attribute(ARM_Attribute("department", "OID"))
    ent.add_constraint(arm_constraints.PK_Constraint("self"))
    ent.add_constraint(arm_constraints.FK_Constraint("department", "department", "Department"))
    # ent.add_constraint(arm_constraints.Inheritance_Constraint("Person"))
    # ent.add_constraint(arm_constraints.Cover_Constraint(["Doctor", "Masters", "Other"]))
    # ent.add_constraint(arm_constraints.Disjointness_Constraint(["Student", "Cleaner"]))
    ent.add_constraint(arm_constraints.Pathfd_Constraint(["pnum"], "self"))

    arm_model.add_arm_entity(ent)
    ent2 = ARM_Entity("Department")
    ent2.add_attribute(ARM_Attribute("self", "OID"))
    ent2.add_constraint(arm_constraints.PK_Constraint("self"))
    ent2.add_attribute(ARM_Attribute("dcode", "INT"))
    ent2.add_attribute(ARM_Attribute("dname", "STRING"))
    ent2.add_constraint(arm_constraints.Pathfd_Constraint(["dcode"], "self"))
    arm_model.add_arm_entity(ent2)

    return arm_model


if __name__ == '__main__':
    arm_model = arm_example()
    print(arm_model)
    print(arm_model.transform_to_eer())
