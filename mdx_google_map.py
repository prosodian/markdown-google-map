import os
from urllib.parse import urlencode

from markdown.extensions import Extension
from markdown.inlinepatterns import Pattern
from markdown.util import etree


MAP_MATCH = r'\[map:(?P<location_name>[^\]]+)\]'


class GoogleMapExtension(Extension):
    def __init__(self, config_getter=os.environ.get, **kwargs):
        """
        Initialise Google Maps Markdown Extension with overridable config

        Args:
            config_getter: A callable object that conforms to the interface
                get('key', 'default') e.g. os.environ.get or dict.get
        """
        google_api_key = config_getter('GOOGLE_API_KEY', '')
        
        self.config = {
            'google_api_key': [
                google_api_key, 'Google API Key required to load maps',
            ],
            'width': ['500', 'Width of iframe for map'],
            'height': ['300', 'Height of iframe for map'],
            'fluid': [
                False, 'Should iframe be wrapped in div allowing fluid sizing?'
            ]
        }

        super().__init__(**kwargs)

    def extendMarkdown(self, md, md_globals):
        """
        Extends markdown with inline patterns providing Google map function.

        See base class for further info.
        """
        google_map = GoogleMapPattern(MAP_MATCH)
        google_map.extension_conf = self.config
        md.inlinePatterns['google_map'] = google_map


class GoogleMapPattern(Pattern):
    extension_conf = None

    def handleMatch(self, match):
        """
        Handles a regex match object, rendering the matching map tag as a map.

        Args:
            match: A regex match object that will match map markdown and group
                the location.
        
        Returns:
            An etree.Element of the generated map html.
        """
        location = match.group('location_name')

        return self._render_iframe(location)

    def _render_iframe(self, location):
        """
        Creates an iframe that will be a google map centered on the given
        location.

        Additional configuration is taken from the calling class
        GoogleMapsExtension.config dict.

        Args:
            location: A plain text string detailing the location to be passed
                to google maps. e.g. 'City of London'.

        Returns:
            an etree.Element of either an iframe or, in the case that
            extension_conf['fluid'] is Truthy, a div wrapping an iframe.

        """
        gmaps_url = "//www.google.com/maps/embed/v1/place?"
        query = {
            'key': self.extension_conf['google_api_key'][0],
            'q': location
        }
        src = gmaps_url + urlencode(query)

        width = str(self.extension_conf['width'][0])
        height = str(self.extension_conf['height'][0])

        iframe = etree.Element('iframe')
        iframe.set('width', width)
        iframe.set('height', height)
        iframe.set('src', src)
        iframe.set('allowfullscreen', 'true')
        iframe.set('frameborder', '0')

        wrapper = self._fluid_wrapper(iframe)

        return wrapper or iframe

    def _fluid_wrapper(self, iframe):
        """
        Wraps the given iframe in a div and adds styling to both in order to
        create a fluid sized, full-width iframe.

        Only wraps the element if the config 'fluid' is set to True.

        Args:
            iframe: An etree.Element object of the iframe.

        Returns:
            An etree element with the iframe as a child, the case that
            extension_conf['fluid'] is Falsey, returns None.
        """
        if self.extension_conf['fluid']:
            wrapper_style = (
                'position:relative;padding-bottom:56.25%;'
                'padding-top:25px;height:0;'
            )
            iframe_style = (
                'position:absolute;top:0;left:0;width:100%;height:100%;'
            )

            iframe.set('style', iframe_style)

            wrapper = etree.Element('div')
            wrapper.set('class', 'iframe-wrapper')
            wrapper.set('style', wrapper_style)
            wrapper.append(iframe)

        else:
            wrapper = None

        return wrapper
