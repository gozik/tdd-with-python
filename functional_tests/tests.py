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

    def test_can_start_a_list_for_one_user(self):
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



    def test_multiple_users_can_start_lists_at_different_urls(self):
        """ test: multiple users can start lists at different urls """
        # Greg starts new list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Call mother')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Call mother')

        # He notices, that his list has unique url.
        greg_list_url = self.browser.current_url
        self.assertRegex(greg_list_url, '/lists/.+')

        # New user, Sue appears on site.
        
        ## Using new browser instance to hide any Greg session information from Sue.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Sue visits home page. There is no track of Greg's activity
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Call mother', page_text)
        self.assertNotIn('Say granny I love her')

        # Sue starts new list. She gonna to grossery.
        inputbox = self.browser.find_elment_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Sue gets unique url.
        sue_list_url = self.browser.current_url
        self.assertRegex(sue_list_url, '/lists/.+')
        self.assertNotEqual(greg_list_url, sue_list_url)

        # Still there is no track of Greg's list on page.
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('1: Call mother', page_text)
        self.assertIn('1: Buy milk', page_text)

        # Sue and Greg go sleep.
