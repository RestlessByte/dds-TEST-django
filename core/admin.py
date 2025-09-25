from django.contrib import admin
from .models import Status, Type, Category, Subcategory, Transaction

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id","name")
    search_fields = ("name",)

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ("id","name")
    search_fields = ("name",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name","type")
    list_filter = ("type",)
    search_fields = ("name",)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name","category","get_type")
    list_filter = ("category","category__type")
    search_fields = ("name",)
    def get_type(self, obj): return obj.category.type
    get_type.short_description = "Тип"

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id","date","status","type","category","subcategory","amount")
    list_filter = ("status","type","category","subcategory")
    search_fields = ("comment",)
    date_hierarchy = "date"
