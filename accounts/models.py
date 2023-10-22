from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from os.path import join
from django.utils.timezone import now


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    mobile = models.CharField(max_length=20, null=True)
    is_online = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_seen = models.DateTimeField(blank=False,
        null=False, auto_now_add=True)
    date_joined = models.DateTimeField(default=now ,blank=False,
        null=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    @property
    def full_name(self):
        return str(self.first_name)+' '+str(self.last_name)


def get_sentinal_user():
    return get_user_model().objects.get_or_create(first_name="deleted")[0]


class UserGroup(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.SET(get_sentinal_user))
    group_info = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name="all_groups")

    def last_10_messages(grp_name, times=0):
        group = UserGroup.objects.get(group_name=grp_name)
        if not times:
            return list(group.messages.order_by("date_posted"))[-30:]
        return list(group.messages.order_by("date_posted"))[(-30*(times+1)):(-30*times)]
    
    def __str__(self) -> str:
        return self.name


def get_image_path(instance, filename):
    return join("profile_pics", instance.user.full_name, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.jpg", upload_to=get_image_path)

    def __str__(self):
        return self.user.full_name


def get_group_image_path(instance, filename):
    return join("group_profile_pics", instance.group.name, filename)


class UserGroupProfile(models.Model):
    group = models.OneToOneField(UserGroup, on_delete=models.CASCADE)
    image = models.ImageField(
        default="default_group.jpg", upload_to=get_group_image_path
    )

    def __str__(self):
        return self.group.name
