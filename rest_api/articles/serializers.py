from rest_framework import serializers

from .models import Article, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, validators=False)
    tags_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ('title', 'pub_date', 'description', 'author_name', 'tags_count', 'tags')

    def create(self, validated_data):
        print(validated_data)

        tags_data = validated_data.pop('tags')
        article = Article.objects.create(**validated_data)
        for tag_data in tags_data:
            tag = Tag.objects.update_or_create(**tag_data)
            article.tags.add(tag)

        return article

    def get_tags_count(self, obj):
        return obj.tags.count()
