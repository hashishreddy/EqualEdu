from django.contrib import admin


from .models import Subject
from .models import Book
from .models import Department
from .models import Video



admin.site.register(Subject)
admin.site.register(Book)
admin.site.register(Department)
admin.site.register(Video)