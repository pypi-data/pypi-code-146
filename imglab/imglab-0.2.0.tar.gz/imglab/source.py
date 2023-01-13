import os


class Source:
    """A class to represent imglab sources

    :Examples:
        >>> import imglab
        >>> source = imglab.Source("assets")
        >>> source = imglab.Source("assets", subdomains=False)
        >>> source = imglab.Source("assets", https=False, host="imglab.net", port=8080)

    :param name: The name of source
    :type name: str
    :param host: A host to be used with the source, defaults to 'imglab-cdn.net'
    :type host: str, optional
    :param https: A bool value specifying if the source should use https schema to generate host value, defaults to `True`
    :type https: bool, optional
    :param port: A integer identifying the port to be used with the source, defaults to None
    :type port: int, optional
    :param secure_key: A string value with the secure_key to be used with the source, defaults to None
    :type secure_key: str, optional
    :param secure_salt: A string value with the secure_salt to be used with the source, defaults to None
    :type secure_salt: str, optional
    :param subdomains: A bool value specifying if the source should use subdomains or not, defaults to `True`
    :type subdomains: bool, optional
    """

    DEFAULT_HOST = "imglab-cdn.net"
    DEFAULT_HTTPS = True
    DEFAULT_SUBDOMAINS = True

    def __init__(
        self,
        name,
        host=DEFAULT_HOST,
        https=DEFAULT_HTTPS,
        port=None,
        secure_key=None,
        secure_salt=None,
        subdomains=DEFAULT_SUBDOMAINS,
    ):
        self._host = host
        self._https = https
        self._name = name
        self._port = port
        self._secure_key = secure_key
        self._secure_salt = secure_salt
        self._subdomains = subdomains

    @property
    def host(self):
        """Returns the host used by the source

        :return: A string value with the host used by the source
        :rtype: str
        """
        if self.subdomains:
            return "%s.%s" % (self.name, self._host)
        else:
            return self._host

    @property
    def https(self):
        """Returns if the source uses https or not

        :return: `True` if the source uses https scheme, `False` otherwise
        :rtype: bool
        """
        return self._https

    @property
    def name(self):
        """Returns the name of the source

        :return: A string value with the name of the source
        :rtype: str
        """
        return self._name

    @property
    def port(self):
        """Returns the port used by the source

        :return: An integer value identifying the port used by the source or None if no port is used
        :rtype: int, None
        """
        return self._port

    @property
    def secure_key(self):
        """Returns the secure_key used by the source

        :return: A string value with the secure_key used by the source or None if no secure_key is used
        :rtype: str, None
        """
        return self._secure_key

    @property
    def secure_salt(self):
        """Returns the secure_salt used by the source

        :return: A string value with the secure_salt used by the source or None if no secure_salt is used
        :rtype: str, None
        """
        return self._secure_salt

    @property
    def subdomains(self):
        """Returns if the source uses subdomains or not

        :return: `True` if the source uses subdomains, `False` otherwise
        :rtype: bool
        """
        return self._subdomains

    def scheme(self):
        """Returns the URI scheme to be used with the source ('http' or 'https')

        :return: 'https' if the source is using https scheme, 'http' otherwise
        :rtype: str
        """
        if self.https:
            return "https"
        else:
            return "http"

    def path(self, path):
        """Returns the path to be used with the source

        :param path: A path to be used
        :type path: str
        :return: A string with the path to be used with the source
        :rtype: str
        """
        if self.subdomains:
            return path
        else:
            return os.path.join(self.name, path)

    def is_secure(self):
        """Returns if the source is secure or not

        :return: `True` if the source is secure, `False` otherwise
        :rtype: bool
        """
        return bool(self.secure_key and self.secure_salt)
