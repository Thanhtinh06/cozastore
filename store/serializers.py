from dataclasses import field
from store.models import Product
from rest_framework import serializers, status
from rest_framework.response import Response


class ProductSerializer(serializers.HyperlinkedModelSerializer):

    category = serializers.CharField(source='category_id')

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.price_sell = validated_data.get(
            'price_sell', instance.price_sell)
        instance.price_buy = validated_data.get(
            'price_buy', instance.price_buy)
        instance.image = validated_data.get('image', instance.image)
        instance.content = validated_data.get('content', instance.content)
        instance.inventory = validated_data.get(
            'inventory', instance.inventory)

        instance.save()
        return instance

    # Xoa
    def destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
