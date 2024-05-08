from django import forms
from .models import Category, Ingredient, Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'description', 'steps', 'cooking_time', 'ingredients',
                  'categories', 'photo', 'author',)
        labels = {
            'name': 'Название',
            'description': 'Рецептура',
            'steps': 'Количество шагов',
            'cooking_time': 'Время приготовления, в мин.',
            'ingredients': 'Ингредиенты',
            'categories': 'Категории рецепта',
            'photo': 'Фото готового блюда',
            'author': 'Автор'}
        help_texts = {'ingredients': 'Выберите все необходимые ингредиенты с помощью удержания кнопки CTRL',
                      'categories': 'Выберите все необходимые категории с помощью удержания кнопки CTRL'}
        field_classes = {'author': forms.ModelChoiceField,
                         'ingredients': forms.ModelMultipleChoiceField,
                         'categories': forms.ModelMultipleChoiceField, }


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('name',)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
