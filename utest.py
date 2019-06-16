import unittest
from csvreader import showDB, searchCrime, makeHTML,makeJSON
from unittest import mock
import os


class Test(unittest.TestCase):
         

    # Test if project directory is being created
    def test1_create_project_directory(self):
        directory = 'html/fullhtml.html'
        makeHTML() # testing this method
        is_created = False
        if os.path.exists(directory):
            is_created = True
        self.assertTrue(is_created),


    def test2_create_project_directory(self):
        directory = 'json/fulljson.json'
        makeJSON() # testing this method
        is_created = False
        if os.path.exists(directory):
            is_created = True
        self.assertTrue(is_created)



    


if __name__ == "__main__":
    unittest.main()