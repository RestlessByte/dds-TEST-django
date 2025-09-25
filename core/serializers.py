from rest_framework import serializers
from .models import Status, Type, Category, Subcategory, Transaction

class StatusSerializer(serializers.ModelSerializer):
    class Meta: model = Status; fields = ["id","name"]

class TypeSerializer(serializers.ModelSerializer):
    class Meta: model = Type; fields = ["id","name"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta: model = Category; fields = ["id","name","type"]

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta: model = Subcategory; fields = ["id","name","category"]

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id","date","status","type","category","subcategory","amount","comment"]
    def validate(self, attrs):
        category = attrs.get("category")
        typ = attrs.get("type")
        subcategory = attrs.get("subcategory")
        if category and typ and category.type_id != typ.id:
            raise serializers.ValidationError({"category":"Категория не относится к выбранному типу."})
        if subcategory and category and subcategory.category_id != category.id:
            raise serializers.ValidationError({"subcategory":"Подкатегория не принадлежит выбранной категории."})
        return attrs
