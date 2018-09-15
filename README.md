# markdown-google-map
Python markdown extension for Google Maps. Should be [loaded as an extension](https://python-markdown.github.io/extensions/) 
to the [markdown library](https://python-markdown.github.io/).

### Installation:
pip install git+git://github.com/tictocs/markdown-google-map.git

### Usage:
```python
import markdown

md = markdown.Markdown(extensions=["mdx_google_map"])
md.convert("[map:Central Paris]")
```

OR

```python
import markdown

md = markdown.Markdown(extensions=[GoogleMapExtension(...config values...)])
md.convert("[map:Central Paris]")
```

### Markdown syntax:
It's pretty simple:

```markdown
Hey look at my map!
[map:City of London]
```

Which will output:

```html
<p>
Hey look at my map!
<iframe allowfullscreen="true" frameborder="0" height="300" src="//www.google.com/maps/embed/v1/place?key=AIzaSyD5DlGo1lo0V2Np7TxfpuNuWbWcr5TV8Sw&amp;q=City+of_London" width="500"></iframe>
</p>
```

### Configuring:
You will need an API Key from Google to use the Maps APIs, once obtained it can
be configured as an environment variable:

`$ export GOOGLE_API_KEY=MyGoogleAPIKey1234`

or simply passed through to the extension as with any other config:

`GoogleMapExtension(google_api_key='MyGoogleAPIKey1234')`

You can also load the API key by passing a callable that conforms to the same
syntax as dict.get('KEY', 'default value'). This is more of an
implementation detail, but it is supported if you find the need.

```python

my_dict = {'GOOGLE_API_KEY': 'MyGoogleAPIKey1234'}

GoogleMapExtension(config_getter=my_dict.get)
```

***Explicitly passing the google_api_key config param takes precedence over other
methods of setting the API Key.***

*All other config is optional and detailed below*

Config is passed through when loading the extension as with the API Key example
above:

`GoogleMapExtension(width='500', height='400', ...)`

- **width**: Sets width of iframe. Default is 500
- **height**: Sets height of iframe. Default is 300
- **fluid**: If True the iframe will be wrapped in a styled outer div set to 100%
    width. This will make the iframe expand to full width of the page (or any 
    other container you put it in) fludily, whilst maintaining the same aspect
    ratio. Default is False.
