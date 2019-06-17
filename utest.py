import unittest
from csvreader import showDB, searchCrime, makeHTML,makeJSON, searchCrimeRadius, writeToCSV
from unittest import mock
import os


class Test(unittest.TestCase):
         

    # Test if project directory is being created
    def test_create_html_doc(self):
        filePath = 'html/fullhtml.html'
        makeHTML() # testing this method
        is_created = False
        if os.path.exists(filePath):
            is_created = True
        self.assertTrue(is_created, "sucsessful, since file is created"),

    def test_create_html_doc_fail(self):
        filePath = 'html/fullhtmlFail.html'
        makeHTML() # testing this method
        is_created = False
        if os.path.exists(filePath):
            is_created = True
        self.assertTrue(is_created, "Fails since filename is wrong"),


    def test_create_json_doc(self):
        filePath = 'json/fulljson.json'
        makeJSON() # testing this method
        is_created = False
        if os.path.exists(filePath):
            is_created = True
        self.assertTrue(is_created, "sucsessful, since file is created")
    
    
    def test_create_json_doc_fail(self):
        filePath = 'json/fulljsonFail.json'
        makeJSON() # testing this method
        is_created = False
        if os.path.exists(filePath):
            is_created = True
        self.assertTrue(is_created,"Fails, since filename is wrong"),
    
    def test_showdb(self):
        sb = showDB()# testing this method
        self.assertGreater(sb,2, msg="did good"),
    
    def test_showdb_fail(self):
        sb = showDB()# testing this method
        self.assertLess(sb,2,msg="did bad")
    
    def test_search_crime(self):
        sc = searchCrime()
        self.assertGreater(sc,1,msg="did good search")

    def test_search_crime_fail(self):
        sc = searchCrime()
        self.assertLess(sc,2,msg="did bad search")   

    def test_search_crime_radius(self):
        sc = searchCrimeRadius()
        self.assertGreater(sc,1,msg="did good search")

    def test_search_crime_radius_fail(self):
        sc = searchCrimeRadius()
        self.assertLess(sc,2,msg="did bad search")
    
    def test_write_to_csv(self):
        wrc = writeToCSV()
        blob = {'cdatetime':'01/02/2000 14:00','address':'1234 TEST STREET','district':'88','beat':'88A','grid':'888','crimedescr':'888 BLOBBY', 'ucr_ncic_code':'8899','latitude':'123','longitude':'456' }
        self.assertDictEqual(wrc,blob,msg='did not match')
        
        
    


        

    

    




    



    


if __name__ == "__main__":
    unittest.main()