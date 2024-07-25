from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, login, first_name, last_name, phone, id_region, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not login:
            raise ValueError('Users must have a login')

        user = self.model(
            email=self.normalize_email(email),
            login=login,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            id_region=id_region,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, login, first_name, last_name, phone, id_region, password=None):
        user = self.create_user(
            email,
            password=password,
            login=login,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            id_region=id_region,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    login = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    id_region = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone', 'id_region']

    def __str__(self):
        return self.login

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
class ProductType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type

class Product(models.Model):
    item_code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField()
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name