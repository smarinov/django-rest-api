from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class ProductList(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category')
        if category is not None:
            queryset = queryset.filter(category__category_name=category)
        return queryset

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(seller=self.request.user)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CategoryList(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]

