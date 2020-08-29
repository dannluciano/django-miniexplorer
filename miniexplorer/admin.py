from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import Query


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):

    search_fields = ("title", "uuid")
    list_display = ("title", "sql")

    change_form_template = "admin/miniexplorer/query/change_form.html"

    def change_view(self, request, object_id, form_url="", extra_context=None):
        extra_context = extra_context or {}
        query = get_object_or_404(Query, pk=object_id)

        time = timezone.now()
        results = query.execute()
        fields = results[0]._fields or []

        extra_context["results"] = results
        extra_context["fields"] = fields
        extra_context["last_time"] = time

        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context=extra_context,
        )

    class Media:
        css = {"all": ("codemirror/lib/codemirror.css",)}
        js = (
            "codemirror/lib/codemirror.js",
            "codemirror/mode/sql/sql.js",
            "miniexplorer.js",
        )
