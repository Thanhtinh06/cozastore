# Generated by Django 4.0.5 on 2022-09-23 16:24

import ckeditor_uploader.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('image', models.ImageField(default='dashmain/images/default.png', upload_to='dashmain/images')),
                ('price_sell', models.FloatField()),
                ('price_buy', models.FloatField()),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('inventory', models.IntegerField()),
                ('public_day', models.DateTimeField(default=datetime.datetime.now)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.category')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='store.status')),
            ],
        ),
    ]
