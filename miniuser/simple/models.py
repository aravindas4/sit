
import sys

from django.db import models, transaction
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

from simple import tasks as simple_tasks


class Base(models.Model):
    created_on = models.DateField(auto_now_add=True)
    modified_on = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):

    def _create_user(self, username, password, email, **extra_fields):
        if not username or not email:
            raise ValueError("The given username and email must be set")
        try:
            with transaction.atomic():
                user = self.model(username=username, email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except Exception as e:
            raise print("error_details: %s - %s".format(e, sys.exc_info()[0]))

    def create_user(self, username, password, email, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, email, **extra_fields)

    def create_superuser(self, username, password, email, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, password, email, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=30, default="ash.g.proxy@gmail.com")
    username = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    password = models.CharField(max_length=10000)
    access_token = models.CharField(max_length=100, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        super(MyUser, self).save(*args, **kwargs)


class Issue(Base):
    STATUS_CHOICE = (
        ('C', 'Closed'),
        ('O', 'Open'),
    )
    title = models.CharField(max_length=15)
    description = models.TextField()
    assigned_to = models.ForeignKey(MyUser, on_delete=models.SET_NULL, related_name="assigned_issues", null=True)
    created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name="created_issues")
    status = models.CharField(max_length=7, choices=STATUS_CHOICE, default=STATUS_CHOICE[0][0])

    def __str__(self):
        return self.title


@receiver(post_save, sender=Issue)
def issue_notifier(sender, instance, created, **kwargs):
    if created:
        message = "assigned for you"
    else:
        message = "has update"
    simple_tasks.issue_notifier(instance, message)

    return None

