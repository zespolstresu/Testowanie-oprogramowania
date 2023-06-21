import pytest
from bs4 import BeautifulSoup
from django.urls.base import reverse
from .models import Post
from users.models import Profile

# @pytest.fixture
# def posts():
#     user = User.objects.create_user(username='krisbuj', email='krisu@gmail.com',password='password')
#     author = Profile.objects.create(user=user)
#     return [
#         Post.objects.create(title='Przegapiłem mecz Polska-Mołdawia', content='Ale wstyd dla tej reprezentacji. Buuuu', author=author),
#         Post.objects.create(title='Niezwykłe odkrycie archeologiczne', content='Właśnie znaleziono zaginiony skarb starożytnych wikingów!', author=author),
#         Post.objects.create(title='Nowe badania potwierdzają skuteczność szczepionki', content='Naukowcy dowodzą, że szczepionka przeciwko COVID-19 jest bezpieczna i skuteczna.', author=author),
#     ]

@pytest.mark.django_db
def test_user_posts_page(client, posts):
    url = reverse("user-posts")
    response = client.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    for author in soup.find_all("div.article-metadata > a"):
        assert author.string == 'krisbuj', f"krisbuj is not the author of this post!"