from rest_framework import generics

from .models import Article, Tag
from .serializers import ArticleSerializer, TagSerializer


class ArticleBaseView:
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    tags_to_append = []

    def after_create(self, serializer: ArticleSerializer, update=None):
        article = Article.objects.get(**serializer.validated_data)

        if update:
            article.tags.clear()

        for tag in self.tags_to_append:
            tag, created = Tag.objects.get_or_create(**tag)
            article.tags.add(tag)


class TagBaseView:
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArticleListView(ArticleBaseView, generics.ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        if 'tags' in request.data:
            self.tags_to_append += request.data.pop('tags')
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self.after_create(serializer)


class ArticleDetailView(ArticleBaseView, generics.RetrieveUpdateDestroyAPIView):
    def put(self, request, *args, **kwargs):
        if 'tags' in request.data:
            self.tags_to_append += request.data.pop('tags')
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if 'tags' in request.data:
            self.tags_to_append += request.data.pop('tags')
        return super().patch(request, *args, **kwargs)

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self.after_create(serializer, update=True)


class TagListView(TagBaseView, generics.ListCreateAPIView):
    pass


class TagDetailView(TagBaseView, generics.RetrieveUpdateDestroyAPIView):
    pass
