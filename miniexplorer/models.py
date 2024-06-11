import uuid

from django.db import models
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from .utils import clean_mutable_commands, get_database_schema, raw_sql


class Query(models.Model):
    uuid = models.UUIDField(
        _("uuid"),
        editable=False,
        primary_key=True,
        unique=True,
        default=uuid.uuid4,
    )

    title = models.CharField(_("title"), max_length=50, unique=True)

    sql = models.TextField(_("SQL"))

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):
        self.sql = clean_mutable_commands(self.sql)
        super().save(*args, **kwargs)

    def execute(self):
        self.sql = clean_mutable_commands(self.sql)
        return raw_sql(self.sql)

    def schema(self):
        schema = get_database_schema()
        return render_to_string("schema_table.html", {"db_schema": schema})

    schema.short_description = _("Schema")

    class Meta:
        managed = True
        verbose_name = _("Query")
        verbose_name_plural = _("Queries")
        ordering = ["title"]
