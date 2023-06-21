import pytest
from django.urls import reverse
from bs4 import BeautifulSoup
from blog.models import Post
from django.db import IntegrityError
from django.db import transaction
from django.utils import timezone
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_post_create():
    user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword')
    Post.objects.create(
            title='Test Post',
            file=None,
            content='Test Content',
            date_posted=timezone.now(),
            author=user)
    assert Post.objects.filter(title='Test Post').exists(), "Post with title 'Test Post' was not created correctly!"

# @pytest.mark.django_db
# def test_post_unique():
#     user = User.objects.create_user(
#                 username='testuser',
#                 email='testuser@example.com',
#                 password='testpassword')
#     with pytest.raises(IntegrityError), transaction.atomic():
#         Post.objects.create(
#             title='Test Post',
#             file=None,
#             content='Test Content',
#             date_posted=timezone.now(),
#             author=user)
#         Post.objects.create(
#             title='Test Post',
#             file=None,
#             content='Test Content',
#             date_posted=timezone.now(),
#             author=user)

@pytest.fixture
def post_list():
    user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword')
    return [
        Post.objects.create(
            title='Post nr 1',
            file=None,
            content='Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
            date_posted=timezone.now(),
            author=user),
        Post.objects.create(
            title='Post nr 2',
            file=None,
            content='Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
            date_posted=timezone.now(),
            author=user),
        Post.objects.create(
            title='Post nr 3',
            file=None,
            content='Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
            date_posted=timezone.now(),
            author=user),
        Post.objects.create(
            title='Post nr 4',
            file=None,
            content='Lorem Ipsum is simply dummy text of the printing and typesetting industry.',
            date_posted=timezone.now(),
            author=user)
        ]

@pytest.mark.django_db
def test_pagination_first(client, post_list):
    url = reverse("blog-home")
    response = client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    element = soup.find('a', class_='btn btn-outline-info mb-4', text='First')
    assert element is None

@pytest.mark.django_db
def test_pagination_last(client, post_list):
    url = reverse("blog-home")
    response = client.get(url + "?page=2")
    soup = BeautifulSoup(response.content, "html.parser")
    element = soup.find('a', class_='btn btn-outline-info mb-4', text='Last')
    assert element is None

@pytest.mark.django_db
def test_search(client, post_list):
    url = reverse("search")
    response = client.get(url + "?q=Post+nr+4")
    soup = BeautifulSoup(response.content, "html.parser")
    element = soup.find('a', class_='article-title text-justify', text='Post nr 4')
    assert element is not None