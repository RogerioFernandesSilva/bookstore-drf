from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Category, Order, Product


class OrderViewSetTest(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Ficção", description="")
        self.product = Product.objects.create(
            name="Duna",
            description="Ficção científica",
            price="59.90",
            stock=5,
            category=self.category,
        )
        self.order = Order.objects.create(
            product=self.product,
            customer_name="Maria Silva",
            quantity=2,
        )
        self.list_url = reverse("order-list")

    def detail_url(self, pk):
        return reverse("order-detail", args=[pk])

    def test_list_returns_all_orders(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_returns_nested_product(self):
        response = self.client.get(self.detail_url(self.order.id))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["product"]["id"], self.product.id)
        self.assertEqual(
            response.data["product"]["category"]["id"], self.category.id
        )

    def test_create_order(self):
        data = {
            "customer_name": "João Souza",
            "quantity": 1,
            "product_id": self.product.id,
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(response.data["status"], Order.Status.PENDING)

    def test_create_order_with_quantity_greater_than_stock_fails(self):
        data = {
            "customer_name": "João Souza",
            "quantity": 999,
            "product_id": self.product.id,
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("quantity", response.data)
        self.assertEqual(Order.objects.count(), 1)

    def test_create_order_ignores_status_sent_by_client(self):
        data = {
            "customer_name": "João Souza",
            "quantity": 1,
            "product_id": self.product.id,
            "status": Order.Status.SHIPPED,
        }

        response = self.client.post(self.list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], Order.Status.PENDING)

    def test_update_order_customer_name(self):
        data = {
            "customer_name": "Maria Souza",
            "quantity": 2,
            "product_id": self.product.id,
        }

        response = self.client.put(self.detail_url(self.order.id), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.customer_name, "Maria Souza")

    def test_partial_update_order_quantity(self):
        response = self.client.patch(self.detail_url(self.order.id), {"quantity": 1})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.quantity, 1)

    def test_delete_order(self):
        response = self.client.delete(self.detail_url(self.order.id))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)