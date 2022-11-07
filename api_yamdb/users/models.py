import secrets
import string

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'
SUPERUSER = 'superuser'

ROLE = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
    (SUPERUSER, SUPERUSER),
]


class UserManager(BaseUserManager):
    def create_user(
            self, username, email, password=None, role=USER, bio=None
    ):
        if username is None:
            raise TypeError('Users must have a username.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(
            username=username, email=self.normalize_email(email)
        )
        if role == ADMIN:
            user.is_admin = True
        else:
            user.is_admin = False
        user.role = role
        user.set_password(password)
        user.is_active = True
        user.generate_confirmation_code()
        user.save()

        return user

    def create_staffuser(
            self, username, email, password, role=ADMIN, bio=None
    ):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            bio=bio
        )
        user.is_staff = True
        user.is_active = True
        user.save()
        return user

    def create_superuser(
            self, username, email, password, role=SUPERUSER, bio=None
    ):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            role=role,
            bio=bio
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[\w.@+-]+',
                message='Letters, digits and @/./+/-/_ only',
            )
        ]
    )
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=15,
        choices=ROLE,
        default=USER
    )
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    confirmation_code = models.CharField(
        max_length=100,
        null=True
    )

    objects = UserManager()

    def generate_confirmation_code(self):
        self.confirmation_code = ''.join((
            secrets.choice(
                string.ascii_letters
                + string.digits
            ) for i in range(8)
        ))
