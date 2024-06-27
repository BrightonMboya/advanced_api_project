from django.shortcuts import render

# Create your views here.
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .seriealizers import BookSerializer
from django_filters import rest_framework as django_filters

class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    publication_year = django_filters.NumberFilter(field_name='publication_year')

    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']


class BookListView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author_name']
    ordering_fields = ['title', 'publication_year']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Additional custom filtering based on request parameters, if needed
        # Example: filtering by a specific author ID passed in the URL query
        author_id = self.request.query_params.get('author_id')
        if author_id:
            queryset = queryset.filter(author_id=author_id)

        return queryset

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

