from arm_entity import ARM_Entity
from arm_attribute import ARM_Attribute
from arm import ARM


def run_example():

    arm = ARM()

    ent = ARM_Entity("Movie")
    ent.add_attribute(ARM_Attribute("MovieID"))
    ent.add_primary_key("MovieID")
    ent.add_attribute(ARM_Attribute("Name", "string"))
    ent.add_attribute(ARM_Attribute("Director"))
    ent.add_attribute(ARM_Attribute("Runtime"))
    ent.add_attribute(ARM_Attribute("Genre"))
    # print(ent)
    arm.add_arm_entity(ent)

    ent2 = ARM_Entity("Actor")
    ent2.add_attribute(ARM_Attribute("ActorID"))
    ent2.add_primary_key("ActorID")
    ent2.add_attribute(ARM_Attribute("Name"))
    ent2.add_attribute(ARM_Attribute("Age", "int"))
    ent2.add_attribute(ARM_Attribute("Sex"))
    # print(ent2)
    arm.add_arm_entity(ent2)

    print(arm)


if __name__ == '__main__':
    run_example()
