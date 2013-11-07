import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-mptt-urls',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django>=1.5.1', 'django-mptt>=0.5.5'],
    license='MIT License',
    description='Django app for creating hierarchical URLs associated with django-MPTT models.',
    long_description=README,
    url='https://github.com/MrKesn/django-mptt-urls',
    author='Alexandr Goncharov',
    author_email='kesn@yandex.ru',
    keywords='django mptt urls hierarchy clean friendly',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)