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
    User.objects.create(username='wiki_grym', email='wiki@gmail.com', password='password1')
    with pytest.raises(IntegrityError) as exc_info:
        User.objects.create(username='wiki_grym', email='ala@gmail.com', password='password2')
    assert 'UNIQUE constraint failed' in str(exc_info.value)

