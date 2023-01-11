from .BaseSource import BaseSource
from guide_bot.elements import Element_kink


class ESS_Butterfly(BaseSource):
    """
    MCPL source for guide_bot

    Use MCPL file, but provide approximate width / height. These are not
    used in the component, but used for e.g. plotting.
    """

    def __init__(self, sector="N", beamline=1, height=0.03, acc_power=5.0, cold_frac=0.5, *args, **kwargs):
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

        mcpl_file : str
            Path for mcpl file
        """

        height_list = height
        if not isinstance(height, list):
            height_list = [height]
        for height_value in height_list:
            if height_value not in [0.03, 0.06]:
                raise InputError("ESS Butterfly component only support 0.03 m and 0.06 m height. Was :'" + str(height_value) + "'")

        kwargs["height"] = height

        super().__init__(*args, **kwargs)

        sector_list = sector
        if not isinstance(sector, list):
            sector_list = [sector]
        for index, sector_value in enumerate(sector_list):
            if sector_value not in ["N", "S", "E", "W"]:
                raise InputError("sector needs to be 'N', 'S', 'E' or 'W', was: '" + str(sector_value) + "'.")
            sector_list[index] = '"' + sector_value + '"' # Give string with quotes to McStas
        self.parameters.add("sector", sector_list)

        beamline_list = beamline
        if not isinstance(beamline, list):
            beamline_list = [beamline]
        for beamline_value in beamline_list:
            if not 0 < beamline_value < 12:
                raise InputError("beamline needs to be between 1 and 11, was: '" + str(beamline_value) + '".')
        self.parameters.add("beamline", beamline)

        self.parameters.add("acc_power", acc_power, unit="MW")

        cold_frac_list = cold_frac
        if not isinstance(cold_frac_list, list):
            cold_frac_list = [cold_frac]
        for cold_frac_value in cold_frac_list:
            if not 0 <= cold_frac_value <= 1:
                raise InputError("Cold frac has to be between 0 and 1, was " + str(cold_frac_value) + ".")
        self.parameters.add("cold_frac", cold_frac)

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

        src = instrument.add_component("ESS_butterfly", "ESS_butterfly", after="Origin")

        src.yheight = self["height"]
        src.sector = self["sector"]
        src.beamline = self["beamline"]
        src.cold_frac = self["cold_frac"]
        src.acc_power = self["acc_power"]
        
        # Focus depending on focus_info
        src.dist = focus_info["dist"]
        src.focus_xw = focus_info["width"]
        src.focus_yh = focus_info["height"]

        # Wavelength set by target class
        src.Lmin = "min_wavelength"
        src.Lmax = "max_wavelength"

    def add_start(self, guide, instrument_parameters):
        """
        Adds GuideElement to Guide describing what is between source and guide

        Since the ESS Butterfly moderator has a cold and hot side, it is relevant
        for a guide to point to the side which is most beneficial. This angle is
        optimized. It is also possible that a small translation is useful.

        Parameters
        ----------

        guide : Guide object
            Guide object after apply_guide_start method has been performed

        instrument_parameters : InstrumentParameterContainer
            Parameter container where parameters can be added for optimization
        """

        # Set optimize to True so the kink angle is optimized for performance and not los breaking
        start_kink = Element_kink.Kink(name="moderator_guide_kink",
                                       start_width=self["width"], start_height=self["height"],
                                       v_displacement=0.0, h_displacement=[-0.02, 0.02],
                                       angle=[-3, 3], optimize=True)

        guide.add_guide_element_at_start(start_kink)
