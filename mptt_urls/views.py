from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ImproperlyConfigured
from importlib import import_module


def import_view(path):
    modules = path.split('.')
    module = '.'.join(modules[0:-1])
    view = modules[-1]

    return getattr(import_module(module), view)


def translate_url(request, url, settings):
    url_list = url.split('/')
    del url_list[-1]  # Delete empty url after last slash

    node = None

    # 2do: DRY!
    for i, url in enumerate(url_list):
        if i != len(url_list) - 1:  # i is not last  # 2do: ugly!
            get_dict = {settings['node_settings'].get('slug', 'slug'): url}
            get_object_or_404(settings['node_settings']['model'], **get_dict)  # 2do: Suppress output?
        else:
            # Last url
            # 2do: DRY!
            try:
                get_dict = {settings['node_settings'].get('slug', 'slug'): url}
                node = settings['node_settings']['model'].objects.get(**get_dict)
                is_leaf = False
            except:
                get_dict = {settings['leaf_settings'].get('slug', 'slug'): url}
                node = get_object_or_404(settings['leaf_settings']['model'], **get_dict)
                is_leaf = True

    if is_leaf:
        which_settings = 'leaf_settings'
    else:
        which_settings = 'node_settings'

    template = settings[which_settings].get('template', None)
    view = settings[which_settings].get('view', None)

    if template:
        return render(
            request,
            template,
            {
                'mptt_urls': {
                    'node': node,
                }
            }
        )
    elif view:
        if isinstance(view, basestring):
            view = import_view(view)

        return view(
            request,
            mptt_urls={
                'node': node,
            }
        )
    else:
        raise ImproperlyConfigured('Cannot find `template` or `view` value in mptt_urls settings')
