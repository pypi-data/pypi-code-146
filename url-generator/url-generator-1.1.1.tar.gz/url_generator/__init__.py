
import json
from pathlib import Path
from urllib.parse import urlencode

"""Keywords used in configuration"""
CONFIG_KEYWORDS = [
    '@scheme',
    '@host',
    '@tld',
    '@path',
    '@query',
    '@fragment',
    '@subdomain',
    '@host_postfix'
]

ALLOWED_URL_SCHEMES = [
    'http',
    'https'
]


class UrlGenerator(object):
    def __init__(self, config_file_path, **kwargs):
        """
        Args:
            config_file_path (str): Path to configuration file
            **kwargs: Global parameters

        Raises:
            UrlGeneratorException Ff the configuration file is not found.
        """
        self.params = kwargs

        config_file = Path(config_file_path)
        if not config_file.is_file():
            raise UrlGeneratorException('Configuration file not found "{}"'.format(config_file_path))

        with open(config_file, 'r', encoding='utf8') as f:
            self.config = json.loads(f.read())

    def get_url(self, _path, **kwargs):
        """Return compiled URL from given $pathString using configuration.

        See Readme.md for more information

        Args:
            _path (str): like 'heureka.category.index'
            **kwargs: Additional parameters like `category='auto-moto', page_index=10, lang='sk'`

        Returns:
            str: Compiled URL like 'https://auto-moto.heureka.sk?page=10'
        """
        _path = _path.split('.')

        params = self.params.copy()
        params.update(kwargs)

        config = self._get_url_parts(_path, params, self.config)

        query_string = self._compile_query_string(config['@query'], params) if '@query' in config else ''

        url_template = self.url_join(config, query_string)

        return self.compile_url_template(url_template, params)

    def compile_url_template(self, url, params):
        """Compile and sanitize URL template
        !Note that $params are deleted when used!

        Args:
            url (str): URL Template like 'http://{category_name}.heureka.{lang}/'
            params (dict): like `lang='cz', ...`

        Returns:
            str: Compiled template like 'http://auto-moto.heureka.cz/'

        Raises:
            UrlGeneratorException if any mandatory parameter is missing
        """
        try:
            return url.format(**params)
        except KeyError:
            raise UrlGeneratorException('Missing mandatory parameter')

    def url_join(self, url_parts, query_string):
        """Joins URL defined by configuration

        Args:
            url_parts (dict): like ['@sheme' => 'https, '@host' => 'www.heureka.{tld}', '@path' => 'search' ...]
            query_string (str): like 'q=automobily&offset=2&limit=10'

        Returns:
            str: Compiled URL like 'https://www.heureka.cz/search/?q=automobily&offset=2&limit=1'
        """
        if '@scheme' not in url_parts:
            raise UrlGeneratorException('Missing required property @scheme')

        scheme = url_parts['@scheme']
        if scheme not in ALLOWED_URL_SCHEMES:
            raise UrlGeneratorException('Unsupported URL scheme: "{}"'.format(scheme))

        if '@host' not in url_parts:
            raise UrlGeneratorException('Missing required property @host')

        host = url_parts['@host'].rstrip('/')
        subdomain = url_parts.get('@subdomain')
        host_postfix = url_parts.get('@host_postfix')

        url = "{}://{}{}{}".format(
            scheme,
            f'{subdomain}.' if subdomain else '',
            host,
            f'.{host_postfix}' if host_postfix else ''
        )

        if '@path' in url_parts:
            url += '/{}'.format(url_parts['@path'].lstrip('/'))

        if query_string != '':
            url += '?{}'.format(query_string)

        if '@fragment' in url_parts:
            url += '#{}'.format(url_parts['@fragment'].lstrip('#'))

        return url

    def _compile_query_string(self, query_config, params):
        """Compiles query string from parameters using queryConfig
        !Note that $params are deleted when used!

        Args:
            query_config (dict): configuration like `offset='o', limit='l'`
            params (dict): like `offset=2, limit=10`

        Returns:
            str: Compiled query like 'o=2&l=10'
        """
        query_params = {}
        for param_name, param_key in query_config.items():
            if param_name in params:
                query_params[param_key] = params[param_name]

        return urlencode(query_params)

    def _get_url_parts(self, path, params, config):
        """Gets url parts configuration recursively for given path

        Args:
            path (list): Like ['heureka', 'category', 'index'] means 'heureka.category.index'
            params (dict): Like `category='auto-moto', page_index=10, lang='sk'`
            config (dict): Main configuration array

        Returns:
            dict: Containing urlParts like ['@sheme' => 'https, '@host' => 'www.heureka.{tld}', '@path' => 'search' ...]
        """
        url_parts = {}

        for key, value in config.items():
            if key in CONFIG_KEYWORDS:
                url_parts[key] = value

            if path and key == path[0]:
                _path = path.copy()
                _path.pop(0)
                url_parts.update(self._get_url_parts(_path, params, config[key]))

            if self._evaluate_template_condition(key, params):
                url_parts.update(self._get_url_parts(path, params, config[key]))

        return url_parts

    def _evaluate_template_condition(self, condition, params):
        """Evaluates condition like "{variable}=value" if variable equals value.

        Args:
            condition (str):
            params:

        Returns:
            bool
        """
        if '{' not in condition or not params:
            return False
        try:
            parts = condition.split('=')

            return parts[0].format(**params) == parts[1].format(**params)
        except KeyError:
            return False


class UrlGeneratorException(Exception):
    pass
