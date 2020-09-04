# Generated by Django 3.0.4 on 2020-09-02 10:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_comment_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeatureVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('source', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
