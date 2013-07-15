def mptt_urls_register(base_url, settings):
    def get_absolute_url_new(instance):
        url_list = []
        if isinstance(instance, settings['leaf_settings']['model']):
            # Model is leaf
            url_list.append(getattr(instance, settings['leaf_settings'].get('slug', 'slug')))
            instance = getattr(instance, settings['leaf_settings'].get('parent', 'parent'))
        while instance is not None:
            url_list.append(getattr(instance, settings['node_settings'].get('slug', 'slug')))
            instance = getattr(instance, settings['node_settings'].get('parent', 'parent'))

        return '/' + base_url + '/' + '/'.join(reversed(url_list)) + '/'

    settings['leaf_settings']['model'].get_absolute_url = get_absolute_url_new
    settings['node_settings']['model'].get_absolute_url = get_absolute_url_new
