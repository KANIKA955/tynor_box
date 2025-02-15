# Generated by Django 5.1.4 on 2024-12-20 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BoxDesign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('width', models.FloatField()),
                ('height', models.FloatField()),
                ('depth', models.FloatField()),
                ('material', models.CharField(max_length=50)),
                ('text', models.TextField()),
                ('logo', models.ImageField(upload_to='logos/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
