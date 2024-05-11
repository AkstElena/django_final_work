from django.urls import path
from .views import index, recipes, get_recipes_on_name, get_categories, get_ingredients, \
    get_recipes_on_categories, get_recipes_on_ingredients, update_recipe
from .views import add_recipe, add_categories, add_ingredients

urlpatterns = [
    path('', index, name='index'),
    path('recipes/', recipes, name='recipes'),
    path('recipe_create/', add_recipe, name='add_recipe'),
    path('recipe_update/<str:recipe_name>/', update_recipe, name='update_recipe'),
    path('recipes/<str:recipe_name>/', get_recipes_on_name, name='recipe'),
    path('categories/', get_categories, name='categories'),
    path('categories/<str:category>', get_recipes_on_categories, name='category_recipes'),
    path('category_create/', add_categories, name='add_categories'),
    path('ingredients/', get_ingredients, name='ingredients'),
    path('ingredient_create/', add_ingredients, name='add_ingredients'),
    path('ingredients/<str:ingredient>', get_recipes_on_ingredients, name='ingredient_recipes'),

]
