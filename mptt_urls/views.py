# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_by_path

from mptt_urls import superroot


def process_url(request, url, settings):
    slug_list = url.split('/')
    if slug_list[-1] == '':
        del slug_list[-1]  # Delete empty slug after last slash

    node_slug_field = settings['node'].get('slug_field', 'slug')
    leaf_slug_field = settings['leaf'].get('slug_field', 'slug')

    node_model = import_by_path(settings['node']['model'])
    leaf_model = import_by_path(settings['leaf']['model'])

    if slug_list == []:
        # Root
        object_type = 'node'
        object = superroot(node_model)
    else:
        parent = None
        for slug in slug_list[:-1]:
            attrs = {
                node_slug_field: slug,
                'parent': parent,
            }
            object = get_object_or_404(node_model, **attrs)
            parent = object
        else:
            # Last slug
            slug = slug_list[-1]
            try:
                attrs = {
                    node_slug_field: slug,
                    'parent': parent,
                }
                object = node_model.objects.get(**attrs)
                object_type = 'node'
            except node_model.DoesNotExist:
                attrs = {
                    leaf_slug_field: slug,
                    'parent': parent,
                }
                object = get_object_or_404(leaf_model, **attrs)
                object_type = 'leaf'
            object.is_superroot = lambda: False

    template = settings[object_type].get('template', None)
    view = settings[object_type].get('view', None)

    if view and template:
        raise ImproperlyConfigured('"template" and "view" values cannot be used simultaneously in mptt_urls settings')
    elif view:
        view = import_by_path(view)
        if hasattr(view, 'as_view'):
            view = view.as_view()
        return view(
            request,
            mptt_urls={
                'object': object,
            },
        )
    elif template:
        return render(
            request,
            template,
            {
                'mptt_urls': {
                    'object': object,
                }
            }
        )
    else:
        raise ImproperlyConfigured('Cannot find "template" or "view" value in mptt_urls settings')
