from .BaseSource import BaseSource
from guide_bot.elements import Element_gap
from guide_bot.parameters import instrument_parameters as ipars


class Moderator(BaseSource):
    """
    Simple example of a guide_bot source inheriting from BaseSource

    Simple rectangular source description with constant intensity as a
    function of wavelength. Uses the McStas component Source_simple.
    """

    def __init__(self, *args, **kwargs):
        """
        Simple example of a guide_bot source inheriting from BaseSource

        Simple rectangular source description with constant intensity as a
        function of wavelength. Uses the McStas component Source_simple.

        Parameters
        ----------

        width : float / list for scan
            Width of the rectangular source in [m]

        height : float / list for scan
            Height of the rectangular source in [m]

        guide_start : float / list for scan
            Given distance from source to start of guide (guides can overwrite)

        min_guide_start : float / list for scan
            Minimum distance from source to guide (guides can overwrite)

        max_guide_start : float / list for scan
            Maximum distance from source to guide (guides can overwrite)
        """
        super().__init__(*args, **kwargs)

    def add_to_instrument(self, instrument, instrument_parameters, focus_info):
        """
        Add to instrument adds McStas code describing the source

        Here adding the Source_simple component after origin with the
        parameters contained in the object and given in the method input.

        Parameters
        ----------

        instrument : McStasScript instr object
            Instrument object which the source should be added to

        instrument_parameters : InstrumentParameterContainer object
            Parameter container where parameters can be added for optimization

        focus_info : dict
            Dict with info on focusing to be used by the source
        """

        src = instrument.add_component("Moderator", "Source_simple", after="Origin")

        src.xwidth = self["width"]
        src.yheight = self["height"]

        src.dist = focus_info["dist"]
        src.focus_xw = focus_info["width"]
        src.focus_yh = focus_info["height"]

        # min / max_wavelength parameters always defiend by sample
        src.lambda0 = "0.5 * (min_wavelength + max_wavelength)"
        src.dlambda = "0.5*(max_wavelength - min_wavelength)"


class ModeratorDoubleGap(Moderator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_start(self, guide, instrument_parameters):
        """
        Adds GuideElement to Guide describing what is between source and guide

        In most cases there is just a Gap between the source and the guide,
        which is what will be insterted from the BaseSource. One could imagine
        sources with some other element, perhaps reflector parts, that can be
        added. These can be optimized or have fixed values as if they were
        provided by the user.

        Parameters
        ----------

        guide : Guide object
            Guide object after apply_guide_start method has been performed

        instrument_parameters : InstrumentParameterContainer
            Parameter container where parameters can be added for optimization
        """

        start_gap = Element_gap.Gap(name="moderator_guide_gap_1", start_width=self["width"],
                                    start_height=self["height"])
        guide.add_guide_element_at_start(start_gap)

        start_gap_2 = Element_gap.Gap(name="moderator_guide_gap_2", start_width=1.5*self["width"],
                                      start_height=1.5*self["height"])
        guide.add_guide_element_at_start(start_gap_2)


class ModeratorFree(Moderator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_to_instrument(self, instrument, instrument_parameters, first_element):
        """
        Add to instrument adds McStas code describing the source

        Here adding the Source_simple component after origin with the
        parameters contained in the object and given in the method input.

        Parameters
        ----------

        instrument : McStasScript instr object
            Instrument object which the source should be added to

        instrument_parameters : InstrumentParameterContainer object
            Parameter container where parameters can be added for optimization

        first_element : GuideElement
            The first user provided GuideElement after the source
        """

        src = instrument.add_component("Moderator", "Source_simple", after="Origin")

        mod_pos = ipars.FreeInstrumentParameter("mod_position", -0.1, 0.1)
        instrument_parameters.add_parameter(mod_pos)

        src.set_AT([0, "mod_position", 0], RELATIVE="Origin")

        src.xwidth = self["width"]
        src.yheight = self["height"]

        src.dist = first_element.get_length_name()
        src.focus_xw = first_element.end_width.name
        src.focus_yh = first_element.end_height.name

        # min / max_wavelength parameters always defiend by sample
        src.lambda0 = "0.5 * (min_wavelength + max_wavelength)"
        src.dlambda = "0.5*(max_wavelength - min_wavelength)"