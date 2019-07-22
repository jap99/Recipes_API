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

    # lists the primaryUID of the ingredients/tags
    # creates a primary key related field called "ingredients" & "tags" 
    ingredients = serializers.PrimaryKeyRelatedField(many=True, queryset=Ingredient.objects.all())
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'ingredients', 'tags', 'time_minutes','price', 'link')
        read_only_fields = ('id',)

class RecipeDetailSerializer(RecipeSerializer):

    # adopts the id and name field from the RecipeSerializer
    ingredients = IngredientSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)