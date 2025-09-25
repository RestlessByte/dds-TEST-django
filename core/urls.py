from django.urls import path
from .views import (
    TransactionListView, TransactionCreateView, TransactionUpdateView,
    TransactionDeleteView, DictionariesView, subcategories_for_category
)

urlpatterns = [
    path("", TransactionListView.as_view(), name="transaction_list"),
    path("new/", TransactionCreateView.as_view(), name="transaction_create"),
    path("<int:pk>/edit/", TransactionUpdateView.as_view(), name="transaction_edit"),
    path("<int:pk>/delete/", TransactionDeleteView.as_view(), name="transaction_delete"),
    path("dicts/", DictionariesView.as_view(), name="dicts"),
    path("ajax/subcategories/", subcategories_for_category, name="ajax_subcategories"),
]
