# Generated by Django 5.1.6 on 2025-05-01 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0011_gonullusorunfotograf'),
    ]

    operations = [
        migrations.AddField(
            model_name='gonulludurumveriler',
            name='aciklama',
            field=models.TextField(blank=True, null=True, verbose_name='Açıklama'),
        ),
    ]
