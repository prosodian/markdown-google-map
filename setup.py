from setuptools import setup

# To develop this markdown extension itself, you should install with
# pip install -e .[dev] to get dev dependencies
setup(
    name='mdx_google_map',
    description='A python Markdown extension providing Google Maps syntax',
    long_description=(
        'A python Markdown extension providing Google Maps syntax. '
        'For more details visit https://github.com/tictocs/markdown-google-map'
    ),
    author='Tom Manterfield @ Tic Tocs Tech',
    author_email='tom@tictocs.com',
    url='https://github.com/tictocs/markdown-google-map/',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3'
    ],
    version='1.0.0',
    py_modules=['mdx_google_map'],
    install_requires=['markdown>=2.6.11'],
    extras_require={
        'dev': ['beautifulsoup4']
    },
    project_urls={
        'Bug Reports': 'https://github.com/tictocs/markdown-google-map/issues',
        'Source': 'https://github.com/tictocs/markdown-google-map/',
    })
    
