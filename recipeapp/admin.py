from django.contrib import admin

from .models import Category, Ingredient, Recipe


@admin.action(description="Сбросить количество в ноль")
def reset_views(modeladmin, request, queryset):
    queryset.update(views=0)


class CategoryAdmin(admin.ModelAdmin):
    """Список категорий"""
    list_display = ['name', 'date_added']
    ordering = ['name', '-date_added']
    list_filter = ['date_added']
    search_fields = ['name']
    search_help_text = 'Поиск категории рецепта по имени (name)'

    """Отдельная категория"""
    readonly_fields = ['date_added']
    fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['name'],
            },
        ),
        (
            'Справочно',
            {
                'classes': ['collapse'],
                'description': 'Дата создания категории',
                'fields': ['date_added'],
            }
        ),
    ]


class IngredientAdmin(admin.ModelAdmin):
    """Список ингредиентов"""
    list_display = ['name', 'date_added']
    ordering = ['name', '-date_added']
    list_filter = ['date_added']
    search_fields = ['name']
    search_help_text = 'Поиск ингредиента по имени (name)'

    """Отдельный ингредиент"""
    readonly_fields = ['date_added']
    fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['name'],
            },
        ),
        (
            'Справочно',
            {
                'classes': ['collapse'],
                'description': 'Дата создания ингредиента',
                'fields': ['date_added'],
            }
        ),
    ]


class RecipeAdmin(admin.ModelAdmin):
    """Список рецептов"""
    list_display = ['name', 'display_categories', 'display_ingredients', 'author', 'views']
    ordering = ['name', 'author', '-views']
    list_filter = ['author', 'views']
    search_fields = ['description']
    search_help_text = 'Поиск по полю Описание рецепта (description)'
    actions = [reset_views]

    """Отдельный рецепт"""
    readonly_fields = ['date_added', 'date_updated', 'views']
    fieldsets = [
        (
            None,
            {
                'classes': ['wide'],
                'fields': ['name'],
            },
        ),
        (
            'Описание рецепта',
            {
                'classes': ['collapse'],
                'fields': ['description', 'steps', 'cooking_time', ],
            },
        ),
        (
            'Категории',
            {
                'fields': ['categories'],
            }
        ),
        (
            'Ингредиенты',
            {
                'fields': ['ingredients'],
            }
        ),
        (
            'Прочее',
            {
                'fields': ['author', 'photo', 'views', 'date_added', 'date_updated'],
            }
        ),
    ]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
