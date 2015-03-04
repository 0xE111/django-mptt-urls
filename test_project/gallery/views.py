# coding: utf-8
from django.shortcuts import render

from .models import Category


def category(request, path, instance, extra):
    # This is an example view.
    # As you can see, this view receives additional arg - instance.

    # Some logic here: we increase the number of category views (hits).
    # Instance will be None if not resolved
    if instance:
        instance.views += 1
        instance.save()

    return render(
        request,
        'gallery/category.html',
        {
            'instance': instance,
            'children': instance.get_children() if instance else Category.objects.root_nodes(),
            'extra': extra,
        }
    )
