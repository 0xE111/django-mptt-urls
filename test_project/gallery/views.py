from django.shortcuts import render

def category(request, mptt_urls):
    # This is an example view.
    # Use views in mptt_urls only if you have some extra logic that cannot be done in template.
    # Otherwise, use 'template' setting.

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