import pytest
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from .models import Profile

@pytest.mark.django_db
def test_profile_create():
    user = User.objects.create(username='kris_buj00')
    user.set_password('password')
    user.save()
    profile, created = Profile.objects.get_or_create(user=user, defaults={'image': 'profile.jpg'})

    assert created or Profile.objects.filter(user=user).exists(), "The profile for user 'kris_buj00' was not created correctly!"
    

@pytest.mark.django_db
def test_profile_is_unique():
    with pytest.raises(IntegrityError):
        User.objects.create_user(username='wiki_grym', email='wiki@gmail.com',password='password1')
        User.objects.create_user(username='ala_grom', email='ala@gmail.com',password='password2')

