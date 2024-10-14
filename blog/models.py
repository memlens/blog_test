from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'utilisateur doit avoir une adresse email")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:

        verbose_name_plural = "categories"


    def __str__(self):

        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)

    body = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True)

    last_modified = models.DateTimeField(auto_now=True)

    categories = models.ManyToManyField("Category", related_name="posts")

    def __str__(self):

        return self.title



class Comment(models.Model):

    author = models.CharField(max_length=60)

    body = models.TextField()

    created_on = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):

        return f"{self.author} on '{self.post}'"