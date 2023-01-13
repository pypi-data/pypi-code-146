    @classmethod
    def updateWith(klass, objID : str, spec : dict) -> object:
        """
        Update the receiver with new values for the attributes set in spec.

        spec:

        ```
        spec = {
        }
        ```

        Arguments
        ---------
            objID : str
        The TripleObject ID to update

            spec : dict
        A dict object with the appropriate object references:

        - assumed_name
        - address

        The address should be generated using a Coronado Address object and
        then calling its asSnakeCaseDictionary() method

        Returns
        -------
            aTripleObject
        An updated instance of the TripleObject associated with objID, or None
        if the objID isn't associated with an existing resource.

        Raises
        ------
            CoronadoError
        A CoronadoError dependent on the specific error condition.  The full list of
        possible errors, causes, and semantics is available in the
        **`coronado.exceptions`** module.
        """
        endpoint = '/'.join([klass._serviceURL, '%s/%s' % (klass._servicePath, objID)]) # URL fix later
        response = requests.request('PATCH', endpoint, headers = klass.headers, json = spec)

        if response.status_code == 200:
            result = klass(response.content.decode())
        elif response.status_code == 404:
            result = None
        else:
            raise errorFor(response.status_code, info = response.text)

        return result



