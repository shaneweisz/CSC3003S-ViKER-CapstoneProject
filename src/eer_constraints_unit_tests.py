import eer_constraints as EC
import unittest2

class Tests(unittest2.TestCase):

    def test_Identifier_Constraint(self):
        constraint = EC.Identifier_Constraint(["pid", "name"])
        self.assertEqual(constraint.get_identifier()[0], "pid", "should be pid")
        self.assertEqual(constraint.get_identifier()[1], "name", "should be pid")

    def test_Inheritance_Constraint(self):
        constraint = EC.Inheritance_Constraint("Parent")
        self.assertEqual(constraint.get_parent(), "Parent", "should be Parent")

    def test_Cover_Constraint(self):
        constraint = EC.Cover_Constraint(["undergrad", "postgrad"])
        self.assertEqual(constraint.get_covered_by()[0], "undergrad", "should be undergrad")
        self.assertEqual(constraint.get_covered_by()[1], "postgrad", "should be postgrad")


if __name__ == '__main__':
    unittest2.main()
