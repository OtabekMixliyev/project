from django.test import TestCase
from django.urls import reverse

from books.models import Book
from user.models import CustomUser


class BooksTestCase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:list"))

        self.assertContains(response, "No books found.")

    def test_books_list(self):
        book1 = Book.objects.create(title="Book1", description="Description1", isbn="123121")
        book2 = Book.objects.create(title="Book2", description="Description2", isbn="111111")
        book3 = Book.objects.create(title="Book3", description="Description3", isbn="333333")

        response = self.client.get(reverse("books:list"))

        for book in [book1, book2]:
            self.assertContains(response, book.title)

        response = self.client.get(reverse("books:list") + "?page=2")
        self.assertContains(response, book3)

    def test_detail_page(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123121")

        response = self.client.get(reverse("books:detail", kwargs={"id": book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

    def test_search_books(self):
        book1 = Book.objects.create(title="Sport", description="Description1", isbn="123121")
        book2 = Book.objects.create(title="Guide", description="Description2", isbn="111111")
        book3 = Book.objects.create(title="Shoe Dog", description="Description3", isbn="333333")

        response = self.client.get(reverse("books:list") + "?q=Sport")
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=Guide")
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)

        response = self.client.get(reverse("books:list") + "?q=Shoe Dog")
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)


class BookReviewTestCase(TestCase):
    def test_add_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123121")
        user = CustomUser.objects.create(
            username="otabek",
            first_name="Otabek",
            last_name="Mixliyev",
            email="mixliyevotabek73@gmail.com"
        )
        user.set_password("somepass")
        user.save()

        self.client.login(username="otabek", password="somepass")

        self.client.post(reverse('books:reviews', kwargs={"id": book.id}), data={
            "comment": "vert good book"
        })
        book_reviews = book.bookreview_set.all()

        self.assertEqual(book_reviews.count(), 1)
        self.assertEqual(book_reviews[0].comment, "vert good book")
        self.assertEqual(book_reviews[0].user, user)
