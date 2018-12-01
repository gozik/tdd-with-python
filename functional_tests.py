from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    '''New visitor test'''
    def setUp(self):
        '''Making setup'''
        self.browser = webdriver.Firefox()

    def tearDown(self):
        '''Shutting down'''
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        '''test: it is possible to create a list and work with it later'''
        #Greg is aware about cool to-do list on internet. He decides to check its home page.
        self.browser.get('http://localhost:8000')

        #He sees title and header sing about to-do lists
        self.assertIn('To-Do', self.browser.title)

        self.fail('End of test')
        #He is invited to create a list item


        #He types 'Make a call with mother' as first to-do item


        #Text field still asks to make another item
        #He enters 'Say granny I love her'


        #Page reloads and now it displays both items


        #Greg wonders if site remembers his list. He sees that site generates unique URL for him.
        #There is some text with explanation.


        #He visits this URL - his list is still there.



        #Greg is happy, he goes to bed.

if __name__ == '__main__':
    unittest.main(warnings='ignore')
