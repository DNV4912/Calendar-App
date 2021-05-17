import unittest
import sys

sys.path.insert(1, '../')
import fetching_holidays as fh


class TestHoliday(unittest.TestCase):
    def test_scrapped_table(self): #To test if the scrapped table has values and the right column names
        df = fh.get_table()
        column_names = df.columns
        self.assertIsNot(len(df),0) #checks if the table is populated after parsing
        self.assertEqual(list(column_names),['Date','Day','Holiday','States','id']) #checks if it has thSe required column names

    def test_db_table(self):# To test if the table stored in the DB has values and the right column names
        df = fh.select_table()
        column_names = df.columns
        self.assertIsNot(len(df),0) #checks if the table is populated after being pulled from the db
        self.assertEqual(list(column_names),['Date','Day','Holiday','State','ID']) #checks if it has the required column names


if __name__ =="__main__":
    unittest.main()