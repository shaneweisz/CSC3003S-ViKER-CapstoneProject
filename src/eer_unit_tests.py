import eer
import arm
import eer_constraints
import unittest2


class Tests(unittest2.TestCase):

    def test_EERAttribute(self):
        # Test EER_Attribute()
        attribute = eer.EER_Attribute("name", False, False, True)
        self.assertEqual(attribute.get_name(), "name", "Should be name")
        self.assertEqual(attribute.is_multi_valued(), False, "Should be False")
        self.assertEqual(attribute.is_derived(), False, "Should be False")
        self.assertEqual(attribute.is_optional(), True, "Should be True")

    def test_EEREntity(self):
        # Test EER_Entity()
        entity = eer.EER_Entity("Professor", True)
        self.assertEqual(entity.get_name(), "Professor", "Should be Professor")
        # Test constructor and is_weak() and set_weak()
        self.assertEqual(entity.is_weak(), True, "Should be True")
        entity.set_weak(False)
        self.assertEqual(entity.is_weak(), False, "Should be False")
        # Test add_attribute() and get_attributes()
        attribute = eer.EER_Attribute("name")
        entity.add_attribute(attribute)
        self.assertEqual(entity.get_attributes(0).get_name(), "name", "Should be name")
        attribute2 = eer.EER_Attribute("pid")
        entity.add_attribute(attribute2)
        self.assertEqual(len(entity.get_attributes()), 2, "Should be 2")
        # Test add_constraint() and get_identifier()
        self.assertEqual(entity.get_identifier(), None, "Should be None")
        constraint = eer_constraints.Identifier_Constraint(["pid", "name"])
        entity.add_constraint(constraint)
        self.assertEqual(entity.get_identifier()[0], "pid", "Should be pid")
        self.assertEqual(entity.get_identifier()[1], "name", "Should be name")
        # Test get_inheritance_constraint()
        inheritance_constraint = entity.get_inheritance_constraint()
        self.assertEqual(inheritance_constraint.is_disjoint(), True, "Should be True")
        self.assertEqual(inheritance_constraint.is_covering(), False, "Should be False")

    def test_EER_Relationship(self):
        relationship = eer.EER_Relationship("WORK",
                                            "Professor", "Department",
                                            ("0", "n"),  ("1",),
                                            True)
        # Test get_name()
        self.assertEqual(relationship.get_name(), "WORK", "Should be WORK")
        # Test get_entities()
        self.assertEqual(relationship.get_entity1(), "Professor", "Should be Professor")
        self.assertEqual(relationship.get_entity2(), "Department",
                         "Should be Department")
        self.assertEqual(relationship.get_mult1(), ("0", "n"), "Should be (\"0\", \"n\")")
        self.assertEqual(relationship.get_mult2(), ("1",), "Should be (\"1\",)")

        # Test is_weak()
        self.assertEqual(relationship.is_weak(), True, "Should be True")

    def test_EER_Model(self):
        # Test add_eer_entity() and get_eer_entities()
        EER = eer.EER_Model()
        entity = eer.EER_Entity("Professor")
        EER.add_eer_entity(entity)
        self.assertEqual(EER.get_eer_entities()[0].get_name(), "Professor", "Should be Professor")
        # Test add_eer_relationship() and get_eer_relationships()
        relationship = eer.EER_Relationship("WORK",
                                            "Professor", "Department",
                                            ("0", "n"),  ("1",),
                                            True)
        EER.add_eer_relationship(relationship)
        self.assertEqual(EER.get_eer_relationships()[0].get_name(), "WORK", "Should be WORK")

    def test_LoadEER(self):
        EER = eer.EER_Model()
        EER.load_eer()
        #Write tests once XML schema is finalised
        print(EER )

if __name__ == '__main__':
    unittest2.main()
