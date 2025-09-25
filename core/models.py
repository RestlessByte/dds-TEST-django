from django.core.validators import MinValueValidator
from django.db import models
from django.core.exceptions import ValidationError

class Status(models.Model):
    name = models.CharField(max_length=64, unique=True)
    def __str__(self): return self.name

class Type(models.Model):
    name = models.CharField(max_length=64, unique=True)  # Пополнение / Списание + расширяемо
    def __str__(self): return self.name

class Category(models.Model):
    name = models.CharField(max_length=128)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="categories")
    class Meta:
        unique_together = ("name","type")
        verbose_name_plural = "Категории"
    def __str__(self): return f"{self.name} ({self.type})"

class Subcategory(models.Model):
    name = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    class Meta:
        unique_together = ("name","category")
        verbose_name_plural = "Подкатегории"
    def __str__(self): return f"{self.name} ⇐ {self.category}"

class Transaction(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(help_text="Дата создания/учёта записи", null=False, blank=False)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="transactions")
    type = models.ForeignKey(Type, on_delete=models.PROTECT, related_name="transactions")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="transactions")
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT, related_name="transactions")
    amount = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0.01)])  # рубли
    comment = models.TextField(blank=True, default="")

    class Meta:
        ordering = ["-date","-id"]

    def clean(self):
        # Логические зависимости: subcategory->category->type
        if self.category and self.type and self.category.type_id != self.type_id:
            raise ValidationError({"category": "Категория не относится к выбранному типу."})
        if self.subcategory and self.category and self.subcategory.category_id != self.category_id:
            raise ValidationError({"subcategory": "Подкатегория не принадлежит выбранной категории."})

    def __str__(self):
        return f"{self.date} | {self.type} | {self.category}/{self.subcategory} | {self.amount}₽"
