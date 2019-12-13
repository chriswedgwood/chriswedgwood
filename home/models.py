from __future__ import unicode_literals

from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from blog.models import BlogPage, BlogCategory


class HomePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full"),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super(HomePage, self).get_context(request)
        #.values('person_id', 'display_name')
        category_counts = BlogCategory.objects.values('name').annotate(category_cnt=models.Count("blogpage"))
        context['category_counts'] = category_counts
        return context