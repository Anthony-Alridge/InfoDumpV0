from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Focus, Links, KeyWords
# Create your tests here:

#helper functions


def insert_focus(topic):
    #inserts a new focus to the test database
    foc = Focus(focus=topic)
    foc.save()

def insert_url(topic, url):
    foc = Focus(focus=topic)
    foc.save()
    url = Links(links=url)
    url.save()
    foc.links.add(url)

def insert_note(topic, note):
    foc = Focus(focus=topic)
    foc.save()
    note = KeyWords(keywords=note)
    note.save()
    foc.keywords.add(note)

class UserPageViewTests(TestCase):
    def test_home_view_with_no_focuses(self):
        '''
        if there are no focuses in the database an appropriate message
        should be displayed
        '''
        response = self.client.get(reverse('streamer:user_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add a focus to begin researching')

    def test_home_view_with_multiple_focuses(self):
        for rand_words in range(100):
            word = str(rand_words)
            insert_focus(word)
        response = self.client.get(reverse('streamer:user_page'))
        self.assertEqual(response.status_code, 200)
        for rand_words in range(100):
            word = str(rand_words)
            self.assertContains(response, word)

    def test_user_can_add_views(self):
        response = self.client.post(reverse('streamer:user_page'),{'query':'test_focus'})
        self.assertContains(response, 'test_focus')


class FocusPageViewTests(TestCase):
    def test_focus_correct(self):
        '''
        upon loading should display correct focus
        '''
        insert_focus('Monty Python')
        response = self.client.post(reverse('streamer:focus_page'),{'focus_query':'Monty Python'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Monty Python')

    def test_focus_page_lets_user_add_keywords(self):
        '''
        when a post request is sent to the server named keyword it should be added
        to a list on the page
        '''
        insert_focus('Monty Python 1')
        response = self.client.post(reverse('streamer:focus_page'), {'focus_query':'Monty Python 1','keyword':'test_notes'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_notes')

    def test_focus_page_lets_user_add_urls(self):
        '''
        when a post request named link is sent to the server the user should be
        see it dislpayed on the page
        '''
        insert_focus('Monty Python 3')
        response = self.client.post(reverse('streamer:focus_page'), {'focus_query':'Monty Python 3','link':'test_links'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_links')

    def test_focus_page_returns_a_summary(self):
        '''
        The summary context should not be none.
        '''
        insert_focus('Monty Python 4')
        response = self.client.post(reverse('streamer:focus_page'), {'focus_query':'Monty Python 4'})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['summary'])

    def test_focus_page_allows_user_to_delete_notes(self):
         '''
         When a post request labelled delete_note is sent to server
         it should delete a keyword from the model
         '''
         topic = 'Monty Python'
         note = 'I should learn more about tests'
         insert_note(topic, note)
         response = self.client.post(reverse('streamer:focus_page'), {'focus_query':'Monty Python', 'delete-note':note})
         notes = [str(_) for _ in response.context['keywords']]
         self.assertEqual(response.status_code, 200)
         assert note not in notes

    def test_focus_page_allows_user_to_delete_urls(self):
        '''
        When a post request labelled delete_l is sent to server
        it should delete a link from the model
        '''
        topic = 'Monty Python'
        url = 'www.test-url.com/Pythonista'
        insert_url(topic, url)
        response = self.client.post(reverse('streamer:focus_page'), {'focus_query':'Monty Python', 'delete-link':url})
        links = [str(_) for _ in response.context['links']]
        self.assertEqual(response.status_code, 200)
        assert url not in links

    def test_user_can_change_summary(self):
        '''
        user should be able to write their own summary of the
        topic which will replace the default and be stored in db
        '''
        pass
