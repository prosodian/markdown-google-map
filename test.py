import unittest
from urllib.parse import urlparse, parse_qs

from bs4 import BeautifulSoup
import markdown

from mdx_google_map import GoogleMapExtension


class ExtensionTestCase(unittest.TestCase):
    def test_creates_single_map(self):
        gmap_extension = GoogleMapExtension(google_api_key='KEY')
        md_output = markdown.markdown(
            '[map:London]', extensions=[gmap_extension])

        soup = BeautifulSoup(md_output, 'html.parser')
        iframes = soup.find_all('iframe')

        self.assertEqual(1, len(iframes))

    def test_creates_multiple_maps(self):
        gmap_extension = GoogleMapExtension(google_api_key='KEY')
        md_output = markdown.markdown(
            '[map:London]Dummy Text[map:Paris]', extensions=[gmap_extension])

        soup = BeautifulSoup(md_output, 'html.parser')
        iframes = soup.find_all('iframe')

        self.assertEqual(2, len(iframes))

    def test_returns_non_map_content(self):
        md_output = markdown.markdown('Foo', extensions=[GoogleMapExtension()])
        
        soup = BeautifulSoup(md_output, 'html.parser')
        iframes = soup.find_all('iframe')

        self.assertEqual('<p>Foo</p>', md_output)
        self.assertEqual(0, len(iframes))

    def test_src_is_correct(self):
        gmap_extension = GoogleMapExtension(google_api_key='KEY')
        md_output = markdown.markdown('[map:Loc]', extensions=[gmap_extension])

        soup = BeautifulSoup(md_output, 'html.parser')
        iframe_src = soup.find_all('iframe')[0]['src']

        url = urlparse(iframe_src)
        params = parse_qs(url.query)

        # Verify each component of the src attribute is correct.
        # We don't want to do a string comparison as query order is unimportant
        self.assertEqual(url.scheme, '')
        self.assertEqual(url.netloc, 'www.google.com')
        self.assertEqual(url.path, '/maps/embed/v1/place')
        # Make sure only one API key is set and that it is correct
        self.assertEqual('KEY', params['key'][0])
        self.assertEqual(1, len(params['key']))
        # Make sure only one location is set and that it is correct
        self.assertEqual('Loc', params['q'][0])
        self.assertEqual(1, len(params['q']))

    def test_width_and_height_set(self):
        gmap_extension = GoogleMapExtension(
            google_api_key='KEY', width=600, height=400)
        md_output = markdown.markdown('[map:Loc]', extensions=[gmap_extension])

        soup = BeautifulSoup(md_output, 'html.parser')
        iframe = soup.find('iframe')

        self.assertEqual('600', iframe['width'])
        self.assertEqual('400', iframe['height'])

    def test_adds_fluid_container(self):
        gmap_extension = GoogleMapExtension(
            google_api_key='KEY', fluid=True)
        md_output = markdown.markdown('[map:Loc]', extensions=[gmap_extension])

        soup = BeautifulSoup(md_output, 'html.parser')
        containers = soup.find_all('div', {"class": "iframe-wrapper"})
        iframes = containers[0].find_all("iframe")

        self.assertEqual(1, len(containers))
        self.assertEqual(1, len(iframes))


    def test_api_key_pulled_from_env(self):
        conf_getter = lambda val, _: 'MYKEY' if val == 'GOOGLE_API_KEY' else ''

        gmap_extension = GoogleMapExtension(config_getter=conf_getter)
        md_output = markdown.markdown('[map:Loc]', extensions=[gmap_extension])

        soup = BeautifulSoup(md_output, 'html.parser')
        iframe = soup.find('iframe')

        self.assertIn('MYKEY', iframe['src'])

    def test_explicit_api_key_takes_precedence_over_env(self):
        conf_getter = lambda val, _: 'MYKEY' if val == 'GOOGLE_API_KEY' else ''

        gmap_extension = GoogleMapExtension(
            config_getter=conf_getter, google_api_key='OVERRIDDENKEY')
        md_output = markdown.markdown('[map:Loc]', extensions=[gmap_extension])

        soup = BeautifulSoup(md_output, 'html.parser')
        iframe = soup.find('iframe')

        self.assertIn('OVERRIDDENKEY', iframe['src'])

    def test_explicit_api_key_set_from_config_with_env_unset(self):
        conf_getter = lambda val, _: ''

        gmap_extension = GoogleMapExtension(
            config_getter=conf_getter, google_api_key='OVERRIDDENKEY')
        md_output = markdown.markdown('[map:Loc]', extensions=[gmap_extension])

        soup = BeautifulSoup(md_output, 'html.parser')
        iframe = soup.find('iframe')

        self.assertIn('OVERRIDDENKEY', iframe['src'])
