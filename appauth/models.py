import secrets
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.timezone import now
from django.core.files import File
import qrcode
from PIL import Image, ImageDraw
from io import BytesIO


class UserManager(BaseUserManager):
    def create_user(self, email, reg_no, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            reg_no=reg_no,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, reg_no, email, first_name, last_name, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            reg_no=reg_no,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, reg_no, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            reg_no= reg_no,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


# 
class User(AbstractBaseUser):
    objects = UserManager()
    email = models.EmailField(verbose_name='email address', max_length=255,unique=True)
    reg_no = models.CharField(unique=True, max_length=255, blank=False, default='', verbose_name='reg_no')
    first_name = models.CharField(max_length=255, blank=False, default='', verbose_name='first name')
    last_name = models.CharField(max_length=255, blank=False, default='', verbose_name='last name')
    created = models.DateTimeField(default=now)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'reg_no'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def get_full_name(self):
        # The user is identified by their first & last name
        full_name = '%s %s'%(self.first_name, self.last_name)
        return full_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.last_name

    def __str__(self):  # __unicode__ on Python 2
        full_name = '%s %s'%(self.first_name, self.last_name)
        return str(full_name)

    def has_perms(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.staff

    @property
    def is_admin(self):
        """Is the user a admin member?"""
        return self.admin

    @property
    def is_active(self):
        """Is the user active?"""
        return self.active

class Faculty(models.Model):
    faculty_name = models.CharField(max_length=255, blank=False, default='', verbose_name='faculty')

    def __str__(self):
        return str(self.faculty_name)

class UserBio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    tel = models.CharField(default='', null=True, blank=True, max_length=11)
    department = models.CharField(max_length=255, blank=False, default='', verbose_name='department')
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    code = models.CharField(default='', blank=True, max_length=9)
    qrcode = models.ImageField(upload_to='user_QRC_auth/', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        qrcode_image = qrcode.make(f"{self.user}")
        canvas = Image.new('RGB', (350, 350), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_image)
        fname = f"{'%s%s%s' % (f'{self.user.first_name}_{self.user.last_name}_', '-', self.code)}.png"
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qrcode.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)
