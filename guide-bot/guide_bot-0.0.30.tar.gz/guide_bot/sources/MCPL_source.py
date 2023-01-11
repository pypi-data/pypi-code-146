from .BaseSource import BaseSource


class MCPL_source(BaseSource):
    """
    MCPL source for guide_bot

    Use MCPL file, but provide approximate width / height. These are not
    used in the component, but used for e.g. plotting.
    """

    def __init__(self, mcpl_file, repeat_count=1, E_smear=0, pos_smear=0, dir_smear=0,
                 x_offset=0, y_offset=0, z_offset=0, x_rotation=0, y_rotation=0, z_rotation=0,
                 scaling=1.0, *args, **kwargs):
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

        super().__init__(*args, **kwargs)

        self.parameters.add("mcpl_file", mcpl_file, is_filename=True)
        self.parameters.add("E_smear", E_smear)
        self.parameters.add("pos_smear", pos_smear, unit="m")
        self.parameters.add("dir_smear", dir_smear, unit="deg")
        self.parameters.add("repeat_count", repeat_count)
        self.parameters.add("scaling", scaling)
        self.parameters.add("x_offset", x_offset)
        self.parameters.add("y_offset", y_offset)
        self.parameters.add("z_offset", z_offset)
        self.parameters.add("x_rotation", x_rotation)
        self.parameters.add("y_rotation", y_rotation)
        self.parameters.add("z_rotation", z_rotation)


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

        src = instrument.add_component("MCPL_source", "MCPL_input", after="Origin")

        src.filename = self["mcpl_file"]
        src.dir_smear = self["dir_smear"]
        src.pos_smear = self["pos_smear"]
        src.E_smear = self["E_smear"]
        src.repeat_count = self["repeat_count"]

        # Wavelength to energy:
        # min / max_wavelength parameters always defined by sample
        # wavelength -> k: 2*pi/wavelength
        src.Emin = "2.0*PI/max_wavelength*2.0*PI/max_wavelength*K2V*K2V*VS2E"
        src.Emax = "2.0*PI/min_wavelength*2.0*PI/min_wavelength*K2V*K2V*VS2E"

        # Allow rotation in case a coordinate change is needed
        src.set_ROTATED([self["x_rotation"], self["y_rotation"], self["z_rotation"]], RELATIVE="Origin")

        # Handle position offsets on coordinate
        if self["x_offset"] != 0:
            src.append_EXTEND(f"x += {self['x_offset']};")
        if self["y_offset"] != 0:
            src.append_EXTEND(f"y += {self['y_offset']};")
        if self["z_offset"] != 0:
            src.append_EXTEND(f"z += {self['z_offset']};")

        # Optional scaling
        if self["scaling"] != 1.0:
            src.append_EXTEND(f"p *= {self['scaling']};")

        face = instrument.add_component("moderator_face", "Shape", after=src)
        face.set_AT([0, 0, 0], RELATIVE="Origin")
        face.xwidth=self["width"]
        face.yheight=self["height"]

        face.append_EXTEND("ALLOW_BACKPROP;")
        face.append_EXTEND("PROP_Z0;")
        face.append_EXTEND("SCATTER;")



