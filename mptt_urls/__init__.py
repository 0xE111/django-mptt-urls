from importlib import import_module


def adv_import(obj):
    if isinstance(obj, basestring): 
        modules = obj.split('.')
        module = '.'.join(modules[0:-1])
        view = modules[-1]

        return getattr(import_module(module), view)
    else:
        return view


def register(base_url, settings):
    def get_absolute_url(instance):
        slug_list = []
        if isinstance(instance, adv_import(settings['leaf']['model'])):
            # Model is leaf
            slug_list.append(getattr(instance, settings['leaf'].get('slug_field', 'slug')))
            instance = getattr(instance, settings['leaf'].get('parent', 'parent'))
        while instance is not None:
            slug_list.append(getattr(instance, settings['node'].get('slug_field', 'slug')))
            instance = getattr(instance, settings['node'].get('parent', 'parent'))

        return '/' + base_url + '/' + '/'.join(reversed(slug_list)) + '/'

    leaf_model = adv_import(settings['leaf']['model'])
    node_model = adv_import(settings['node']['model'])

    leaf_model.get_absolute_url = get_absolute_url
    node_model.get_absolute_url = get_absolute_url


def make_superroot(model):
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