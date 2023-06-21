import pytest
import requests
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
    soup = BeautifulSoup(response.content, "html.parser")
    for author in soup.find_all("div.article-metadata > a"):
        assert author.string == 'krisbuj', f"krisbuj is not the author of this post!"
        
        
def test_main_page_title(client):
    url = reverse("blog-home")
    response = client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("nav").find("a").text.lower().strip() == "django webapp", "Incorrect page title!"
        
def test_response_status(client):
    url = reverse("i-dont-exist")
    response = client.get(url)
    assert response.status_code == 404, "This page is not supposed to exist!"
    
def test_image_download(client):
    url = reverse("blog-home")
    response = client.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    download_links = soup.find_all('a', attrs={'download': True})

    for link in download_links:
        image_url = link['href']
        image_response = requests.get(image_url)
        assert image_response.status_code == 200