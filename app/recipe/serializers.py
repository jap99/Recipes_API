from rest_framework import serializers
from core.models import Tag, Ingredient, Recipe



# we'll link serializer model 
    # and we'll pull in the ID & the name values

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag 
        fields = ('id', 'name')
        read_only_fields = ('id',)

class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)

class RecipeSerializer(serializers.ModelSerializer):

    # lists the list of primary id of the ingredients
    ingredients = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Ingredient.objects.all()
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingredients', 'tags', 'time_minutes',
                   'price', 'link')
        read_only_fields = ('id',)