# Generated by Django 4.1.3 on 2022-11-24 18:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_report_created_by_report_type_of_report_row_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='report',
            name='header',
        ),
        migrations.RemoveField(
            model_name='report',
            name='rows',
        ),
        migrations.RemoveField(
            model_name='report',
            name='type_of_report',
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True)),
                ('type_of_report', models.TextField(blank=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('header', models.ManyToManyField(blank=True, related_name='head', to='app.holder')),
                ('rows', models.ManyToManyField(blank=True, related_name='row', to='app.row')),
            ],
        ),
        migrations.AddField(
            model_name='report',
            name='tables',
            field=models.ManyToManyField(blank=True, to='app.table'),
        ),
    ]
