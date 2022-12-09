from django.db import models
from django.contrib.auth.models import User

class Holder(models.Model):
    the_holder = models.TextField(blank=True)

    # def __str__(self):
    #     return self.the_holder


class Row(models.Model):
    the_row = models.ManyToManyField(Holder, blank=True)


class Table(models.Model):
    name = models.TextField(blank=True)
    header = models.ManyToManyField(Holder, blank=True,related_name='head')
    rows = models.ManyToManyField(Row, blank=True, related_name='row')
    row_head_name = models.TextField(blank=True)


class Report(models.Model):
    name = models.TextField(blank=True)
    tables = models.ManyToManyField(Table, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    type_of_report = models.TextField(blank=True)

    def __str__(self):
        return self.name