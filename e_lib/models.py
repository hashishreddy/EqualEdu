# models.py in e_lib app
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from members.models import CustomUser  
from django.contrib.auth import get_user_model

class Department(models.Model):
    name = models.CharField('Name', max_length=120)

    def __str__(self):
        return self.name

class Subject(models.Model):
    subject_name = models.CharField('Name', max_length=120)
    subject_id = models.AutoField(primary_key=True)

    def __str__(self):
        return self.subject_name

User = get_user_model()

class Book(models.Model):
    books_name = models.CharField('Name', max_length=120)
    books_id = models.AutoField(primary_key=True)
    subject = models.ForeignKey(Subject, blank=True, null=True, on_delete=models.CASCADE)
    book_pdf = models.FileField(("book_pdf"), upload_to='pdfs/') 
    book_img = models.ImageField(("book_img"), upload_to='imgs/')
    author = models.CharField('author', max_length=120, null=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    added_at = models.DateTimeField(auto_now_add=True,null=True)

    # users_opened = models.ManyToManyField(User, related_name='opened_books', blank=True)

    def __str__(self):
        return self.books_name

    def save(self, *args, **kwargs):
        if not self.added_by_id:
            self.added_by = kwargs.pop('user', None)
        super().save(*args, **kwargs)

class ViewedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

class Video(models.Model):
    title = models.CharField(max_length=120)
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/')
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    added_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title
    




