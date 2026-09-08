from django.test import TestCase

from api.models import Category
from api.serializers import CategorySerializer


class CategorySerializerTest(TestCase):
    def test_accepts_valid_data(self):
        data = {"name": "Ficção", "description": "Livros de ficção"}

        serializer = CategorySerializer(data=data)

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_requires_name(self):
        data = {"description": "Categoria sem nome"}

        serializer = CategorySerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_rejects_blank_name(self):
        data = {"name": "   ", "description": "Nome inválido"}

        serializer = CategorySerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_creates_category(self):
        data = {"name": "Técnico", "description": "Livros técnicos"}

        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        category = serializer.save()

        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(category.name, "Técnico")

    def test_returns_expected_fields(self):
        category = Category.objects.create(name="Infantil", description="Para crianças")

        serializer = CategorySerializer(category)

        self.assertEqual(set(serializer.data.keys()), {"id", "name", "description"})
