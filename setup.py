import os
from setuptools import setup, find_packages

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-mptt-urls',
    version='2.0.0a1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django>=1.7', 'django-mptt>=0.6.1'],
    license='MIT',
    description='Django app for creating hierarchical URLs associated with django-MPTT models.',
    long_description=README,
    url='https://github.com/c0ntribut0r/django-mptt-urls',
    keywords='django mptt urls hierarchy clean friendly',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
