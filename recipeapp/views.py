from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Category, Ingredient, Recipe
from .forms import CategoryForm, IngredientForm, RecipeForm
from django.core.paginator import Paginator


def index(request):
    recipes = Recipe.objects.all().order_by('-views')[:5]
    context = {'recipes': recipes, 'name': 'Рецепты'}
    return render(request, 'recipeapp/index.html', context)


def recipes(request):
    recipes = Recipe.objects.all().order_by('-views')
    paginator = Paginator(recipes, per_page=4)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    context = {'recipes': page_object, 'name': 'Рецепты'}
    return render(request, 'recipeapp/recipes.html', context)


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        message = 'Ошибка в данных'
        if form.is_valid():
            name = form.cleaned_data['name']
            recipe = form.save()
            recipe.author = request.user
            recipe.save()
            return redirect('recipe', recipe_name=name)
    else:
        form = RecipeForm()
        message = 'Заполните форму'
    return render(request, 'recipeapp/form_add.html', {'form': form, 'message': message})


@login_required
def get_recipes_on_name(request, recipe_name):
    recipe = Recipe.objects.filter(name=recipe_name).first()
    if recipe is not None:
        recipe.views += 1
        recipe.save()
        context = {'recipe': recipe, 'name': f'Рецепт {recipe_name}'}
        return render(request, 'recipeapp/recipe.html', context)
    return render(request, 'recipeapp/404.html',
                  {'text': f'Рецепта с названием {recipe_name} не обнаружено',
                   'name': 'Данные не обнаружены'})


@login_required
def update_recipe(request, recipe_name):
    recipe = Recipe.objects.filter(name=recipe_name).first()
    if recipe is not None:
        if recipe.author == request.user:
            if request.method == 'POST':
                form = RecipeForm(request.POST, request.FILES, instance=recipe)
                message = 'Ошибка в данных'
                if form.is_valid():
                    name = form.cleaned_data['name']
                    form.save()
                    return redirect('recipe', recipe_name=name)
            else:
                form = RecipeForm(instance=recipe)
                message = 'Редактирование рецепта'
            return render(request, 'recipeapp/form_edit.html', {'form': form,
                                                                'message': message,
                                                                'recipe': recipe})
        else:
            return render(request, 'recipeapp/404.html',
                          {'text': f'Автором рецепта: {recipe_name} является другой пользователь',
                           'name': 'Данные не обнаружены'})
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
        paginator = Paginator(all_recipes, per_page=4)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        context = {'recipes': page_object, 'name': f'Рецепты по категории: {category}'}
        # context = {'recipes': all_recipes, 'name': f'Рецепты по категории: {category}'}
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
        paginator = Paginator(all_recipes, per_page=4)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        context = {'recipes': page_object, 'name': f'Рецепты содержащие ингредиент:  {ingredient}'}
        # context = {'recipes': all_recipes, 'name': f'Рецепты содержащие ингредиент:  {ingredient}'}
        return render(request, 'recipeapp/recipes.html', context)
    return render(request, 'recipeapp/404.html',
                  {'text': f'Рецептов c ингредиентом {ingredient} не обнаружено',
                   'name': 'Данные не обнаружены'})


def get_categories(request):
    categories = Category.objects.all()
    paginator = Paginator(categories, per_page=40)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    context = {'categories': page_object, 'name': 'Категории рецептов'}
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
    paginator = Paginator(ingredients, per_page=40)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    context = {'categories': page_object, 'name': 'Ингредиенты'}
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
