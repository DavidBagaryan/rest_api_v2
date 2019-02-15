from rest_framework import generics

from .serializers import ArticleSerializer, TagSerializer
from .models import Article, Tag


class ArticleBase:
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    existed_tags = []
    new_tags = []

    def filter_tags(self, request):
        requested_tags = request.data.pop('tags')
        for tag in requested_tags:
            tag_exists = Tag.objects.filter(**tag).first()
            if tag_exists:
                self.existed_tags.append(tag_exists)
            else:
                self.new_tags.append(tag)

        return request

    def add_related_data(self, serializer):
        saved_article = Article.objects.get(**serializer.validated_data)

        """TODO solve the problem with tags remaining"""
        # tags_list = set(self.existed_tags) | set(self.new_tags)
        # print(tags_list)

        for tag in self.existed_tags:
            saved_article.tags.add(tag)

        for tag in self.new_tags:
            tag, created = Tag.objects.get_or_create(**tag)
            saved_article.tags.add(tag)


class TagBase:
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ArticleList(ArticleBase, generics.ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        filtered_request = self.filter_tags(request)
        return super().post(filtered_request, *args, **kwargs)

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self.add_related_data(serializer)


class ArticleDetail(ArticleBase, generics.RetrieveUpdateDestroyAPIView):
    def put(self, request, *args, **kwargs):
        filtered_request = self.filter_tags(request)
        return super().put(filtered_request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        filtered_request = self.filter_tags(request)
        return super().patch(filtered_request, *args, **kwargs)

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self.add_related_data(serializer)


class TagList(TagBase, generics.ListCreateAPIView):
    pass


class TagDetail(TagBase, generics.RetrieveUpdateDestroyAPIView):
    pass
