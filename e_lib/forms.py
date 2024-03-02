from django import forms
from django.forms import ModelForm
from .models import Book
from .models import Video



class BookForm(ModelForm):
    class Meta:
        model = Book 
        exclude = ('added_by','book_img',)



class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'video_file', 'thumbnail']

    def save(self, commit=True, user=None):
        instance = super(VideoForm, self).save(commit=False)
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance
         