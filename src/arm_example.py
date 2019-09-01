from arm import ARM_Model, ARM_Entity, ARM_Attribute
import arm_constraints


def arm_example():
    """Returns an example constructed ARM Model.
    This example has a 1-to-many relationship"""
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


def arm_example2():
    """Returns a second example constructed ARM Model.
       This one has a many-to-many relationship between Suppliers and Parts"""
    arm_model = ARM_Model()

    ent = ARM_Entity("Supplier")
    ent.add_attribute(ARM_Attribute("self", "OID"))
    ent.add_attribute(ARM_Attribute("sname", "STRING"))
    ent.add_constraint(arm_constraints.PK_Constraint("self"))
    ent.add_constraint(arm_constraints.Pathfd_Constraint(["sname"], "self"))
    arm_model.add_arm_entity(ent)

    ent2 = ARM_Entity("Part")
    ent2.add_attribute(ARM_Attribute("self", "OID"))
    ent2.add_attribute(ARM_Attribute("PID", "INT"))
    ent2.add_constraint(arm_constraints.PK_Constraint("self"))
    ent2.add_constraint(arm_constraints.Pathfd_Constraint(["PID"], "self"))
    arm_model.add_arm_entity(ent2)

    ent3 = ARM_Entity("Supplies")
    ent3.add_attribute(ARM_Attribute("self", "OID"))
    ent3.add_attribute(ARM_Attribute("sname", "OID"))
    ent3.add_attribute(ARM_Attribute("PID", "OID"))
    ent3.add_constraint(arm_constraints.PK_Constraint("self"))
    ent3.add_constraint(arm_constraints.Pathfd_Constraint(["sname", "PID"], "self"))
    ent3.add_constraint(arm_constraints.FK_Constraint("sname", "sname", "Supplier"))
    ent3.add_constraint(arm_constraints.FK_Constraint("pid", "PID", "Part"))
    arm_model.add_arm_entity(ent3)

    return arm_model


def arm_example3():
    """Returns a third example constructed ARM Model.
       This one has a weak entity relationship between Loan and Payment"""
    arm_model = ARM_Model()

    ent = ARM_Entity("Payment")
    ent.add_attribute(ARM_Attribute("self", "OID"))
    ent.add_attribute(ARM_Attribute("LID", "OID"))
    ent.add_attribute(ARM_Attribute("paytime", "DATE"))
    ent.add_attribute(ARM_Attribute("amt", "INT"))
    ent.add_attribute(ARM_Attribute("type", "STRING"))
    ent.add_constraint(arm_constraints.PK_Constraint("self"))
    ent.add_constraint(arm_constraints.Pathfd_Constraint(["LID", "paytime"], "self"))
    ent.add_constraint(arm_constraints.FK_Constraint("LID", "LID", "Loan"))
    arm_model.add_arm_entity(ent)

    ent2 = ARM_Entity("Loan")
    ent2.add_attribute(ARM_Attribute("self", "OID"))
    ent2.add_attribute(ARM_Attribute("LID", "OID"))
    ent2.add_attribute(ARM_Attribute("other", "STRING"))
    ent2.add_constraint(arm_constraints.PK_Constraint("self"))
    ent2.add_constraint(arm_constraints.Pathfd_Constraint(["LID"], "self"))
    arm_model.add_arm_entity(ent2)

    return arm_model


if __name__ == '__main__':
    arm_model = arm_example3()
    print(arm_model)
    print(arm_model.transform_to_eer(debug=False))
