Overview
--------

This reusable app helps to create arbitrary-depth [Clean URLs](http://en.wikipedia.org/wiki/Clean_URL) which correspond to MPTT tree hierarchy of model instances, like these:

`http://best-photographer.com/gallery/weddings/Dexter-and-Rita/`

`http://best-photographer.com/gallery/my-pets/dogs/husky/`

As you can see, the links are quite different - they have different depth of hierarchy. When users see these URLs they can easily discover where they are located. They can either delete some part of the URL and thus move up in the hierarchy.

Django-mptt-urls is just a simple view that knows how to resolve hierarchical urls.

Example
-------

The simpliest way to understand how django_mptt_urls works is to clone this GitHub project, create virtual environment and run test_project (no extra settings required, except sqlite3 database support):
```
git clone https://github.com/c0ntribut0r/django-mptt-urls.git
pyvenv django-mptt-urls
source django-mptt-urls/bin/activate
pip install django-mptt-urls/
python django-mptt-urls/test_project/manage.py runserver
```

And visit 127.0.0.1:8000 in your browser.

Requirements
------------

Developed using django 1.7, python 3.4.3, other versions may work too. If python 2 support required, just fork and patch, there are only few lines of code there.

django-mptt-urls uses [django-mptt](https://github.com/django-mptt/django-mptt). It will be automatically installed as a requirement.

Installation
------------

First of all, you should already be using django-mptt, something like this:

```
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    ...
    parent = TreeForeignKey('self', null=True, blank=True)
    slug = models.SlugField()
    class Meta:
        unique_together = ('slug', 'parent')
```

Install django-mptt-urls:

```
pip install django-mptt-urls
```

Then, in your `urls.py`, replace one or more views with special `mptt_urls.view`:

```
# urls.py
...
import mptt_urls

urlpatterns = patterns('',
    ...
    url(r'^gallery/(?P<path>.*)', mptt_urls.view(model='gallery.models.Category', view='gallery.views.category', slug_field='slug'), {'extra': 'You may also pass extra options as usual!'}, name='gallery'),
    ...
)
```

Here is what we've done:
* We are capturing `(?P<path>.*)`, which will be passed to `mptt_urls.view` when url resolution is fired. You can define `path` whatever you like (for example `(?P<path>[\d/]+)`), but **don't forget to include '/' in the regex**.
* Replace your view with special `mptt_urls.view`.

`mptt-urls.view` works like a decorator to a view: it gets fired when url resolution is performed, calculates an instance the `path` is poining to, and passes it to original view.

So, if you write
```
url(r'^gallery/(?P<path>.*)', 'gallery.views.category', name='gallery'),
```
the `gallery.views.category` view will receive `path` variable and will have to make object resolution.
With `mptt_urls.view`, you will get the resolved object automatically - `gallery.views.category` view will receive `path` and `instance` variables:
```
url(r'^gallery/(?P<path>.*)', mptt_urls.view(model='gallery.models.Category', view='gallery.views.category', slug_field='slug'), name='gallery'),
```

`mptt_urls.view` options are:
* `model` - your model derived from MPTTModel.
* `view` - a view which will process the request. Don't forget to capture `path` and `instance` (`def category(request, path, instance):`). If resolution fails, `instance` will be None.
* `slug_field` - the field where model instance's slug is stored

get_absolute_url()
------------------
Well, url(...) defines direct url resolution.
To define reverse url resolution, add to your model:
```
class Category(MPTTModel):
    ...
    def get_absolute_url(self):
        return reverse('gallery', kwargs={'path': self.get_path()})
```
Here, we use `Category.get_path()` which is available since using `mptt_urls.view`.

License
-------
MIT. Do whatever you like.
View license file for details.


