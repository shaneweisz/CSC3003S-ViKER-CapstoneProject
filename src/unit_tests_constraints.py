import eer_constraints as EC
import arm_constraints as AC
import unittest2


class Tests(unittest2.TestCase):

    #EER - Identifier Constraint
    def test_Identifier_Constraint(self):
        constraint = EC.Identifier_Constraint(["pid", "name"])
        self.assertEqual(constraint.get_identifier()[0], "pid", "should be pid")
        self.assertEqual(constraint.get_identifier()[1], "name", "should be pid")

    #EER - Inheritance Constraint
    def test_Inheritance_Constraint(self):
        constraint = EC.Inheritance_Constraint("Parent", True, False)
        self.assertEqual(constraint.get_parent(), "Parent", "should be Parent")
        self.assertEqual(constraint.is_disjoint(), True,  "should be True")
        self.assertEqual(constraint.is_covering(), False, "should be False")

    #ARM - PK Constraint
    def test_Pk_Constraint(self):
        constraint = AC.PK_Constraint("pid")
        self.assertEqual(constraint.get_pk(), "pid", "should be pid")

    #ARM - FK Constraint
    def test_FK_Constraint(self):
        constraint = AC.FK_Constraint("name", "fk", "references")
        self.assertEqual(constraint.get_name(), "name", "should be name")
        self.assertEqual(constraint.get_fk(), "fk", "should be fk")
        self.assertEqual(constraint.get_references(), "references", "should be references")

    #ARM - Inheritance Constraint
    def test_Inheritance_Constraint(self):
        constraint = AC.Inheritance_Constraint("parent")
        self.assertEqual(constraint.get_parent(), "parent", "should be parent")

    #ARM - Cover Constraint
    def test_Cover_Constraint(self):
        constraint = AC.Cover_Constraint(["x", "y"])
        self.assertEqual(constraint.get_covered_by()[0], "x", "should be x")
        self.assertEqual(constraint.get_covered_by()[1], "y", "should be x")
        self.assertEqual(len(constraint.get_covered_by()), 2, "should be 2")

    #ARM - Disjoint Constraint
    def test_Cover_Constraint(self):
        constraint = AC.Disjointness_Constraint(["x", "y"])
        self.assertEqual(constraint.get_disjoint_with()[0], "x", "should be x")
        self.assertEqual(constraint.get_disjoint_with()[1], "y", "should be x")
        self.assertEqual(len(constraint.get_disjoint_with()), 2, "should be 2")

    #ARM - Pathfd Constraint
    def test_Pathfd_Constraint(self):
        constraint = AC.Pathfd_Constraint(["x", "y"], "target")
        self.assertEqual(constraint.get_attributes()[0], "x", "should be x")
        self.assertEqual(constraint.get_attributes()[1], "y", "should be x")
        self.assertEqual(len(constraint.get_attributes()), 2, "should be 2")
        self.assertEqual(constraint.get_target(), "target", "should be target")

if __name__ == '__main__':
    unittest2.main()
