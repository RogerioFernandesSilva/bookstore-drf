from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Category, Order, Product
from .serializers import CategorySerializer, OrderSerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações de CRUD sobre Category.

    Endpoints gerados automaticamente pelo router:
        GET    /api/categories/          -> list
        POST   /api/categories/          -> create
        GET    /api/categories/{pk}/     -> retrieve
        PUT    /api/categories/{pk}/     -> update
        PATCH  /api/categories/{pk}/     -> partial_update
        DELETE /api/categories/{pk}/     -> destroy
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações de CRUD sobre Product.

    `select_related` evita consultas extras ao banco ao acessar a
    categoria relacionada na representação aninhada do serializer.
    """

    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    ViewSet para operações de CRUD sobre Order.

    `select_related` evita consultas extras ao acessar o produto (e a
    categoria do produto) na representação aninhada do serializer.

    Exige autenticação via Token: o cliente precisa enviar o header
    `Authorization: Token <token>` para acessar qualquer endpoint
    desta ViewSet. As demais ViewSets (Category, Product) não são
    afetadas — continuam sem restrição.
    """

    queryset = Order.objects.select_related("product", "product__category").all()
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]