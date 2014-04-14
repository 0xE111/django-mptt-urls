# coding: utf-8

from importlib import import_module

from django.utils.module_loading import import_by_path
from django.conf.urls import url
from django.core.urlresolvers import reverse


def url_mptt(url_string, name, settings):
    '''
    This wrapper creates and returns a usual url() object, and additionally sets get_absolute_url() methods for all models mentioned in settings
    '''

    leaf_model = import_by_path(settings['leaf']['model'])
    node_model = import_by_path(settings['node']['model'])

    # ---- Set up get_absolute_url() for nodes and leaves ----
    def get_absolute_url(instance):
        slug_list = []
        if isinstance(instance, leaf_model):
            # Model is leaf
            slug_list.append(getattr(instance, settings['leaf'].get('slug_field', 'slug')))
            instance = getattr(instance, settings['leaf'].get('parent', 'parent'))
        while instance is not None:
            slug_list.append(getattr(instance, settings['node'].get('slug_field', 'slug')))
            instance = getattr(instance, settings['node'].get('parent', 'parent'))

        return reverse(name, kwargs={'url': '/'.join(reversed(slug_list))})

    leaf_model.get_absolute_url = get_absolute_url
    node_model.get_absolute_url = get_absolute_url

    return url(url_string, 'mptt_urls.views.process_url', {'settings': settings}, name=name)


def superroot(model):
    # Create a superroot instance with fake mptt methods from model
    instance = model()  # Create instance of the model

    instance.save = lambda: instance  # Preserve fake instance from saving
    instance.delete = lambda: None

    instance.get_ancestors = lambda ascending, include_self: []
    instance.get_children = lambda: model.objects.root_nodes()  # Main usage
    instance.get_descendants = lambda include_self: []
    instance.get_descendant_count = lambda: 0
    instance.get_next_sibling = lambda: None
    instance.get_previous_sibling = lambda: None
    instance.get_root = lambda: None
    instance.get_siblings = lambda include_self: []
    instance.insert_at = lambda target, position, save: None
    instance.is_child_node = lambda: False
    instance.is_leaf_node = lambda: False
    instance.is_root_node = lambda: False
    instance.move_to = lambda target, position: None

    return instance