from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Category, Product


class ProductViewSetTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Ficção", description="")
        self.product = Product.objects.create(
            name="Duna",
            description="Ficção científica",
            price="59.90",
            stock=10,
            category=self.category,
        )
        self.list_url = reverse("product-list")

    def detail_url(self, pk):
        return reverse("product-detail", args=[pk])

    def test_list_returns_all_products(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_returns_nested_category(self):
        response = self.client.get(self.detail_url(self.product.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["category"]["id"], self.category.id)
        self.assertEqual(response.data["category"]["name"], "Ficção")

    def test_create_product(self):
        data = {
            "name": "Fundação",
            "description": "Ficção científica",
            "price": "45.00",
            "stock": 5,
            "active": True,
            "category_id": self.category.id,
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(response.data["category"]["id"], self.category.id)

    def test_create_product_without_category_fails(self):
        data = {
            "name": "Fundação",
            "price": "45.00",
            "stock": 5,
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("category_id", response.data)

    def test_create_product_with_price_zero_fails(self):
        data = {
            "name": "Fundação",
            "price": "0.00",
            "stock": 5,
            "category_id": self.category.id,
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", response.data)

    def test_update_product(self):
        new_category = Category.objects.create(name="Técnico", description="")
        data = {
            "name": "Duna (edição especial)",
            "description": "Ficção científica",
            "price": "69.90",
            "stock": 8,
            "active": True,
            "category_id": new_category.id,
        }

        response = self.client.put(self.detail_url(self.product.id), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Duna (edição especial)")
        self.assertEqual(self.product.category, new_category)

    def test_partial_update_product_stock(self):
        response = self.client.patch(self.detail_url(self.product.id), {"stock": 3})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

    def test_delete_product(self):
        response = self.client.delete(self.detail_url(self.product.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)