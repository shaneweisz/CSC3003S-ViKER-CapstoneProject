from arm import ARM_Model, ARM_Entity, ARM_Attribute
from constraints import PK_Constraint, FK_Constraint, Pathfd_Constraint


def arm_example():
    """Returns an example constructed ARM Model."""
    arm = ARM_Model()

    ent = ARM_Entity("professor")
    ent.add_attribute(ARM_Attribute("self", "OID"))
    ent.add_attribute(ARM_Attribute("pnum", "INT"))
    ent.add_attribute(ARM_Attribute("pname", "STRING"))
    ent.add_attribute(ARM_Attribute("office", "STRING"))
    ent.add_attribute(ARM_Attribute("department", "OID"))
    ent.add_constraint(PK_Constraint("self"))
    ent.add_constraint(Pathfd_Constraint(["pnum"], "self"))
    ent.add_constraint(FK_Constraint("department", "department"))

    arm.add_arm_entity(ent)
    ent2 = ARM_Entity("department")
    ent2.add_attribute(ARM_Attribute("self", "OID"))
    ent2.add_constraint(PK_Constraint("self"))
    ent2.add_attribute(ARM_Attribute("dcode", "INT"))
    ent2.add_attribute(ARM_Attribute("dname", "STRING"))
    arm.add_arm_entity(ent2)

    return arm


if __name__ == '__main__':
    print(arm_example())
