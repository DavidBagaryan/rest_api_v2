from django.shortcuts import get_object_or_404
from rest_framework import generics

from .serializers import ArticleSerializer, TagSerializer
from .models import Article, Tag


class ArticleBase:
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    existed_tags = []

    def filter_tags(self, request):
        """
        TODO solve problem with unsaved, existed tags
        """
        tags = request.data.get('tags')
        new_tags = [tag for tag in tags if not Tag.objects.filter(**tag)]
        request.data['tags'] = new_tags
        self.existed_tags = [Tag.objects.get(**tag) for tag in tags if Tag.objects.filter(**tag)]
        return request


class TagBase:
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArticleList(ArticleBase, generics.ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        filtered_request = self.filter_tags(request)
        if super().post(filtered_request, *args, **kwargs):
            request_article_data = filtered_request.data.copy()
            request_article_data.pop('tags')
            existed_article = Article.objects.get(**request_article_data)

            for tag in self.existed_tags:
                existed_article.tags.add(tag)


class ArticleDetail(ArticleBase, generics.RetrieveUpdateDestroyAPIView):
    def put(self, request, *args, **kwargs):
        filtered_request = self.filter_tags(request)
        return super().put(filtered_request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        filtered_request = self.filter_tags(request)
        return super().patch(filtered_request, *args, **kwargs)


class TagList(TagBase, generics.ListCreateAPIView):
    pass


class TagDetail(TagBase, generics.RetrieveUpdateDestroyAPIView):
    pass
