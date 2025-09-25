from django.urls import path
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status as drf_status
from .models import Status, Type, Category, Subcategory, Transaction
from .serializers import (
    StatusSerializer, TypeSerializer, CategorySerializer, SubcategorySerializer, TransactionSerializer
)

@api_view(["GET","POST"])
def statuses(request):
    if request.method == "POST":
        ser = StatusSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(StatusSerializer(obj).data, status=drf_status.HTTP_201_CREATED)
    return Response(StatusSerializer(Status.objects.all(), many=True).data)

@api_view(["GET","POST"])
def types(request):
    if request.method == "POST":
        ser = TypeSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(TypeSerializer(obj).data, status=drf_status.HTTP_201_CREATED)
    return Response(TypeSerializer(Type.objects.all(), many=True).data)

@api_view(["GET","POST"])
def categories(request):
    if request.method == "POST":
        ser = CategorySerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(CategorySerializer(obj).data, status=drf_status.HTTP_201_CREATED)
    type_id = request.GET.get("type")
    qs = Category.objects.all()
    if type_id: qs = qs.filter(type_id=type_id)
    return Response(CategorySerializer(qs, many=True).data)

@api_view(["GET","POST"])
def subcategories(request):
    if request.method == "POST":
        ser = SubcategorySerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        obj = ser.save()
        return Response(SubcategorySerializer(obj).data, status=drf_status.HTTP_201_CREATED)
    category_id = request.GET.get("category")
    qs = Subcategory.objects.all()
    if category_id: qs = qs.filter(category_id=category_id)
    return Response(SubcategorySerializer(qs, many=True).data)

@api_view(["GET","POST"])
def transactions(request):
    if request.method == "POST":
        ser = TransactionSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=drf_status.HTTP_201_CREATED)
    qs = Transaction.objects.all()
    g = request.GET
    if g.get("date_from"): qs = qs.filter(date__gte=g["date_from"])
    if g.get("date_to"): qs = qs.filter(date__lte=g["date_to"])
    for f in ("status","type","category","subcategory"):
        if g.get(f): qs = qs.filter(**{f+"_id": g[f]})
    return Response(TransactionSerializer(qs, many=True).data)

urlpatterns = [
    path("statuses/", statuses),
    path("types/", types),
    path("categories/", categories),
    path("subcategories/", subcategories),
    path("transactions/", transactions),
]
