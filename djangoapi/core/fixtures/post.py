import pytest

from core.fixtures.user import user
from core.post.models import Post

@pytest.fixture
def post(db, user):
    post = Post.objects.create(author=user,
                               body="Teste de post...")

    return post