from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(LiveServerTestCase):
    '''New visitor test'''
    def wait_for_row_in_list_table(self, row_text):
        """wait for row in table"""
        start_time = time.time()
        while True:
            try:
                self.check_for_row_in_list_table(row_text)
                return
            except(AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
 
    def setUp(self):
        '''Making setup'''
        self.browser = webdriver.Firefox()

    def tearDown(self):
        '''Shutting down'''
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        '''test: it is possible to create a list and work with it later'''
        #Greg is aware about cool to-do list on internet. He decides to check its home page.
        self.browser.get(self.live_server_url)

        #He sees title and header sing about to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        #He is invited to create a list item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )



        #He types 'call mother' as first to-do item
        inputbox.send_keys('Call mother')

        #When he presses enter page refreshes, now page contains "1. Call mother" as list item.
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Call mother')

        #Text field still asks to make another item
        #He enters 'Say granny I love her'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Say granny I love her')
        inputbox.send_keys(Keys.ENTER)


        #Page reloads and now it displays both items
        self.wait_for_row_in_list_table('1: Call mother')
        self.wait_for_row_in_list_table('2: Say granny I love her')

        #Greg wonders if site remembers his list. He sees that site generates unique URL for him.
        #There is some text with explanation.

        self.fail('To finish test')

        #He visits this URL - his list is still there.



        #Greg is happy, he goes to bed.
