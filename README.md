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

`URL: /gallery/my-pets/dogs/` ---> `MPTT_URLS: select view` --mptt_urls['object']--> `VIEW: gallery.views.photo`

or

`URL: /gallery/my-pets/dogs/` ---> `MPTT_URLS: select template` --mptt_urls.object--> `TEMPLATE: gallery/photo.html`

Mptt_urls does these things:
* Checks URL for being valid (or Http404)
* Selects corresponding view/template
* Passes extra argument to the view/template: mptt_urls['object']


Example
-------

The simpliest way to understand how django_mptt_urls works is to clone this GitHub project and to run test_project (no extra settings required):
```
git clone https://github.com/MrKesn/django-mptt-urls.git
cd django-mptt-urls
python setup.py install
cd test_project
python manage.py runserver
```

And point your browser to 127.0.0.1:8000

Requirements
------------

django-mptt-urls app is strongly tied to [django-mptt](https://github.com/django-mptt/django-mptt). So be sure you have installed it:

`pip install django-mptt`

Your models should use mptt models, for example for gallery:

```
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    ...
    parent = TreeForeignKey('self', null=True, blank=True, verbose_name='parent category', related_name='categories')
    slug = models.SlugField()
    class Meta:
        unique_together = ('slug', 'parent')

class Photo(models.Model):
    ...
    parent = TreeForeignKey(Category, verbose_name='parent category', related_name='photos')
    slug = models.SlugField()

    class Meta:
        unique_together = ('slug', 'parent')
```

Here gallery consists of Categories, and leaf Categories are containers for Photos. We will continue using our gallery example in next sections.


Installation
------------

You can use pip:
```
pip install django-mptt-urls
```

Or, if you want an exaple project being included (test_project), clone the GitHub repo:
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

Then, in your `urls.py`, 
* import: `from mptt_urls import url_mptt`
* add a variable `mptt_urls_gallery_settings` containing gallery settings,
* add url `url_mptt` :

```
# urls.py
...
from mptt_urls import url_mptt

mptt_urls_gallery_settings = {
    'node': {
        'model': 'gallery.models.Category',
        'view': 'gallery.views.category',
        'slug_field': 'slug',
    },
    'leaf': {
        'model': 'gallery.models.Photo',
        'template': 'gallery/photo.html',
        'slug_field': 'slug',
    }
}

urlpatterns = patterns('',
    ...
    url_mptt(r'^gallery/(?P<url>.*)', name='gallery', settings=mptt_urls_gallery_settings),
    ...
)
```

Here is what we've done:
* We are storing our gallery settings in `mptt_urls_gallery_settings` variable. It has settings for nodes and leaves, the fields are:
* ** `model`: Which model to use. As we've defined in `Requirements` section, nodes are Categories instances, leaves are Photos instances.
* ** `view`: A view which will be called. Mptt_urls provides an argument `mptt_urls` to the view, so be sure to accept this arg in a view (`def someview(request, mptt_urls=None)`). `view` should be a string like `'gallery.views.someview'`.
* ** `template`: If you do not need a view, you can redirect mptt_urls output directly to a template. The rule is: if you need some extra logic/calculations in your view, use `view`; otherwise use `template`.
* ** `slug_field`: Name of 'slug' field. The field's value will be taken for constructing and resolving URLs. It's up to you to generate slug for model instances! (Use `prepopulate_fields` in admin, or django-autoslug, etc.)
* We set up new url catcher: url_mptt(...). 1st arg is usual url regexp. Do not forget to catch `(?P<url>.*)` pattern. 2nd arg is url name, so thet you can use `reverse(name, kwargs={'url': ''})` in your code. 3rd arg contains settings. Note that **url_mptt does not accept `view` variable**.
* Note that **every URL starting with /gallery/ will be caught by mptt_urls** and treated as hierarchical path. Be careful with it.

Usage
-----

Now, when everything is set up, it's time to use mptt_urls.
The views you specified in the settings (`'gallery.views.category'` in example) will get `mptt_urls` arg, containing `object` - instance of a model, corresponding to the url. Just like this:
```
# gallery.views.category
def category(request, mptt_urls):
    # Here extra logic is: we increase the number of category views
    object = mptt_urls['object']
    if not object is None:
        object.views += 1
        object.save()

    return render(
        request,
        'gallery/category.html',
        {
            'mptt_urls': mptt_urls,
        }
    )
```

The templates will get the same arg `mptt_urls` containing `object`, like this:
```
# gallery/photo.html
<html>
    <body>
        {{ mptt_urls.object }}
    </body>
</html>
```

Feel free to use `get_absolute_url()` method for hierarchical objects - it will return correct hierarchical urls.

To get the root, use `reverse('gallery', kwargs={'url': ''})` (in view) or `{% url 'gallery' url='' %}` (in templates.

The SuperRoot
-------------

To simplify developer's life and to follow KISS, django_mptt_urls *always* passes and arg `object` to a view/template. There are 3 types of instances which an `object` can be:
* leaf - A leaf object, the end point of path. In the example, a leaf is a Photo instance.
* node - Nodes which actually create the hierarchy. In the example, a node is a Category instance.
* superroot - A fake node which is parent to all real root nodes (root node is such a node that node.parent == None). You will find superroot helpful when you process base path (/gallery/). When you visit /gallery/ url, there is actually no object associated with the path, and you probably would like to simply show all root nodes to the user. So, mptt_urls['object'] here is a superroot, and it has 1 working method: get_children(), which will return all root nodes. Introducing superroot allows you to write only one view/template for both root and non-root urls. Oh, just check `test_project` for clear example.

`mptt_urls['object'].is_superroot()` will help you to discover if the object is superroot.

License
-------
MIT.
View license file for details.

P.S.
----
Please feel free to make pull requests! :)

