from django.test import TestCase
from django.contrib.auth import get_user_model

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