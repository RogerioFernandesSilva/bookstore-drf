from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Category


class CategoryViewSetTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Ficção", description="Livros de ficção"
        )
        self.list_url = reverse("category-list")

    def detail_url(self, pk):
        return reverse("category-detail", args=[pk])

    def test_list_returns_all_categories(self):
        Category.objects.create(name="Técnico", description="Livros técnicos")

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_returns_category_data(self):
        response = self.client.get(self.detail_url(self.category.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Ficção")

    def test_retrieve_unknown_category_returns_404(self):
        response = self.client.get(self.detail_url(9999))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_category(self):
        data = {"name": "Infantil", "description": "Para crianças"}

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(response.data["name"], "Infantil")

    def test_create_category_with_blank_name_fails(self):
        data = {"name": "   ", "description": "Nome inválido"}

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertEqual(Category.objects.count(), 1)

    def test_update_category(self):
        data = {"name": "Ficção Científica", "description": "Atualizada"}

        response = self.client.put(self.detail_url(self.category.id), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Ficção Científica")

    def test_partial_update_category(self):
        response = self.client.patch(
            self.detail_url(self.category.id), {"description": "Nova descrição"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.description, "Nova descrição")
        # o nome não deve ter sido alterado em um PATCH parcial
        self.assertEqual(self.category.name, "Ficção")

    def test_delete_category(self):
        response = self.client.delete(self.detail_url(self.category.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)