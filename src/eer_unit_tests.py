import eer
import arm
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

    def test_LoadEER(self):
        #Test load_eer()
        EER = eer.EER()
        EER.load_eer()
        self.assertEqual(len(EER.eer_entities), 2, "Should be 2")
        self.assertEqual(EER.eer_entities[0].get_name(), "Professor", "Should be Professor")
        self.assertEqual(EER.eer_entities[0].attributes[0].get_name(), "pid", "Should be pid")
        self.assertEqual(EER.eer_entities[0].primary_keys[0].get_name(), "pid", "Should be pid")
        self.assertEqual(EER.eer_entities[0].attributes[1].get_name(), "pname", "Should be pname")
        self.assertEqual(EER.eer_entities[0].attributes[2].get_name(), "office", "Should be office")
        self.assertEqual(EER.eer_entities[1].get_name(), "Department", "Should be Department")
        self.assertEqual(EER.eer_entities[1].attributes[0].get_name(), "dcode", "Should be dcode")
        self.assertEqual(EER.eer_entities[1].primary_keys[0].get_name(), "dcode", "Should be dcode")
        self.assertEqual(EER.eer_entities[1].attributes[1].get_name(), "dname", "Should be dname")

        self.assertEqual(len(EER.eer_relationships), 1, "Should be 1")
        self.assertEqual(EER.eer_relationships[0].get_name(), "WORK", "Should be WORK")
        self.assertEqual(EER.eer_relationships[0].get_entity1(), "Professor", "Should be Professor")
        self.assertEqual(EER.eer_relationships[0].get_entity2(), "Department", "Should be Department")
        self.assertEqual(EER.eer_relationships[0].get_mult1(), "n", "Should be n")
        self.assertEqual(EER.eer_relationships[0].get_mult2(), "1", "Should be 1")
        print(EER)

if __name__ == '__main__':
    unittest2.main()
