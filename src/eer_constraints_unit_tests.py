import eer_constraints as EC
import unittest2

class Tests(unittest2.TestCase):

    def test_Identifier_Constraint(self):
        constraint = EC.Identifier_Constraint(["pid", "name"])
        self.assertEqual(constraint.get_identifier()[0], "pid", "should be pid")
        self.assertEqual(constraint.get_identifier()[1], "name", "should be pid")

    def test_Inheritance_Constraint(self):
        constraint = EC.Inheritance_Constraint("Parent", True, False)
        self.assertEqual(constraint.get_parent(), "Parent", "should be Parent")
        self.assertEqual(constraint.is_disjoint(), True,  "should be True")
        self.assertEqual(constraint.is_covering(), False, "should be False")


if __name__ == '__main__':
    unittest2.main()
