import json
from django.contrib import admin
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.html import mark_safe
from django.utils.translation import get_language
from django.http import JsonResponse
from django.urls import path, reverse
from django.utils.translation import gettext as _

from .models import Query


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):

    search_fields = ("title", "uuid")
    list_display = ("title", "get_result")

    fieldsets = (
        (
            None,
            {
                "fields": (("title",),),
            },
        ),
        (
            "Data Base Schema",
            {
                "classes": ("collapse",),
                "fields": ("schema",),
            },
        ),
        (
            None,
            {
                "fields": (("sql",),),
            },
        ),
    )
    readonly_fields = ("schema",)

    change_form_template = "admin/miniexplorer/query/change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        execute_url = [
            path(
                "execute/",
                self.execute_sql_view,
                name="execute_sql",
            ),
        ]
        return execute_url + urls

    def get_result(self, obj):
        results = obj.execute()
        number_of_rows = len(results)
        if number_of_rows == 1:
            number_of_cols = len(results[0]._fields)
            if number_of_cols == 1:
                return mark_safe(f"<strong>{results[0][0]}</strong>")
            else:
                return mark_safe("")
        return mark_safe("")

    get_result.short_description = _("Result")

    def execute_sql_view(self, request):
        try:
            data = json.loads(request.body)
            context = {}
            query = Query()
            query.sql = data["sql"]

            time = timezone.now()
            results = query.execute()
            delta_time = timezone.now() - time

            fields = results[0]._fields or []

            context["results"] = results
            context["fields"] = fields
            context["last_time"] = time
            context["delta_time"] = delta_time.total_seconds()
            context["current_language"] = get_language()

            return JsonResponse(context)

        except json.JSONDecodeError as e:
            return JsonResponse(
                {
                    "error": "JSONDecodeError:",
                    "msg": "Invalid JSON Payload",
                }
            )
        except TypeError as e:
            return JsonResponse(
                {
                    "error": "TypeError:",
                    "msg": "SQL type error",
                }
            )
        except Exception as e:
            return JsonResponse(
                {
                    "error": str(e.__class__),
                    "msg": str(e),
                }
            )

    class Media:
        css = {
            "all": (
                "https://cdn.jsdelivr.net/npm/codemirror@5.59.2/lib/codemirror.min.css",
                "miniexplorer.css",
            )
        }
        js = (
            "https://cdn.jsdelivr.net/npm/codemirror@5.59.2/lib/codemirror.min.js",
            "https://cdn.jsdelivr.net/npm/codemirror@5.59.2/mode/sql/sql.min.js",
            "https://codemirror.net/addon/display/panel.js",
            "https://unpkg.com/sql-formatter@4.0.2/dist/sql-formatter.min.js",
            "miniexplorer.js",
        )
