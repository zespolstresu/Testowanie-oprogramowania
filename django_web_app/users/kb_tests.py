import pytest
from django.contrib.auth.models import User
from .models import Profile

@pytest.mark.django_db
def test_profile_create():
    # Create a user
    user = User.objects.create(username='kris_buj00')
    user.set_password('password')
    user.save()

    # Create or retrieve the profile for the user
    profile, created = Profile.objects.get_or_create(user=user, defaults={'image': 'profile.jpg'})

    assert created or Profile.objects.filter(user=user).exists(), "The profile for user 'kris_buj00' was not created correctly!"