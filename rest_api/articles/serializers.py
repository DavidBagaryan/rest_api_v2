from rest_framework import serializers

from .models import Article, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    tags_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('id', 'title', 'pub_date', 'description', 'author_name', 'tags_count', 'tags')

    @staticmethod
    def get_tags_count(obj):
        return obj.tags.count()
