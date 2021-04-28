from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager

# =======================================================
class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, last_name, first_name, password=None):
        if not email:
            raise ValueError('User must have an email address.')

        if not username:
            raise ValueError('User must have an username.')

        if not last_name:
            raise ValueError('User must have an last_name.')

        if not first_name:
            raise ValueError('User must have an first_name.')

        user = self.model(email=self.normalize_email(email),
                          username=username,
                          last_name=last_name,
                          first_name=first_name,
                         )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, last_name, first_name, password=None):
        if not email:
            raise ValueError('User must have an email address.')

        if not username:
            raise ValueError('User must have an username.')

        if not last_name:
            raise ValueError('User must have an last_name.')

        if not first_name:
            raise ValueError('User must have an first_name.')

        user = self.create_user(email=self.normalize_email(email),
                                username=username,
                                last_name=last_name,
                                first_name=first_name,
                                password=password,
                               )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user

# =======================================================
class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    last_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    # ... identity and contact
    identity_number = models.CharField(max_length=15, blank=True, null=True)
    identity_number = models.CharField(max_length=15, blank=True, null=True)
    tel = models.CharField(max_length=30, blank=True, null=True)
    address_home = models.CharField(max_length=30, blank=True, null=True)
    address_city = models.CharField(max_length=30, blank=True, null=True)
    address_postal_code = models.CharField(max_length=30, blank=True, null=True)
    address_country = models.CharField(max_length=30, blank=True, null=True)
    # ...

    # ... Professor case
    profile = models.CharField(max_length=30)
    grad = models.CharField(max_length=30)
    expertize = models.CharField(max_length=30)
    university = models.CharField(max_length=30)
    departement = models.CharField(max_length=30)
    # ...   
     
    # ...
    # TODO add Uploaded documents part
    # CV
    # Diplomas
    # Contract
    # Justificatif du grade
    # autorisation de l'etablissement
    # fiche d'engagement    
    # ...

    # ... flags
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) # TODO must be False until validation by admin
    is_staff = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # ...
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'last_name', 'first_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
