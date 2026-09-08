from django.test import TestCase

from api.models import Category, Order, Product
from api.serializers import OrderSerializer


class OrderSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Ficção", description="")
        self.product = Product.objects.create(
            name="Duna",
            description="Ficção científica",
            price="59.90",
            stock=5,
            category=self.category,
        )

    def test_accepts_valid_data(self):
        data = {
            "customer_name": "Maria Silva",
            "quantity": 2,
            "product_id": self.product.id,
        }

        serializer = OrderSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_requires_customer_name(self):
        data = {"quantity": 1, "product_id": self.product.id}

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("customer_name", serializer.errors)

    def test_requires_product(self):
        data = {"customer_name": "Maria Silva", "quantity": 1}

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("product_id", serializer.errors)

    def test_rejects_zero_quantity(self):
        data = {
            "customer_name": "Maria Silva",
            "quantity": 0,
            "product_id": self.product.id,
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("quantity", serializer.errors)

    def test_rejects_quantity_greater_than_stock(self):
        data = {
            "customer_name": "Maria Silva",
            "quantity": 999,
            "product_id": self.product.id,
        }

        serializer = OrderSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("quantity", serializer.errors)

    def test_creates_order_linked_to_product(self):
        data = {
            "customer_name": "Maria Silva",
            "quantity": 2,
            "product_id": self.product.id,
        }

        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()

        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.status, Order.Status.PENDING)

    def test_returns_nested_product_representation(self):
        order = Order.objects.create(
            product=self.product,
            customer_name="Maria Silva",
            quantity=1,
        )

        serializer = OrderSerializer(order)

        self.assertEqual(serializer.data["product"]["id"], self.product.id)
        self.assertEqual(
            serializer.data["product"]["category"]["id"], self.category.id
        )

    def test_status_is_read_only(self):
        data = {
            "customer_name": "Maria Silva",
            "quantity": 1,
            "product_id": self.product.id,
            "status": Order.Status.SHIPPED,
        }

        serializer = OrderSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()

        # mesmo enviando "shipped", o valor padrão deve prevalecer
        self.assertEqual(order.status, Order.Status.PENDING)

    def test_returns_expected_fields(self):
        order = Order.objects.create(
            product=self.product,
            customer_name="Maria Silva",
            quantity=1,
        )

        serializer = OrderSerializer(order)

        expected_fields = {
            "id",
            "product",
            "customer_name",
            "quantity",
            "status",
            "created_at",
        }
        self.assertEqual(set(serializer.data.keys()), expected_fields)
