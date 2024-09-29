import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, UserManager
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404

from core.abstract.models import AbstractModel, AbstractManager

# Create your models here.
class UserManager(BaseUserManager, AbstractManager):
    # def getObjectByPublicId(self, public_id):
    #     try:
    #         instance = self.get(public_id=public_id)
    #         return instance
    #     except (ObjectDoesNotExist, ValueError, TypeError):
    #         return Http404

    def create_user(self, username, email, password=None, **kwargs):
        if username is None:
            raise TypeError('Usuários devem ter um nome!')

        if email is None:
            raise TypeError('Usuários devem ter um email!')

        if password is None:
            raise TypeError('Uma senha precisa ser definida!')

        user = self.model(username=username, email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password, **kwargs):
        if username is None:
            raise TypeError('Superusuários precisam ter um nome!')

        if email is None:
            raise TypeError('Superusuários precisam ter um email!')

        if password is None:
            raise TypeError('Uma senha precisa ser definida!')

        super_user = self.create_user(username, email, password, **kwargs)
        super_user.is_superuser = True
        super_user.is_staff = True
        super_user.save(using=self._db)

        return super_user



class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True)
    post_liked = models.ManyToManyField('core_post.Post', related_name='liked_by')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def like(self, post):
        # Adiciona um post que foi dado like por este usuário
        return self.post_liked.add(post)

    def removeLike(self, post):
        # Remove o post da lista de posts curtidos por este usuário
        return self.post_liked.remove(post)

    def hasLiked(self, post):
        # Retorna true se o usúario tiver dado algum like em algum post
        return self.post_liked.filter(pk=post.pk).exists()