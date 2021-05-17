import unittest
import sys

sys.path.insert(1, '../')
import generate_ics as gi


class TestICS(unittest.TestCase):
    def test_validate_master_id(self): #To test if the master ID validatation function
        self.assertFalse(gi.validate_master_id('12345')) #checks if a valid id is entered
        self.assertTrue(gi.validate_master_id('NLzPiS6HZ4wxckeivqLBVA')) 
        
    

if __name__ =="__main__":
    unittest.main()