class FactoryPlanDebug(dict):
    """
    A subclass of dict that allows us to specify the default values to use
    for the various debug settings available to a factory
    """

    DEMOLISH_ON_FAILURE_KEY = "demolish_on_failure"

    def __init__(self, *args, **kwargs):
        super(FactoryPlanDebug, self).__init__(*args, **kwargs)

        for (
            _debug_key,
            _debug_configuration,
        ) in self._debug_configuration().items():
            self.setdefault(_debug_key, _debug_configuration["default"])
            # Set it as an attribute for easier lookups
            setattr(self, f"_{_debug_key}", self[_debug_key])

    @classmethod
    def _debug_configuration(cls):
        """
        The main source of truth for factory debugging.  Keys in here can be
        specified on a factory plan.  Keys not provided on the factory plan
        will default to the value here.
        Usage:
        # factory-plan.yaml
        factory:
           debug:
              demolish_on_failure: false
        """
        return {
            # Should we demolish the factory on build failure?  Ensure we
            # do this by default
            cls.DEMOLISH_ON_FAILURE_KEY: {"default": True}
        }

    @property
    def _demolish_on_failure_msg(self):
        """
        Helper to show a consistent message in the various places that we
        inform the user that demolishing isn't happening
        """
        return (
            "Resources have not been deleted because "
            f"`{self.DEMOLISH_ON_FAILURE_KEY}` is set to false. These will "
            "have to be tidied up manually using the "
            "`qalx factory-demolish` command. "
            "See the logs for more details"
        )
