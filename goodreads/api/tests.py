from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from user.models import CustomUser
from books.models import Book, BookReview


class BookReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="Otabek", first_name="Otabek")
        self.user.set_password("somepass")
        self.user.save()
        self.client.login(username="Otabek", password="somepass")

    def test_book_review_detail(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123121")
        br = BookReview.objects.create(book=book, user=self.user, comment="Very good book")

        response = self.client.get(reverse('api:review-detail', kwargs={'id': br.id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], br.id)
        self.assertEqual(response.data['comment'], "Very good book")
        self.assertEqual(response.data['book']['id'], br.book.id)
        self.assertEqual(response.data['book']['title'], 'Book1')
        self.assertEqual(response.data['book']['description'], 'Description1')
        self.assertEqual(response.data['book']['isbn'], "123121")
        self.assertEqual(response.data['user']['first_name'], "Otabek")
        self.assertEqual(response.data['user']['username'], "Otabek")

    def test_delete_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123121")
        br = BookReview.objects.create(book=book, user=self.user, comment="Very good book")

        response = self.client.delete(reverse('api:review-detail', kwargs={'id': br.id}))

        self.assertEqual(response.status_code, 204)
        self.assertFalse(BookReview.objects.filter(id=br.id).exists())

    def test_patch_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123121")
        br = BookReview.objects.create(book=book, user=self.user, comment="Very good book")

        response = self.client.patch(reverse('api:review-detail', kwargs={'id': br.id}),
                                     data={'comment': "Very good book"})
        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.comment, "Very good book")

    def test_put_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123121")
        br = BookReview.objects.create(book=book, user=self.user, comment="Very good book")

        response = self.client.patch(
            reverse('api:review-detail', kwargs={'id': br.id}),
            data={'comment': "Very good book", 'user_id': self.user.id, 'book_id': book.id}
        )

        br.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(br.comment, "Very good book")

    def test_create_review(self):
        book = Book.objects.create(title="Book1", description="Description1", isbn="123121")

        data = {
            'comment': 'bad book',
            'user_id': self.user.id,
            'book_id': book.id
        }

        response = self.client.post(reverse('api:review-list'), data=data)
        br = BookReview.objects.get(book=book)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(br.comment, 'bad book')

#    def test_book_review_list(self):
#        user_two = CustomUser.objects.create(username="Ibrohim", first_name="Ibrohim")
#        book = Book.objects.create(title="Book1", description="Description1", isbn="123121")
#        br = BookReview.objects.create(book=book, user=self.user, comment="Very good book")
#        br_two = BookReview.objects.create(book=book, user=user_two, comment="Not good")

#        response = self.client.get(reverse('api:review-list'))

#        self.assertEqual(response.status_code, 200)
#        self.assertEqual(len(response.data['results']), 1)

#        self.assertEqual(response.data['count'], 1)
#        self.assertIn('next', response.data)
#        self.assertIn('previous', response.data)
#        self.assertEqual(response.data['results'][0]['id'], br_two.id)
#        self.assertEqual(response.data['results'][0]['comment'], br_two.comment)
#        self.assertEqual(response.data['results'][1]['id'], br.id)
#        self.assertEqual(response.data['results'][1]['comment'], br.comment)
