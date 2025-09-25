from django.views.generic import RedirectView, ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.db.models import Q
from django.http import JsonResponse
from .models import Transaction, Status, Type, Category, Subcategory
from .forms import TransactionForm

class HomeRedirectView(RedirectView):
    pattern_name = "transaction_list"

class TransactionListView(ListView):
    model = Transaction
    template_name = "core/transaction_list.html"
    paginate_by = 20
    context_object_name = "items"

    def get_queryset(self):
        qs = Transaction.objects.select_related("status","type","category","subcategory").all()
        g = self.request.GET
        date_from = g.get("date_from"); date_to = g.get("date_to")
        status_id = g.get("status"); type_id = g.get("type")
        category_id = g.get("category"); subcategory_id = g.get("subcategory")
        if date_from: qs = qs.filter(date__gte=date_from)
        if date_to: qs = qs.filter(date__lte=date_to)
        if status_id: qs = qs.filter(status_id=status_id)
        if type_id: qs = qs.filter(type_id=type_id)
        if category_id: qs = qs.filter(category_id=category_id)
        if subcategory_id: qs = qs.filter(subcategory_id=subcategory_id)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["statuses"] = Status.objects.all()
        ctx["types"] = Type.objects.all()
        ctx["categories"] = Category.objects.all()
        ctx["subcategories"] = Subcategory.objects.all()
        g = self.request.GET
        ctx["f"] = {
            "date_from": g.get("date_from",""),
            "date_to": g.get("date_to",""),
            "status": g.get("status",""),
            "type": g.get("type",""),
            "category": g.get("category",""),
            "subcategory": g.get("subcategory",""),
        }
        return ctx

class TransactionCreateView(CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "core/transaction_form.html"
    success_url = reverse_lazy("transaction_list")

class TransactionUpdateView(UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "core/transaction_form.html"
    success_url = reverse_lazy("transaction_list")

class TransactionDeleteView(DeleteView):
    model = Transaction
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy("transaction_list")

# Управление справочниками — простой экран с формами добавления/удаления
from django.views import View
from django.shortcuts import render, redirect

class DictionariesView(View):
    template_name = "core/dicts.html"
    def get(self, request):
        return render(request, self.template_name, {
            "statuses": Status.objects.all(),
            "types": Type.objects.all(),
            "categories": Category.objects.select_related("type").all(),
            "subcategories": Subcategory.objects.select_related("category","category__type").all(),
        })
    def post(self, request):
        action = request.POST.get("action")
        model = request.POST.get("model")
        name = request.POST.get("name","").strip()
        if action == "add" and name and model in {"status","type","category","subcategory"}:
            if model == "status":
                Status.objects.get_or_create(name=name)
            elif model == "type":
                Type.objects.get_or_create(name=name)
            elif model == "category":
                type_id = request.POST.get("type_id")
                if type_id:
                    Category.objects.get_or_create(name=name, type_id=type_id)
            elif model == "subcategory":
                category_id = request.POST.get("category_id")
                if category_id:
                    Subcategory.objects.get_or_create(name=name, category_id=category_id)
        elif action == "delete" and model and request.POST.get("id"):
            mdl = {"status":Status,"type":Type,"category":Category,"subcategory":Subcategory}[model]
            try:
                mdl.objects.get(id=request.POST["id"]).delete()
            except Exception: pass
        return redirect("dicts")

# AJAX: вернуть подкатегории по категории
def subcategories_for_category(request):
    cat_id = request.GET.get("category_id")
    data = []
    if cat_id:
        subs = Subcategory.objects.filter(category_id=cat_id).values("id","name")
        data = list(subs)
    return JsonResponse({"items": data})
