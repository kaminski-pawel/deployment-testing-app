from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

User = get_user_model()


class PublicUserApiTests(TestCase):
    def test_for_error_if_no_email_nor_password(self):
        with self.assertRaises(TypeError):
            User.objects.create_user()

    def test_for_error_if_no_password(self):
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")

    def test_for_error_if_empy_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_for_error_if_user_exists(self):
        User.objects.create_user(email="test@example.com", password="foo")
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email="test@example.com", password="bar")

    def test_if_password_is_correct(self):
        email = "test@example.com"
        password = "zaq12wsx"
        user = User.objects.create_user(email=email, password=password)
        self.assertTrue(user.check_password(password))

    def test_default_values(self):
        email = "test@example.com"
        password = "zaq12wsx"
        user = User.objects.create_user(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertTrue(user.date_joined)

    def test_email_normalization(self):
        user = User.objects.create_user(email="test@EXamplE.com", password="bar")
        self.assertEqual(user.email, "test@example.com")
