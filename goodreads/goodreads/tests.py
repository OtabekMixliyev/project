from django.test import TestCase
from django.urls import reverse
from books.models import Book, BookReview
from user.models import CustomUser


class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title="Sport", description="Description1", isbn="123121")
        user = CustomUser.objects.create(
            username="otabek",
            first_name="Otabek",
            last_name="Mixliyev",
            email="mixliyevotabek73@gmail.com"
        )
        user.set_password("somepass")
        user.save()
        review1 = BookReview.objects.create(book=book, user=user, comment="Very good book")
        review2 = BookReview.objects.create(book=book, user=user, comment="Useful book")
        review3 = BookReview.objects.create(book=book, user=user, comment="Nice book")

        response = self.client.get(reverse("home_page") + "?page_size=2")

        #self.assertContains(response, review3.comment)
        #self.assertContains(response, review2.comment)
        #self.assertContains(response, review1.comment)
