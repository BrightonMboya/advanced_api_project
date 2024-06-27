# api/test_views.py

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Book, Author

class BookAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.author = Author.objects.create(name='Author1')
        self.book = Book.objects.create(title='Book1', publication_year=2020, author=self.author)
        self.client.login(username='testuser', password='testpassword')

    def test_create_book(self):
        url = reverse('book-list')
        data = {'title': 'New Book', 'publication_year': 2021, 'author': self.author.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(id=response.data['id']).title, 'New Book')

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book1')

    def test_retrieve_book(self):
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Book1')

    def test_update_book(self):
        url = reverse('book-detail', args=[self.book.id])
        data = {'title': 'Updated Book', 'publication_year': 2021, 'author': self.author.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')

    def test_delete_book(self):
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    # def test_search_books(self):
    #     url = reverse('book-list')
    #     response = self.client.get(url, {'search': 'Author1'}, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.data[0]['title'], 'Book1')

    def test_filter_books(self):
        url = reverse('book-list')
        response = self.client.get(url, {'author': self.author.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book1')

    def test_order_books(self):
        url = reverse('book-list')
        response = self.client.get(url, {'ordering': 'title'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book1')
