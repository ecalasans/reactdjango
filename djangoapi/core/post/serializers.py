from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.abstract.serializers import AbstractSerializer
from core.post.models import Post
from core.user.models import User
from core.user.serializers import UserSerializer


class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(slug_field='public_id',
                                          queryset=User.objects.all())
    liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def validate_author(self, value):
        if self.context['request'].user != value:
            raise ValidationError('Você não pode criar um post por outro usuário!')
        return value

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        print(rep)

        author = User.objects.getObjectByPublicId(rep['author'])

        rep['author'] = UserSerializer(author).data

        return rep

    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True

            instance = super().update(instance, validated_data)

            return instance

    def get_liked(self, instance):
        request = self.context.get('request', None)

        if request is None or request.user.is_anonymous:
            return False

        return request.user.hasLiked(instance)  # Retorna o valor de retorno da função hasLiked definida no modelo

    def get_likes_count(self, instance):
        return instance.liked_by.count()

    class Meta:
        model = Post
        fields = ['id', 'author', 'body', 'edited', 'liked', 'likes_count', 'created', 'updated']
        read_only_fields = ['edited']