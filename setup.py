from os import path
from setuptools import setup


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='mdx_google_map',
    description='A python Markdown extension providing Google Maps syntax',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Tom Manterfield @ Tic Tocs Tech',
    author_email='tom@tictocs.com',
    url='https://github.com/tictocs/markdown-google-map/',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    version='1.0.1',
    py_modules=['mdx_google_map'],
    install_requires=['markdown>=2.6.11'],
    extras_require={
        'dev': ['beautifulsoup4']
    },
    project_urls={
        'Bug Reports': 'https://github.com/tictocs/markdown-google-map/issues',
        'Source': 'https://github.com/tictocs/markdown-google-map/',
    })
    
