import unittest
import os
from unittest import mock
import csvreader 

class Test_File_Handler(unittest.TestCase):

    @mock.patch('setupMenu.input', create=True)
    def testdictCreateSimple(self, mocked_input):
        mocked_input.side_effect = ['1','10','0']

    def test_deck(self):                        #This deck tests if the deck gets created correctly (len of the list is printed out to see if there's the correct amount of cards in it)
        deck = Deck()                           #The build method is called in the deck constructor so the deck is built at this point.
        self.assertTrue(len(deck.cards) == 52

if __name__ == '__main__':
    unittest.main()