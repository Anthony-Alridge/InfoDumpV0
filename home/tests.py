from django.test import TestCase
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import Profile
# Create your tests here.
def make_user(username, password):
    user = User.objects.create_user(username=username, password=password)
    p1 = Profile(user=user)
    p1.save()
    return user
class HomePage(TestCase):
    '''
    home page will handle authentication and
    redirect either to streamer app or registration
    (sign_up_page) view
    '''
    def test_home_page(self):
        '''
        simple test to ensure users are
        directed to the home view when visiting root path
        '''
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_authenticated_users_are_redirected(self):
        '''
        if a user is corrected authenticated they should be
        redirected to the userPage(in streamer app)
        '''
        username = 'test'
        password = 'test'
        make_user(username, password)
        response = self.client.post('', {'username': username, 'password': password})
        self.assertRedirects(response, reverse('streamer:user_page'), status_code=302, target_status_code=200)

    def test_user_not_redirected_if_authentication_fails(self):
        username = 'not_auth'
        password = 'not_auth'
        response = self.client.post('', {'username': username, 'password': password})
        self.assertContains(response, 'There was a problem with your login details.')

    def test_login_form_works(self):
        '''
        Test that the login form works. Useful for ensuring changes on the
        front end doesnt break the backend
        '''
        form = LoginForm({'username':'test', 'password':'test'})
        self.assertTrue(form.is_valid())

class SignUpPage(TestCase):
    '''
    Testing the registration mechanisms, which utilise django forms
    and views.
    '''
    def test_registration_form_works(self):
        '''
        test that the registration form is valid when the correct details are
        submitted
        '''
        form = RegistrationForm({'username':'test_username','email':'test_email@example.com', 'password':'test_password'})
        self.assertTrue(form.is_valid())
    def test_page_with_form_rendered_if_get_request(self):
        '''
        if a GET request is sent to the server than the user has been redirected to the sign up page via a link
        and the html form should be displayed
        '''
        response = self.client.get(reverse('home:sign_up'))
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        assert form #make sure a form is rendered
    def test_sign_up_page_redirects_to_self_if_unsuccessful(self):
        '''
        if some information is invalid the user should be redirected to back to sign up page
        with the original form.
        '''
        response = self.client.post(reverse('home:sign_up'), {'username':'','email':'test@example.com', 'password':'password'})
        self.assertEqual(response.status_code, 200)


    def test_sign_up_page_redirects_to_streamer_if_successful(self):
        '''
        if login is successful it should redirect to a login successful page
        which will display some instructions and a redirect to the focuses
        '''
        response = self.client.post(reverse('home:sign_up'), {'username':'username', 'email':'test@example.com', 'password':'password'})
        self.assertRedirects(response, reverse('streamer:user_page'), status_code=302, target_status_code=200)
