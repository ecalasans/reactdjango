import pytest
from core.post.models import Post
from core.fixtures.user import user

# Create your tests here.
@pytest.mark.django_db
def test_create_post(user):
    post = Post.objects.create(author=user, body="Testando post...")

    assert post.author == user
    assert post.body is "Testando post..."
