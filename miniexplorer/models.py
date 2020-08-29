import uuid

from django.db import models

from .utils import raw_sql

class Query(models.Model):

    uuid = models.UUIDField(
        "uuid", 
        editable=False,
        primary_key=True,
        unique=True, 
        default=uuid.uuid4, 
    )

    title = models.CharField(
        "title", 
        max_length=50,
        unique=True
    )

    sql = models.TextField(
        "SQL"
    )

    def __str__(self):
        return f'{self.title}'

    def execute(self):
        print(f'Running: {self.sql}')
        return raw_sql(self.sql)

    class Meta:
        managed = True
        verbose_name = 'Query'
        verbose_name_plural = 'Queries'
