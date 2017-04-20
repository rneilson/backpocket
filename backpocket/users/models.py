import datetime, uuid
from django.db import models, transaction
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, Group
)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import validate_email
from django.core.exceptions import (
    ObjectDoesNotExist, ValidationError, PermissionDenied
)
from django.core.mail import send_mail
from backpocket.utils import validuuid, utcnow


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, password, commit=True, **extra_fields):
        """
        Create and save a user with the given username and password.
        """
        if not username:
            raise ValueError('The given username must be set')

        username = self.model.normalize_username(username)
        email = self.normalize_email(extra_fields.get('email', None))
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.full_clean()

        if commit:
            user.save(using=self._db)

        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_superuser') is True:
            raise ValueError('Normal user must have is_superuser=False.')

        # TODO: create default list(s)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):

    class Meta: 
        verbose_name = 'user'
        verbose_name_plural = 'users'
        default_related_name = 'users'
        db_table = 'bp_user'

        # Quite nonstandard permissions
        permissions = (
            ('view_user', 'Can view user'),
            ('view_admin', 'Can view admin interface'),
            ('set_user_admin', 'Can set user as admin'),
            ('set_user_active', 'Can activate/deactivate user'),
            ('set_user_password', 'Can set user password'),
            ('reset_user_password', 'Can reset user password'),
            ('change_user_groups', 'Can change user groups'),
        )

    class ObjectPermissions:
        # TODO: flesh out
        pass

    class ObjectPermissionFilters:
        # TODO: flesh out
        pass

    # UUIDv4 for long-term sanity
    id = models.UUIDField(
        'user ID', primary_key=True, default=uuid.uuid4, editable=False
    )
    username = models.CharField(
        'username',
        max_length=32,
        unique=True,
        validators=(UnicodeUsernameValidator,),
        help_text=(
            'Required. 32 characters or fewer. '
            'Letters, digits and @/./+/-/_ only.'
        ),
        error_messages={
            'unique': 'A user with that username already exists.',
        },
    )
    name = models.CharField('display name', max_length=150, blank=True)
    email = models.EmailField('email address', blank=True)
    date_joined = models.DateTimeField('date joined', default=utcnow)
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Designates whether this user should be treated as active.',
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    @property
    def is_staff(self):
        if self.is_superuser:
            return True
        # Check for admin permission, cache result
        if not hasattr(self, '_is_staff'):
            self._is_staff = self.has_perm('view_admin')
        return self._is_staff

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return self.name or self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        # TODO: check settings for SMTP config
        # send_mail(subject, message, from_email, [self.email], **kwargs)
        raise NotImplementedError
