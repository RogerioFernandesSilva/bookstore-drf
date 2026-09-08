from django.test import TestCase

from api.models import Category, Product
from api.serializers import ProductSerializer


class ProductSerializerTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Ficção", description="")

    def test_accepts_valid_data(self):
        data = {
            "name": "Duna",
            "description": "Ficção científica",
            "price": "59.90",
            "stock": 10,
            "active": True,
            "category_id": self.category.id,
        }

        serializer = ProductSerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_requires_name(self):
        data = {
            "price": "59.90",
            "stock": 10,
            "category_id": self.category.id,
        }

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_requires_category(self):
        data = {
            "name": "Duna",
            "price": "59.90",
            "stock": 10,
        }

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("category_id", serializer.errors)

    def test_rejects_price_less_or_equal_zero(self):
        data = {
            "name": "Duna",
            "price": "0.00",
            "stock": 10,
            "category_id": self.category.id,
        }

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("price", serializer.errors)

    def test_rejects_unknown_category(self):
        data = {
            "name": "Duna",
            "price": "59.90",
            "stock": 10,
            "category_id": 9999,
        }

        serializer = ProductSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("category_id", serializer.errors)

    def test_creates_product_linked_to_category(self):
        data = {
            "name": "Duna",
            "description": "Ficção científica",
            "price": "59.90",
            "stock": 10,
            "active": True,
            "category_id": self.category.id,
        }

        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()

        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(product.category, self.category)

    def test_returns_nested_category_representation(self):
        product = Product.objects.create(
            name="Duna",
            description="Ficção científica",
            price="59.90",
            stock=10,
            category=self.category,
        )

        serializer = ProductSerializer(product)

        self.assertEqual(serializer.data["category"]["id"], self.category.id)
        self.assertEqual(serializer.data["category"]["name"], self.category.name)

    def test_returns_expected_fields(self):
        product = Product.objects.create(
            name="Duna",
            description="Ficção científica",
            price="59.90",
            stock=10,
            category=self.category,
        )

        serializer = ProductSerializer(product)

        expected_fields = {
            "id",
            "name",
            "description",
            "price",
            "stock",
            "active",
            "category",
        }
        self.assertEqual(set(serializer.data.keys()), expected_fields)
