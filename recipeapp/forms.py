from django import forms
from .models import Category, Ingredient, Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ('name', 'description', 'steps', 'cooking_time', 'ingredients',
                  'categories', 'photo')
        labels = {
            'name': 'Название',
            'description': 'Рецептура',
            'steps': 'Количество шагов, шт.',
            'cooking_time': 'Время приготовления, в мин.',
            'ingredients': 'Ингредиенты',
            'categories': 'Категории рецепта',
            'photo': 'Фото готового блюда'
        }
        help_texts = {'ingredients': 'Выберите все необходимые ингредиенты с помощью удержания кнопки CTRL',
                      'categories': 'Выберите все необходимые категории с помощью удержания кнопки CTRL'}
        field_classes = {'ingredients': forms.ModelMultipleChoiceField,
                         'categories': forms.ModelMultipleChoiceField}

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={
            'placeholder': 'Введите название', 'description': 'Описание процесса приготовления блюда'})
        self.fields['description'].widget = forms.Textarea(attrs={
            'placeholder': 'Описание процесса приготовления блюда, желательно с указание шагов'})


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ('name',)
        labels = {'name': 'Ингредиент'}

    def __init__(self, *args, **kwargs):
        super(IngredientForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={
            'placeholder': 'Введите название'})


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        labels = {'name': 'Категория'}

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={
            'placeholder': 'Введите название'})
