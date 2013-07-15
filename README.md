Overview
--------

This reusable app helps to create arbitrary-depth [Clean URLs](http://en.wikipedia.org/wiki/Clean_URL) which correspond to MPTT tree hierarchy of model instances, like these:

`http://best-photographer.com/gallery/weddings/Dexter-and-Rita/photo-1`
`http://best-photographer.com/gallery/my-pets/dogs/husky/Mishka`

As you can see, the links are quite different - they have different depth of hierarchy. When users see these URLs they can easily discover where they are located. They can either delete some part of the URL and thus move up in the hierarchy.

Each URL leads either to a view or to a template (you can choose).

How it works
------------

Django-mptt-urls is an intermediator between URLs and views.
In standard django app usual url resolution looks like:

`URL: /gallery/photos/` ---> `VIEW: gallery.views.photos`

With django-mptt-urls it looks like:

`URL: /gallery/my-pets/dogs/` ---> `MPTT_URLS: select view` --arg--> `VIEW: gallery.views.photo`

or

`URL: /gallery/my-pets/dogs/` ---> `MPTT_URLS: select template` --arg--> `TEMPLATE: gallery/photo.html`

Mptt_urls does these things:
* Checks URL for being valid (or Http404)
* Selects corresponding view/template
* Passes extra argument to the view/template: mptt_urls={'node': node, 'leaf': leaf}

Requirements
------------

django-mptt-urls app is strongly tied to [django-mptt](https://github.com/django-mptt/django-mptt). So be sure you have installed it:

`pip install django-mptt`

Your models should use mptt models, for example for gallery:

```
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    ...
    parent = TreeForeignKey('self', ...)

class Photo(models.Model):
    ...
    parent = TreeForeignKey(Category, ...)
```

Here gallery consists of Categories, and leaf Categories are containers for Photos. We will continue using our gallery example in the next sections.


Installation
------------

Since django-mptt-urls is not added to PyPI, install it manually:
```
git clone https://github.com/MrKesn/django-mptt-urls.git
cd django-mptt-urls
python setup.py install
```

Add mptt_urls in your `INSTALLED_APPS`:

```
# settings.py

INSTALLED_APPS = (
    ...
    'mptt_urls',
)
```

Select the *base URL* where the hierarchy URLs will be located. In these URLs the *base URL* is `gallery/`:

`http://best-photographer.com/gallery/weddings/Dexter-and-Rita/photo-1`
`http://best-photographer.com/gallery/miscellaneous/my-pets/dogs/husky/Mishka`

Then, in your `urls.py`, 
* import `mptt_urls_register`
* add a variable `mptt_urls_gallery_settings` containing gallery settings, 
* call `mptt_urls_register`,
* include `mptt.urls` :

```
# urls.py
...
from mptt_urls import mptt_urls_register

mptt_urls_gallery_settings = {
    'node_settings': {
        'model': Category,
        'view': 'gallery.views.category',
        'parent': 'parent',
        'slug': 'slug',
    },
    'leaf_settings': {
        'model': Photo,
        'template': 'gallery/photo.html',
        'parent': 'parent',
        'slug': 'slug',
    }
}

mptt_urls_register('gallery', mptt_urls_gallery_settings)

urlpatterns = patterns('',
    ...
    url(r'^gallery/', include('mptt_urls.urls'), {'settings': mptt_urls_gallery_settings}),
    ...
)
```

Here is what we've done:

1) We are storing our gallery settings in `mptt_urls_gallery_settings` variable. It has settings for nodes and leaves, the fields are:
* `model`: Which model to use. As we've defined in `Requirements` section, nodes are Categories instances, leaves are Photos instances.
* `view`: A view which will be called. Mptt_urls provides an argument `mptt_urls` (python dictionary) to the view, so be sure to accept this arg in a view (`def someview(request, mptt_urls=None)`). `view` can be either a view or a string like `'gallery.views.someview'`.
* `template`: If you do not need a view, you can redirect mptt_urls output directly to a template. The rule is: if you need only the object associated with the URL, use `template`; if you need some extra logic/calculations, use `view`.
* `parent`: Name of 'parent' field (foreign key field to parent(ancestor) of the model).
* `slug`: Name of 'slug' field. The field's value will be taken for constructing and resolving URLs.

2) we call `mptt_urls_register`, which hooks into models' classes (Category and Photo here) and defines `get_absolute_url` methods. First arg is *base URL*, second arg contains our settings.

3) We include `mptt_urls.urls` in `url(r'^gallery/', ...)`. That means that **every URL starting with /gallery/ will be caught by mptt_urls** and treated as hierarchical path. Be careful with it, especially when you do `url(r^/', include('mptt_urls.urls'), ...)`.

