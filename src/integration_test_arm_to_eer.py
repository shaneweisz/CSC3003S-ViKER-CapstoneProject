import arm
import eer
import eer_constraints
import unittest2


class Tests(unittest2.TestCase):

    #A transformation from EER to ARM will be used with the sample file EER_PartSupplier as found in viker/EER_XML_Examples
    def test_EER_PartSupplierTransformation(self):
        ARM = arm.ARM_Model()
        ARM.load_arm("../ARM_XML_Examples/ARM_PartSupplier.xml")
        EER = ARM.transform_to_eer()
        self.assertEqual(len(EER.get_eer_entities()), 2, "Should be 3")
        self.assertEqual(len(EER.get_eer_relationships()), 1, "Should be 3")

        entities = EER.get_eer_entities()
        relationships = EER.get_eer_relationships()
        supplier = entities[0]
        part = entities[1]
        supplies = relationships[0]
        supplier_attributes = supplier.get_attributes()
        count = 0
        for attr in supplier_attributes:
            if(attr.get_name() == "sname"):
                count += 1
            if(attr.get_name() == "slocation"):
                count += 1
        self.assertEqual(count, 2, "Should be 2") #check that all of the above attributes were stored in the entity

        supplier_constraints = supplier.get_constraints()
        count = 0
        for constr in supplier_constraints:
            if(type(constr) == eer_constraints.Identifier_Constraint):
                self.assertEqual(constr.get_identifier()[0], "sname", "Should be sname")
                count += 1
        self.assertEqual(count, 1, "Should be 1") #check that all of the above constraints were stored in the entity

        part_attributes = part.get_attributes()
        count = 0
        for attr in part_attributes:
            if(attr.get_name() == "PID"):
                count += 1
            if(attr.get_name() == "pname"):
                count += 1
        self.assertEqual(count, 2, "Should be 2") #check that all of the above attributes were stored in the entity

        part_constraints = part.get_constraints()
        count = 0
        for constr in part_constraints:
            if(type(constr) == eer_constraints.Identifier_Constraint):
                self.assertEqual(constr.get_identifier()[0], "PID", "Should be PID")
                count += 1
        self.assertEqual(count, 1, "Should be 1") #check that all of the above constraints were stored in the entity

        supplies_attributes = supplies.get_attributes()
        count = 0
        for attr in supplies_attributes:
            if(attr.get_name() == "price"):
                count += 1
        self.assertEqual(count, 1, "Should be 1") #check that all of the above attributes were stored in the entity
        self.assertEqual(supplies.get_entity1(), "Supplier", "Should be Supplier")
        self.assertEqual(supplies.get_entity2(), "Part", "Should be Part")
        self.assertEqual(supplies.get_mult1(), ("0", "n"), "Should be 0, n")
        self.assertEqual(supplies.get_mult2(), ("0", "n"), "Should be 0, n")

if __name__ == '__main__':
    unittest2.main()
