import eer
import unittest2

class Tests(unittest2.TestCase):

    def test_EERAttribute(self):
        #Test EER_Attribute()
        attribute = eer.EER_Attribute("name")
        self.assertEqual(attribute.name, "name", "Should be name")
        self.assertEqual(attribute.multi_valued, False, "Should be False")
        self.assertEqual(attribute.derived, False, "Should be False")
        self.assertEqual(attribute.optional, False, "Should be False")

    def test_EEREntity(self):
        #Test EER_Entity()
        entity = eer.EER_Entity("Professor")
        self.assertEqual(entity.name, "Professor", "Should be Professor")
        #Test add_attribute()
        attribute = eer.EER_Attribute("name")
        entity.add_attribute(attribute)
        self.assertEqual(entity.attributes[0].name, "name", "Should be name")

    def test_EER(self):
        #Test add_eer_entity()
        EER = eer.EER()
        entity = eer.EER_Entity("Professor")
        EER.add_eer_entity(entity)
        self.assertEqual(EER.eer_entities[0].name, "Professor", "Should be Professor")

if __name__ == '__main__':
    unittest2.main()
