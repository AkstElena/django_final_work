from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Category, Ingredient, Recipe
from .forms import CategoryForm, IngredientForm, RecipeForm


# Create your views here.
def index(request):
    return render(request, 'recipeapp/index.html')


def recipes(request):
    recipes = Recipe.objects.all()
    context = {'recipes': recipes, 'name': 'Рецепты'}
    return render(request, 'recipeapp/recipes.html', context)


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        message = 'Ошибка в данных'
        if form.is_valid():
            name = form.cleaned_data['name']
            form.save()
            return redirect('recipe', recipe_name=name)
    else:
        form = RecipeForm()
        message = 'Заполните форму'
    return render(request, 'recipeapp/form_add.html', {'form': form, 'message': message})


def get_recipes_on_name(request, recipe_name):
    recipe = Recipe.objects.filter(name=recipe_name).first()
    if recipe is not None:
        context = {'recipe': recipe, 'name': f'Рецепт {recipe_name}'}
        return render(request, 'recipeapp/recipe.html', context)
    return render(request, 'recipeapp/404.html',
                  {'text': f'Рецепта с названием {recipe_name} не обнаружено',
                   'name': 'Данные не обнаружены'})


def update_recipe(request, recipe_name):
    recipe = Recipe.objects.filter(name=recipe_name).first()
    if recipe is not None:
        if request.method == 'POST':
            form = RecipeForm(request.POST, request.FILES)
            message = 'Ошибка в данных'
            if form.is_valid():
                name = form.cleaned_data['name']
                form.save()
                return redirect('recipe', recipe_name=name)
        else:
            form = RecipeForm()
            message = 'Введите новые данные по товару'
        return render(request, 'recipeapp/form_edit.html', {'form': form,
                                                            'message': message,
                                                            'name': 'Текущие данные рецепта',
                                                            'recipe': recipe})
    return render(request, 'recipeapp/404.html',
                  {'text': f'Рецепта с названием {recipe_name} не найдено',
                   'name': 'Данные не обнаружены'})


# def get_recipes_on_categories(request, category):
#     recipes = Recipe.objects.all()
#     all_recipes = []
#     for recipe in recipes:
#         for el in recipe.categories.all():
#             if el.name == category:
#                 all_recipes.append(recipe)
#     if all_recipes is not None:
#         context = {'recipes': all_recipes, 'name': f'Рецепты по категории {category}'}
#         return render(request, 'recipeapp/recipes.html', context)
#     return render(request, 'recipeapp/404.html',
#                   {'text': f'Рецептов в категории {category} не обнаружено',
#                    'name': 'Данные не обнаружены'})

@login_required
def get_recipes_on_categories(request, category):
    recipes = Recipe.objects.all()
    all_recipes = []
    for recipe in recipes:
        if category in recipe.display_categories():
            all_recipes.append(recipe)
    if all_recipes:
        context = {'recipes': all_recipes, 'name': f'Рецепты по категории {category}'}
        return render(request, 'recipeapp/recipes.html', context)
    return render(request, 'recipeapp/404.html',
                  {'text': f'Рецептов в категории {category} не обнаружено',
                   'name': 'Данные не обнаружены'})


@login_required
def get_recipes_on_ingredients(request, ingredient):
    recipes = Recipe.objects.all()
    all_recipes = []
    for recipe in recipes:
        if ingredient in recipe.display_ingredients():
            all_recipes.append(recipe)
    if all_recipes:
        context = {'recipes': all_recipes, 'name': f'Рецепты по категории {ingredient}'}
        return render(request, 'recipeapp/recipes.html', context)
    return render(request, 'recipeapp/404.html',
                  {'text': f'Рецептов в категории {ingredient} не обнаружено',
                   'name': 'Данные не обнаружены'})


def get_categories(request):
    categories = Category.objects.all()
    categories_dict = {index: value for index, value in enumerate(categories, 1)}
    context = {'categories': categories_dict, 'name': 'Категории рецептов'}
    return render(request, 'recipeapp/categories.html', context)


@login_required
def add_categories(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        message = 'Ошибка в данных'
        if form.is_valid():
            form.save()
            return redirect('categories')
    else:
        form = CategoryForm()
        message = 'Заполните форму'
    return render(request, 'recipeapp/form_add.html', {'form': form, 'message': message})


def get_ingredients(request):
    ingredients = Ingredient.objects.all()
    categories_dict = {index: value for index, value in enumerate(ingredients, 1)}
    context = {'categories': categories_dict, 'name': 'Текущие ингредиенты'}
    return render(request, 'recipeapp/ingredients.html', context)


@login_required
def add_ingredients(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        message = 'Ошибка в данных'
        if form.is_valid():
            form.save()
            return redirect('ingredients')
    else:
        form = IngredientForm()
        message = 'Заполните форму'
    return render(request, 'recipeapp/form_add.html', {'form': form, 'message': message})
