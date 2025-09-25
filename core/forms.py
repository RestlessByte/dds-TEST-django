from django import forms
from datetime import date
from .models import Transaction, Category, Subcategory

class TransactionForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(attrs={"type":"date","class":"form-control"}),
        initial=date.today,
    )

    class Meta:
        model = Transaction
        fields = ["date","status","type","category","subcategory","amount","comment"]
        widgets = {
            "status": forms.Select(attrs={"class":"form-select"}),
            "type": forms.Select(attrs={"class":"form-select", "id":"form-type"}),
            "category": forms.Select(attrs={
                "class":"form-select",
                "id":"form-category",
                "data-sub-url":"/dds/ajax/subcategories/"
            }),
            "subcategory": forms.Select(attrs={"class":"form-select","id":"form-subcategory"}),
            "amount": forms.NumberInput(attrs={"step":"0.01","class":"form-control"}),
            "comment": forms.Textarea(attrs={"rows":3,"class":"form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Базовые queryset'ы
        self.fields["category"].queryset = Category.objects.all()
        self.fields["subcategory"].queryset = Subcategory.objects.none()

        # Фильтрация категорий по выбранному типу (если передан)
        if "type" in self.data:
            try:
                type_id = int(self.data.get("type"))
                self.fields["category"].queryset = Category.objects.filter(type_id=type_id)
            except (TypeError, ValueError):
                pass
        elif self.instance.pk and self.instance.type_id:
            self.fields["category"].queryset = Category.objects.filter(type_id=self.instance.type_id)

        # Фильтрация подкатегорий по выбранной категории (если передана)
        if "category" in self.data:
            try:
                cat_id = int(self.data.get("category"))
                self.fields["subcategory"].queryset = Subcategory.objects.filter(category_id=cat_id)
            except (TypeError, ValueError):
                pass
        elif self.instance.pk and self.instance.category_id:
            self.fields["subcategory"].queryset = Subcategory.objects.filter(category_id=self.instance.category_id)
