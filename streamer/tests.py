from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Focus, Links, KeyWords
from home.models import Profile
from django.contrib.auth.models import User
# Create your tests here:

#helper functions

#TODO: tests for upload view

def insert_focus(topic, user):
    #inserts a new focus to the test database
    foc = Focus(focus=topic)
    foc.save()
    user.profile.focus.add(foc)

def insert_url(topic, url, user):
    foc = Focus(focus=topic)
    foc.save()
    user.profile.focus.add(foc)
    foc = user.profile.focus.get(focus=topic)
    url = Links(links=url)
    url.save()
    foc.links.add(url)

def insert_note(topic, note, user):
    foc = Focus(focus=topic)
    foc.save()
    user.profile.focus.add(foc)
    foc = user.profile.focus.get(focus=topic)
    note = KeyWords(keywords=note)
    note.save()
    foc.keywords.add(note)

def make_user(username, password):
    user = User.objects.create_user(username=username, password=password)
    p = Profile(user=user)
    p.save()
    return user

class UserPageViewTests(TestCase):

    def test_home_view_with_no_focuses(self):
        '''
        if there are no focuses in the database an appropriate message
        should be displayed
        '''
        user = make_user('username', 'password')
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('streamer:user_page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add a focus to begin researching')

    def test_home_view_with_multiple_focuses(self):
        '''
        Only the users unique focuses should be displayed
        '''
        Amy = make_user('Amy', 'Amy')
        Bob = make_user('Bob', 'Bob')
        for rand_words in range(100):
            word = str(rand_words)
            insert_focus(word, Amy)
        for rand_words in range(200, 301):
            word = str(rand_words)
            insert_focus(word, Bob)
            #bobs focuses should not be on Amy's page
        self.client.login(username='Amy', password='Amy')
        response = self.client.get(reverse('streamer:user_page'))
        self.assertEqual(response.status_code, 200)
        for rand_words in range(100):
            word = str(rand_words)
            self.assertContains(response, word)
        for rand_words in range(200, 301):
            word = str(rand_words)
            assert word not in response

    def test_user_can_add_focuses(self):
        '''
        when a user adds a focus it should be displayed
        '''
        user = make_user('username', 'password')
        self.client.login(username='username', password='password')
        response = self.client.post(reverse('streamer:user_page'),{'focus':'test_focus'})
        self.assertContains(response, 'test_focus')

    def test_user_can_delete_focuses(self):
        '''
        A post request sent to the server labelled delete_focus should delete the
        corresponding focus
        '''
        user = make_user('username', 'password')
        focus = 'some focus'
        insert_focus(focus, user)
        self.client.login(username='username', password='password')
        response = self.client.post(reverse('streamer:user_page'), {'focus':'test_focus', 'delete_focus':focus})
        focus = [str(focus) for focus in response.context['focus_list']]
        assert focus not in focus


class FocusPageViewTests(TestCase):
    def test_focus_correct(self):
        '''
        upon loading should display correct focus
        '''
        user = make_user('username', 'password')
        insert_focus('Monty Python', user)
        self.client.login(username='username', password='password')
        response = self.client.post(reverse('streamer:focus_page'),{'focus_query':'Monty Python'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Monty Python')

    def test_focus_page_lets_user_add_keywords(self):
        '''
        when a post request is sent to the server named note it should be added
        to a list on the page
        '''
        user = make_user('username', 'password')
        insert_focus('Monty Python 1', user)
        self.client.login(username='username', password='password')
        response = self.client.post(reverse('streamer:focus_page'), {'focus_query':'Monty Python 1','note':'test_notes'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_notes')

    def test_focus_page_lets_user_add_urls(self):
        '''
        when a post request named link is sent to the server the user should be
        see it dislpayed on the page
        '''
        user = make_user('username', 'password')
        insert_focus('Monty Python 3', user)
        self.client.login(username='username', password='password')
        response = self.client.post(reverse('streamer:focus_page'), {'focus_query':'Monty Python 3','link':'test_links'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test_links')

    def test_focus_page_returns_a_summary_upon_landing(self):
        '''
        The summary context should not be none.
        '''
        user = make_user('username', 'password')
        focus = 'random focus which wont be in wiki'
        insert_focus(focus, user)
        self.client.login(username='username', password='password')
        response = self.client.post(reverse('streamer:focus_page'), {'focus_query':focus})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['summary'])

    def test_focus_page_returns_a_summary_upon_returning(self):
        '''
        when a user does some action on the page (e.g. reload) a summary should
        still be returned
        '''
        user = make_user('username', 'password')
        focus = 'random focus'
        insert_focus(focus, user)
        session = self.client.session
        session['current_focus'] = focus
        session.save()
        self.client.login(username='username', password='password')
        response = self.client.post(reverse('streamer:focus_page'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['summary'])

    def test_focus_page_allows_user_to_delete_notes(self):
         '''
         When a post request labelled delete_note is sent to server
         it should delete a note from the model
         '''
         session = self.client.session
         focus = 'Monty Python'
         session['current_focus'] = focus
         session.save()
         user = make_user('username', 'password')
         note = 'I should learn more about tests'
         insert_note(focus, note, user)
         self.client.login(username='username', password='password')
         response = self.client.post(reverse('streamer:focus_page'), {'delete-note':note})
         notes = [str(_) for _ in response.context['notes']]
         self.assertEqual(response.status_code, 200)
         assert note not in notes

    def test_focus_page_allows_user_to_delete_urls(self):
        '''
        When a post request labelled delete_l is sent to server
        it should delete a link from the model
        '''
        user = make_user('username', 'password')
        session = self.client.session
        focus = 'Monty Python'
        session['current_focus'] = focus
        session.save()
        url = 'www.test-url.com/Pythonista'
        insert_url(focus, url, user)
        self.client.login(username='username', password='password')
        response = self.client.post(reverse('streamer:focus_page'), {'delete-link':url})
        links = [str(_) for _ in response.context['links']]
        self.assertEqual(response.status_code, 200)
        assert url not in links

    def test_user_can_change_summary(self):
        '''
        user should be able to write their own summary of the
        topic which will replace the default and be stored in db
        '''
        pass
