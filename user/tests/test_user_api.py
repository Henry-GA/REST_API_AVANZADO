from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """ Test the API for Public User"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """ Try to create a User with a successful payload"""
        payload = {
            'email': 'test@mail.com',
            'password': 'pass123',
            'name': 'Test Name',
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        """ Try creating a user that already exist"""
        payload={
            'email': 'test@mail.com',
            'password': 'pass123',
            'name': 'Test Name',
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_password_too_short(self):
        """ Try a user with a password shorter than 5 characters """
        payload={
            'email':'test@mail.com',
            'password': 'pw',
            'name': 'Test Name',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        """ Test that the token had been created for the user """
        payload={
            'email':'test@mail.com',
            'password':'pass123',
            'name': 'Test Name'
        }
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credential(self):
        """ Test that the token created token is valid """
        create_user(email='test@mail.com', password='pass123')
        payload={'email':'test@mail.com', 'password':'pass321'}
        
        res= self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_token_no_user(self):
        """ Test that the token is not created without a valid user """
        payload={
            'email': 'test@mail.com',
            'password': 'pass123',
            'name': 'Test Name'
        }
        
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ Try to post without user or password """
        res = self.client.post(TOKEN_URL, {'email':'one', 'password':''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

