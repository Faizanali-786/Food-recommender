# Generated by Django 3.2.7 on 2022-02-25 17:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='foodapp.signup'),
            preserve_default=False,
        ),
    ]
