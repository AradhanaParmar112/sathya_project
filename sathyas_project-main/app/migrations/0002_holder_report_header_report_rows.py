# Generated by Django 4.1.3 on 2022-11-24 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Holder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('the_holder', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='header',
            field=models.ManyToManyField(blank=True, related_name='head', to='app.holder'),
        ),
        migrations.AddField(
            model_name='report',
            name='rows',
            field=models.ManyToManyField(blank=True, related_name='row', to='app.holder'),
        ),
    ]
