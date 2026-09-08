from rest_framework import serializers

from .models import Category, Order, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "O nome da categoria não pode ser vazio."
            )
        return value


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer de Product.

    A categoria é exibida de forma aninhada (somente leitura) através do
    campo `category`, respeitando o relacionamento ForeignKey definido no
    modelo. Para criar/atualizar um produto, informe o id da categoria em
    `category_id`.
    """

    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="category",
        write_only=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "active",
            "category",
            "category_id",
        ]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("O preço deve ser maior que zero.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "O estoque não pode ser negativo."
            )
        return value


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer de Order.

    O produto relacionado é exibido de forma aninhada (somente leitura)
    através do campo `product`. Para criar um pedido, informe o id do
    produto em `product_id`.
    """

    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "product",
            "product_id",
            "customer_name",
            "quantity",
            "status",
            "created_at",
        ]
        read_only_fields = ["created_at", "status"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "A quantidade deve ser maior que zero."
            )
        return value

    def validate(self, attrs):
        # Validação cruzada: não permite pedir mais do que há em estoque.
        product = attrs.get("product")
        quantity = attrs.get("quantity")
        if product is not None and quantity is not None and quantity > product.stock:
            raise serializers.ValidationError(
                {
                    "quantity": (
                        f"Estoque insuficiente. Disponível: {product.stock}."
                    )
                }
            )
        return attrs
