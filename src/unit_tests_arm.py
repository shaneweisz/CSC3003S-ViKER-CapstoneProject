import arm_constraints
import arm
import unittest2


class Tests(unittest2.TestCase):

    def test_ARM_Attribute(self):
        # Test ARM_Attribute() that has a data type
        attribute = arm.ARM_Attribute("pnum", "INT")
        self.assertEqual(attribute.get_name(), "pnum", "Should be pnum")
        self.assertEqual(attribute.get_data_type(), "INT", "Should be INT")

        # Test ARM_Attribute() when no data type supplied
        attribute = arm.ARM_Attribute("pnum")
        self.assertEqual(attribute.get_name(), "pnum", "Should be pnum")
        self.assertEqual(attribute.get_data_type(), "anyType",
                         "Should be anyType")

    def test_Constraints(self):
        # Test PK_Constraint()
        pk_constraint = arm_constraints.PK_Constraint("self")
        self.assertEqual(pk_constraint.get_pk(), "self", "Should be self")

        # Test FK_Constraint()
        fk_constraint = arm_constraints.FK_Constraint("dept", "department", "Department")
        self.assertEqual(fk_constraint.get_name(), "dept", "Should be dept")
        self.assertEqual(fk_constraint.get_fk(), "department", "Should be department")
        self.assertEqual(fk_constraint.get_references(), "Department",
                         "Should be Department")

        # Test Inheritance_Constraint()
        inher_constraint = arm_constraints.Inheritance_Constraint("Person")
        self.assertEqual(inher_constraint.get_parent(), "Person",
                         "Should be Person")

        # Test Cover_Constraint()
        covered_by = ["Student", "Lecturer"]
        cover_constraint = arm_constraints.Cover_Constraint(covered_by)
        self.assertEqual(cover_constraint.get_covered_by(), covered_by,
                         "Should be [\"Student\", \"Lecturer\"]")

        # Test Disjointness_Constraint()
        disjoint_with = ["Student", "Lecturer"]
        d_constraint = arm_constraints.Disjointness_Constraint(disjoint_with)
        self.assertEqual(d_constraint.get_disjoint_with(), disjoint_with,
                         "Should be [\"Student\", \"Lecturer\"]")

        # Test Pathfd_Constraint()
        pathfd_constraint = arm_constraints.Pathfd_Constraint(
            ["pnum, name"], "self")
        self.assertEqual(pathfd_constraint.get_attributes(), ["pnum, name"],
                         "Should be [\"pnum\", \"name\"]")
        self.assertEqual(pathfd_constraint.get_target(), "self",
                         "Should be self")

    def test_ARM_Entity(self):
        # Test ARM_Entity()
        ent = arm.ARM_Entity("Professor")
        self.assertEqual(ent.get_name(), "Professor", "Should be Professor")

        # Test add_attribute()
        attribute = arm.ARM_Attribute("pnum", "INT")
        ent.add_attribute(attribute)
        self.assertEqual(ent.get_attributes()[0].get_name(), "pnum",
                         "Should be pnum")
        self.assertEqual(ent.get_attributes()[0].get_data_type(), "INT",
                         "Should be INT")

        # Test add_constraint()
        pk_constraint = arm_constraints.PK_Constraint("self")
        ent.add_constraint(pk_constraint)
        self.assertEqual(ent.get_constraints()[0].get_pk(), "self",
                         "Should be self")

    def test_ARM_Model(self):
        # Test add_arm_entity()
        arm_model = arm.ARM_Model()
        ent = arm.ARM_Entity("Professor")
        arm_model.add_arm_entity(ent)
        self.assertEqual(arm_model.get_arm_entities()[0].get_name(),
                         "Professor", "Should be Professor")


if __name__ == '__main__':
    unittest2.main()
