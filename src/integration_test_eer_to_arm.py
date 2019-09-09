import arm
import eer
import arm_constraints
import unittest2


class Tests(unittest2.TestCase):

    #A transformation from EER to ARM will be used with the sample file EER_PartSupplier as found in viker/EER_XML_Examples
    def test_EER_PartSupplierTransformation(self):
        EER = eer.EER_Model()
        EER.load_eer("../EER_XML_Examples/EER_PartSupplier.xml")
        ARM = EER.transform_to_arm()

        self.assertEqual(len(ARM.get_arm_entities()), 3, "Should be 3")
        supplier = ARM.find_entity("Supplier")
        supplier_attributes = supplier.get_attributes()
        count = 0
        for attr in supplier_attributes:
            if(attr.get_name() == "self"):
                self.assertEqual(attr.get_data_type(), "OID", "Should be OID")
                count += 1
            if(attr.get_name() == "sname"):
                self.assertEqual(attr.get_data_type(), "anyType", "Should be anyType")
                count += 1
            if(attr.get_name() == "slocation"):
                self.assertEqual(attr.get_data_type(), "anyType", "Should be anyType")
                count += 1
        self.assertEqual(count, 3, "Should be 3") #check that all of the above attributes were stored in the entity

        supplier_constraints = supplier.get_constraints()
        count = 0
        for constr in supplier_constraints:
            if(type(constr) == arm_constraints.PK_Constraint):
                self.assertEqual(constr.get_pk(), "self", "Should be self")
                count += 1
            if(type(constr) == arm_constraints.Pathfd_Constraint):
                self.assertEqual(constr.get_target(), "self", "Should be self")
                self.assertEqual(constr.get_attributes()[0], "sname", "Should be sname")
                count += 1
            if(type(constr) == arm_constraints.Disjointness_Constraint):
                self.assertEqual(constr.get_disjoint_with()[0], "Part", "Should be Part")
                self.assertEqual(constr.get_disjoint_with()[1], "Supplies", "Should be Supplies")
                count += 1
        self.assertEqual(count, 3, "Should be 3") #check that all of the above constraints were stored in the entity

        part = ARM.find_entity("Part")
        part_attributes = part.get_attributes()
        count = 0
        for attr in part_attributes:
            if(attr.get_name() == "self"):
                self.assertEqual(attr.get_data_type(), "OID", "Should be OID")
                count += 1
            if(attr.get_name() == "PID"):
                self.assertEqual(attr.get_data_type(), "anyType", "Should be anyType")
                count += 1
            if(attr.get_name() == "pname"):
                self.assertEqual(attr.get_data_type(), "anyType", "Should be anyType")
                count += 1
        self.assertEqual(count, 3, "Should be 3") #check that all of the above attributes were stored in the entity

        part_constraints = part.get_constraints()
        count = 0
        for constr in part_constraints:
            if(type(constr) == arm_constraints.PK_Constraint):
                self.assertEqual(constr.get_pk(), "self", "Should be self")
                count += 1
            if(type(constr) == arm_constraints.Pathfd_Constraint):
                self.assertEqual(constr.get_target(), "self", "Should be self")
                self.assertEqual(constr.get_attributes()[0], "PID", "Should be PID")
                count += 1
            if(type(constr) == arm_constraints.Disjointness_Constraint):
                self.assertEqual(constr.get_disjoint_with()[0], "Supplier", "Should be Supplier")
                self.assertEqual(constr.get_disjoint_with()[1], "Supplies", "Should be Supplies")
                count += 1
        self.assertEqual(count, 3, "Should be 3") #check that all of the above constraints were stored in the entity

        supplies = ARM.find_entity("Supplies")
        supplies_attributes = supplies.get_attributes()
        count = 0
        for attr in supplies_attributes:
            if(attr.get_name() == "self"):
                self.assertEqual(attr.get_data_type(), "OID", "Should be OID")
                count += 1
            if(attr.get_name() == "supplier"):
                self.assertEqual(attr.get_data_type(), "anyType", "Should be anyType")
                count += 1
            if(attr.get_name() == "part"):
                self.assertEqual(attr.get_data_type(), "anyType", "Should be anyType")
                count += 1
            if(attr.get_name() == "price"):
                self.assertEqual(attr.get_data_type(), "anyType", "Should be anyType")
                count += 1
        self.assertEqual(count, 4, "Should be 4") #check that all of the above attributes were stored in the entity

        supplies_constraints = supplies.get_constraints()
        count = 0
        for constr in supplies_constraints:
            if(type(constr) == arm_constraints.PK_Constraint):
                self.assertEqual(constr.get_pk(), "self", "Should be self")
                count += 1
            if(type(constr) == arm_constraints.Pathfd_Constraint):
                self.assertEqual(constr.get_target(), "self", "Should be self")
                self.assertEqual(constr.get_attributes()[0], "supplier", "Should be supplier")
                self.assertEqual(constr.get_attributes()[1], "part", "Should be part")
                count += 1
            if(type(constr) == arm_constraints.FK_Constraint):
                if(constr.get_name() == "supplier"):
                    self.assertEqual(constr.get_fk(), "supplier", "Should be supplier")
                    self.assertEqual(constr.get_references(), "Supplier", "Should be Supplier")
                    count += 1
                if(constr.get_name() == "part"):
                    self.assertEqual(constr.get_fk(), "part", "Should be part")
                    self.assertEqual(constr.get_references(), "Part", "Should be Part")
                    count += 1
            if(type(constr) == arm_constraints.Disjointness_Constraint):
                self.assertEqual(constr.get_disjoint_with()[0], "Supplier", "Should be Supplier")
                self.assertEqual(constr.get_disjoint_with()[1], "Part", "Should be Part")
                count += 1
        self.assertEqual(count, 5, "Should be 5") #check that all of the above constraints were stored in the entity


if __name__ == '__main__':
    unittest2.main()
