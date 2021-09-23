from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.html import mark_safe

from .models import Query

@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):

    search_fields = ("title", "uuid")
    list_display = ("title", "get_result")

    fieldsets = (
        (None, {
            "fields": (
                ("title", ),
                ("sql", ),
            ),
        }),
        ('Data Base Schema', {
            'classes': ('collapse',),
            'fields': ("schema",),
        }),
    )
    readonly_fields = ('schema', )

    change_form_template = "admin/miniexplorer/query/change_form.html"

    def get_result(self, obj):
        results = obj.execute()
        number_of_rows = len(results)
        if number_of_rows == 1:
            number_of_cols = len(results[0]._fields)
            if number_of_cols == 1:
                return mark_safe(f'<strong>{results[0][0]}</strong>')
            else:
                return mark_safe("")
        return mark_safe('')
    get_result.short_description = 'Result'

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
        css = {"all": (
            "https://cdn.jsdelivr.net/npm/codemirror@5.59.2/lib/codemirror.min.css",
            "miniexplorer.css",
        )}
        js = (
            "https://cdn.jsdelivr.net/npm/codemirror@5.59.2/lib/codemirror.min.js",
            "https://cdn.jsdelivr.net/npm/codemirror@5.59.2/mode/sql/sql.min.js",
            "https://codemirror.net/addon/display/panel.js",
            "https://unpkg.com/sql-formatter@4.0.2/dist/sql-formatter.min.js",
            "miniexplorer.js",
        )
