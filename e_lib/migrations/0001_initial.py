# Generated by Django 4.2.4 on 2023-08-23 08:17

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='book',
            fields=[
                ('books_Name', models.CharField(max_length=120, verbose_name='Name')),
                ('books_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='book_id')),
                ('book_pdf', models.FileField(upload_to='pdfs/', verbose_name='book_pdf')),
                ('book_img', models.ImageField(upload_to='imgs/', verbose_name='book_img')),
            ],
        ),
        migrations.CreateModel(
            name='department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=120, verbose_name='Name')),
            ],
        ),
        migrations.CreateModel(
            name='myuser',
            fields=[
                ('first_name', models.CharField(max_length=120, verbose_name='Name')),
                ('last_name', models.CharField(max_length=120, verbose_name='Name')),
                ('roll_no', models.IntegerField(verbose_name='roll no.')),
                ('phone_no', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Phone No.')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('username', models.CharField(max_length=120, primary_key=True, serialize=False, verbose_name='username')),
                ('user_type', models.CharField(max_length=10, null=True, verbose_name='user_type')),
            ],
        ),
        migrations.CreateModel(
            name='subject',
            fields=[
                ('subject_Name', models.CharField(max_length=120, verbose_name='Name')),
                ('subject_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='subject_id')),
            ],
        ),
        migrations.CreateModel(
            name='teacher',
            fields=[
                ('teacher_Name', models.CharField(max_length=120, verbose_name='Name')),
                ('teacher_emp_id', models.IntegerField(primary_key=True, serialize=False, verbose_name='emp_id')),
                ('teacher_phone_no', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Phone No.')),
                ('teacher_email', models.EmailField(max_length=254, verbose_name='email')),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('Name', models.CharField(max_length=120, verbose_name='Name')),
                ('reg_no', models.IntegerField(primary_key=True, serialize=False, verbose_name='roll no.')),
                ('phone_no', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Phone No.')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='e_lib.department')),
                ('read_books', models.ManyToManyField(blank=True, to='e_lib.book')),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='e_lib.subject'),
        ),
    ]
