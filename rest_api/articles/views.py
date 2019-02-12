from rest_framework import viewsets

from .serializers import ArticleSerializer, TagSerializer
from .models import Article, Tag


class ArticleVies(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class TagVies(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
