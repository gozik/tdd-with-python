from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string

from lists.views import home_page
from lists.models import Item

class HomePageTest(TestCase):
    '''test of home page'''
    def test_uses_home_template(self):
        '''test: home template is used'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        '''test: saves post request'''
        response = self.client.post('/', data={'item_text': 'A new list item'})
        
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

        
    def test_redirects_after_POST(self):
        """test: redirects after POST"""
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/unique_list_in_the_world/')


    def test_home_page_does_not_create_an_item(self):
        """test: home page without item data does not create an empty item"""
        response = self.client.get('/')
        self.assertEqual(Item.objects.count(), 0)
        


class ItemModelTest(TestCase):
    '''test model of list Item'''

    def test_saving_and_retrieving_items(self):
        '''test: save and retrieve list item'''
        first_item = Item()
        first_item.text = 'The first item'
        first_item.save()

        second_item = Item()
        second_item.text = 'The second item'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]

        self.assertEqual(first_saved_item.text, 'The first item')
        self.assertEqual(second_saved_item.text, 'The second item')


class ListViewTest(TestCase):
    """ test list view"""

    def test_displays_all_items(self):
        """ test: all list items are displayed """
        Item.objects.create(text = 'itemey 1')
        Item.objects.create(text = 'itemey 2')

        response = self.client.get('/lists/unique_list_in_the_world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')
