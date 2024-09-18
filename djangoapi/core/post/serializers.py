from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.abstract.serializers import AbstractSerializer
from core.post.models import Post
from core.user.models import User

class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(slug_field='public_id',
                                          queryset=User.objects.all())

    def validate_author(self, value):
        if self.context['request'].user != value:
            raise ValidationError('Você não pode criar um post por outro usuário!')
        return value

    class Meta:
        model = Post
        fields = ['id', 'author', 'body', 'edited', 'created', 'updated']
        read_only_fields = ['edited']