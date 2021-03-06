from rest_framework import serializers

from logistic.models import Product, Stock, StockProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    product = ProductSerializer
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for p in positions:
            StockProduct.objects.update_or_create(stock=stock,
                                                  product=p['product'],
                                                  defaults={'quantity': p['quantity'], 'price': p['price']})
        return stock

    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        for item in validated_data:
            if Stock._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        StockProduct.objects.filter(stock=instance).delete()
        for p in positions:
            d = dict(p)
            StockProduct.objects.create(stock=instance,
                                        product=d['product'],
                                        quantity=d['quantity'],
                                        price=d['price'])
        instance.save()
        return instance
