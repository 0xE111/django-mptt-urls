from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ImproperlyConfigured
from mptt_urls import adv_import, make_superroot


def process_url(request, url, settings):
    slug_list = url.split('/')
    if slug_list[-1] == '':
        del slug_list[-1]  # Delete empty slug after last slash

    node_slug_field = settings['node'].get('slug_field', 'slug')
    leaf_slug_field = settings['leaf'].get('slug_field', 'slug')

    node_model = adv_import(settings['node']['model'])
    leaf_model = adv_import(settings['leaf']['model'])

    if slug_list == []:
        # Root
        object_type = 'node'
        object = make_superroot(node_model)
        object.is_superroot = lambda: True
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
                object.is_superroot = lambda: False
                object_type = 'node'
            except node_model.DoesNotExist:
                attrs = {
                    leaf_slug_field: slug,
                    'parent': parent,
                }
                object = get_object_or_404(leaf_model, **attrs)
                object.is_superroot = lambda: False
                object_type = 'leaf'

    template = settings[object_type].get('template', None)
    view = settings[object_type].get('view', None)

    if view and template:
        raise ImproperlyConfigured('"template" and "view" values cannot be used simultaneously in mptt_urls settings')
    elif view:
        view = adv_import(view)
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
