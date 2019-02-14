from rest_framework import generics

from .serializers import ArticleSerializer, TagSerializer
from .models import Article, Tag


class ArticleBase:
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    existed_tags = []

    def filter_tags(self, request):
        """
        TODO solve the problem with tags remaining
        """
        requested_tags = request.data.get('tags')
        new_tags = []

        for tag in requested_tags:
            existed_tag, new = Tag.objects.update_or_create(**tag)
            if not new:
                self.existed_tags.append(existed_tag)
                request.data['tags'].remove(tag)

        print(request.data)
        return request

    def add_related_data(self, serializer):
        serializer.validated_data.pop('tags')
        saved_article = Article.objects.get(**serializer.validated_data)

        # print(self.existed_tags)

        for tag in self.existed_tags:
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
