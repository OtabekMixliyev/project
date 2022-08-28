from django.urls import reverse
from user.models import CustomUser
from django.test import TestCase
from django.contrib.auth import get_user


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("user:register"),
            data={
                "username": "Otabek",
                "first_name": "Otabek",
                "last_name": "Mixliyev",
                "email": "mixliyevotabek73@gmail.com",
                "password": "somepassword"
            }
        )

        user = CustomUser.objects.get(username="Otabek")

        self.assertEqual(user.first_name, "Otabek")
        self.assertEqual(user.last_name, "Mixliyev")
        self.assertEqual(user.email, "mixliyevotabek73@gmail.com")
        self.assertNotEqual(user.password, 'somepassword')
        self.assertTrue(user.check_password("somepassword"))

    def test_required_fields(self):
        response = self.client.post(
            reverse("user:register"),
            data={
                "first_name": "Otabek",
                "email": "mixliyevotabek73@gmail.com"
            }
        )

        user_count = CustomUser.objects.count()

        # self.assertEqual(user_count, 0)
        # self.assertFormError(response, "form", "username", "This field is required.")
        # self.assertFormError(response, "form", "password", "This field is required.")

    def test_invalid_email(self):
        response = self.client.post(
            reverse("user:register"),
            data={
                "username": "Otabek",
                "first_name": "Otabek",
                "last_name": "Mixliyev",
                "email": "invalid-email",
                "password": "somepassword"
            }
        )
        user_count = CustomUser.objects.count()

        # self.assertEqual(user_count, 0)
        # self.assertFormError(response, "form", "email", "Enter a valid email address.")

    def test_unique_username(self):
        user = CustomUser.objects.create(username="otabek", first_name="Otabek")
        user.set_password("somepass")
        user.save()

        self.client.post(
            reverse("user:register"),
            data={
                "username": "otabek",
                "first_name": "Otabek",
                "last_name": "Mixliyev",
                "email": "maixliyevotabek73@gmail.com",
                "password": "somepassword"
            }
        )

        user_count = CustomUser.objects.count()
        self.assertEqual(user_count, 1)

        # self.assertFormError(response, "form", "username", "A user with that username already exists." )


class LoginTestCase(TestCase):
    def setUp(self):
        self.db_user = CustomUser.objects.create(username="Otabek", first_name="Otabek")
        self.db_user.set_password("somepass")
        self.db_user.save()

    def test_successful_login(self):
        self.client.post(
            reverse("user:login"),
            data={
                "username": "Otabek",
                "password": "somepass"
            }
        )
        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)

    def test_wrong_credential(self):
        self.client.post(
            reverse("user:login"),
            data={
                "username": "wrong-username",
                "password": "somepass"
            }
        )
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse("user:login"),
            data={
                "username": "Otabek",
                "password": "wrong-password"
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

    def test_logout(self):
        self.client.login(username="Otabek", password="somepass")

        self.client.get(reverse("user:logout"))

        user = get_user(self.client)
        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("user:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("user:login") + "?next=/user/profile/")

    def test_profile_detail(self):
        user = CustomUser.objects.create(
            username="otabek",
            first_name="Otabek",
            last_name="Mixliyev",
            email="mixliyevotabek73@gmail.com"
        )
        user.set_password("somepass")
        user.save()

        self.client.login(username="otabek", password="somepass")

        response = self.client.get(reverse("user:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

    def test_update_profile(self):
        user = CustomUser.objects.create(
            username="otabek",
            first_name="Otabek",
            last_name="Mixliyev",
            email="mixliyevotabek73@gmail.com"
        )
        user.set_password("somepass")
        user.save()

        self.client.login(username="otabek", password="somepass")

        response = self.client.post(
            reverse("user:profile_edit"),
            data={
                "username": "otabek",
                "first_name": "Otabek",
                "last_name": "Doe",
                "email": "mixliyevotabek7@gmail.com"
            }
        )

        user.refresh_from_db()

        self.assertEqual(user.last_name, "Doe"),
        self.assertEqual(user.email, "mixliyevotabek7@gmail.com"),
        self.assertEqual(response.url, reverse("user:profile"))


