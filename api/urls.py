from django.urls import path
from .views import ProductList, ProductDetail, CategoryDetail, CategoryList

urlpatterns = [
    path('products/', ProductList.as_view(), name='products-list-create'),
    path('products/<int:pk>', ProductDetail.as_view(), name='product-details'),
    path('categories/', CategoryList.as_view(), name='categories-list-create'),
    path('categories/<int:pk>', CategoryDetail.as_view(), name='category-details'),

]
