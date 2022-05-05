from random import sample
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def sample_user(email='test@mail.com', password='testpass'):
    """ example user """
    return get_user_model().objects.create_user(email, password)

class ModelTest(TestCase):
    
    def test_create_user_with_email_successfull(self):
        """ Try creating new user with an email correctly """
        email = 'test@mail.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email = email,
            password = password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """ Test if the email of a new user is normalized """
        email = 'test@MAIl.com'
        user = get_user_model().objects.create_user(
            email,
            'testpass123'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Test if the new user have an invalid email """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpass123')

    def test_create_new_superuser(self):
        """ Test the new super user """

        email = 'test@mail.com'
        password = 'testpass123'
        user = get_user_model().objects.create_superuser(
            email = email,
            password = password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Try chain representation of the tag's text"""
        tag=models.Tag.objects.create(
            user=sample_user(),
            name='Meat'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredients_str(self):
        ingredient = models.Ingredients.objects.create(
            user = sample_user(),
            name='Banana'
        )

        self.assertEqual(str(ingredient), ingredient.name)