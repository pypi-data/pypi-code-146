from steam_sdk.data.DataRoxieParser import RoxieData
from steam_sdk.data.DataFiQuS import DataFiQuS, MultipoleRoxieGeometry, MultipoleSettings, MultipoleConductor


class BuilderFiQuS:
    """
        Class to generate FiQuS models
    """

    def __init__(self,
                 model_data,
                 roxie_data=None,
                 flag_build: bool = True,
                 flag_plot_all: bool = False,
                 verbose: bool = True):
        """
        Object is initialized by defining FiQuS variable structure and file template.
        :param model_data: DataModelMagnet object
        :param roxie_data: RoxieData object
        :param flag_build: boolean, if set to true data objects needed for ParserFiQuS are assembled
        :param flag_plot_all: this flag gets passed to FiQuS input file for multipole only TODO: is this what we want long term
        :param verbose: if set to True, additional information is printed
        """
        # Unpack arguments
        self.verbose: bool = verbose

        if flag_build:

            # Data structure
            self.data_FiQuS = DataFiQuS(magnet={'type': model_data.GeneralParameters.magnet_type})

            # --------- general ----------
            self.data_FiQuS.general.magnet_name = model_data.GeneralParameters.magnet_name
            self.data_FiQuS.magnet.type = model_data.GeneralParameters.magnet_type
            self.data_FiQuS.run = model_data.Options_FiQuS.run

            if model_data.GeneralParameters.magnet_type == 'multipole':
                if not roxie_data:
                    raise Exception(f'Cannot build model instantly without providing RoxieData as input roxie_data')
                self.buildDataMultipole(model_data, roxie_data, flag_plot_all)
            elif model_data.GeneralParameters.magnet_type == 'CCT_straight':
                self.buildDataCCT(model_data)
            else:
                raise Exception(f'Magnet type: {model_data.GeneralParameters.magnet_type} is incompatible with FiQuS.')

    def buildDataCCT(self, model_data): #TODO: good idea to make them private?
        """
            Load selected conductor data from DataModelMagnet keys, check inputs, calculate and set missing variables
        """
        # --------- geometry ----------
        # windings
        for key, value in model_data.Options_FiQuS.cct.geometry.windings.dict().items():       # for keys that are present in the FiQUS Options model data (but not all keys in data FiQuS)
            self.data_FiQuS.magnet.geometry.windings.__setattr__(key, value)
        self.data_FiQuS.magnet.geometry.windings.n_turnss = model_data.CoilWindings.CCT_straight.winding_numberTurnsFormers  # additional, picked form other places in model data

        self.data_FiQuS.magnet.postproc.windings_wwns = model_data.CoilWindings.CCT_straight.winding_numRowStrands
        self.data_FiQuS.magnet.postproc.windings_whns = model_data.CoilWindings.CCT_straight.winding_numColumnStrands
        self.data_FiQuS.magnet.postproc.winding_order = model_data.CoilWindings.CCT_straight.winding_order

        # fqpls
        self.data_FiQuS.magnet.geometry.fqpls.fndpls = [val for val, flag in zip(model_data.Quench_Protection.FQPLs.fndpls, model_data.Quench_Protection.FQPLs.enabled) if flag]
        self.data_FiQuS.magnet.geometry.fqpls.fwhs = [val for val, flag in zip(model_data.Quench_Protection.FQPLs.fwhs, model_data.Quench_Protection.FQPLs.enabled) if flag]
        self.data_FiQuS.magnet.geometry.fqpls.fwws = [val for val, flag in zip(model_data.Quench_Protection.FQPLs.fwws, model_data.Quench_Protection.FQPLs.enabled) if flag]
        self.data_FiQuS.magnet.geometry.fqpls.n_sbs = [val for val, flag in zip(model_data.Quench_Protection.FQPLs.n_sbs, model_data.Quench_Protection.FQPLs.enabled) if flag]
        self.data_FiQuS.magnet.geometry.fqpls.names = [val for val, flag in zip(model_data.Quench_Protection.FQPLs.names, model_data.Quench_Protection.FQPLs.enabled) if flag]
        self.data_FiQuS.magnet.geometry.fqpls.r_bs = [val for val, flag in zip(model_data.Quench_Protection.FQPLs.r_bs, model_data.Quench_Protection.FQPLs.enabled) if flag]
        self.data_FiQuS.magnet.geometry.fqpls.r_ins = [val for val, flag in zip(model_data.Quench_Protection.FQPLs.r_ins, model_data.Quench_Protection.FQPLs.enabled) if flag]
        self.data_FiQuS.magnet.geometry.fqpls.thetas = [val for val, flag in zip(model_data.Quench_Protection.FQPLs.thetas, model_data.Quench_Protection.FQPLs.enabled) if flag]
        self.data_FiQuS.magnet.geometry.fqpls.z_ends = [val for val, flag in zip(model_data.Quench_Protection.FQPLs.z_ends, model_data.Quench_Protection.FQPLs.enabled) if flag]
        self.data_FiQuS.magnet.geometry.fqpls.z_starts = [val for val, flag in zip(model_data.Quench_Protection.FQPLs.z_starts, model_data.Quench_Protection.FQPLs.enabled) if flag]

        # formers
        for key, value in model_data.Options_FiQuS.cct.geometry.formers.dict().items():       # for keys that are present in the model data (but not all keys in data FiQuS)
            self.data_FiQuS.magnet.geometry.formers.__setattr__(key, value)
        self.data_FiQuS.magnet.geometry.formers.r_ins = model_data.CoilWindings.CCT_straight.former_inner_radiuses  # additional, picked form other places in model data
        self.data_FiQuS.magnet.geometry.formers.r_outs = model_data.CoilWindings.CCT_straight.former_outer_radiuses  # additional, picked form other places in model data

        # air
        self.data_FiQuS.magnet.geometry.air = model_data.Options_FiQuS.cct.geometry.air   # for keys that are present in the model data and in data FiQuS - they are the same

        # ------------- mesh --------------
        self.data_FiQuS.magnet.mesh = model_data.Options_FiQuS.cct.mesh                # for keys that are present in the model data and in data FiQuS - they are the same

        # ------------- solve -------------
        self.data_FiQuS.magnet.solve.windings = model_data.Options_FiQuS.cct.solve.windings              # for keys that are present in the model data and in data FiQuS - they are the same
        self.data_FiQuS.magnet.solve.fqpls.mu_rs = [val for val, flag in zip(model_data.Quench_Protection.FQPLs.mu_rs, model_data.Quench_Protection.FQPLs.enabled) if flag]
        self.data_FiQuS.magnet.solve.fqpls.currents = [val for val, flag in zip(model_data.Quench_Protection.FQPLs.currents, model_data.Quench_Protection.FQPLs.enabled) if flag]
        self.data_FiQuS.magnet.solve.fqpls.sigmas = [val for val, flag in zip(model_data.Quench_Protection.FQPLs.sigmas, model_data.Quench_Protection.FQPLs.enabled) if flag]
        self.data_FiQuS.magnet.solve.formers = model_data.Options_FiQuS.cct.solve.formers
        self.data_FiQuS.magnet.solve.air = model_data.Options_FiQuS.cct.solve.air
        self.data_FiQuS.magnet.solve.file_exts = model_data.Options_FiQuS.cct.solve.file_exts
        self.data_FiQuS.magnet.solve.pro_template = model_data.Options_FiQuS.cct.solve.pro_template
        self.data_FiQuS.magnet.solve.variables = model_data.Options_FiQuS.cct.solve.variables
        self.data_FiQuS.magnet.solve.volumes = model_data.Options_FiQuS.cct.solve.volumes

        # ------------- postproc ---------
        for key, value in model_data.Options_FiQuS.cct.postproc.dict().items():       # for keys that are present in the model data and in data FiQuS - they are the same
            self.data_FiQuS.magnet.postproc.__setattr__(key, value)

    def buildDataMultipole(self, model_data, roxie_data, flag_plot_all):
        """
            Load selected conductor data from DataModelMagnet keys, check inputs, calculate and set missing variables
        """

        # geom file
        self.data_FiQuS_geo = MultipoleRoxieGeometry()
        self.data_FiQuS_geo.Roxie_Data = RoxieData(**roxie_data.dict())

        # set file
        self.data_FiQuS_set = MultipoleSettings()
        self.data_FiQuS_set.Model_Data_GS.general_parameters.I_ref = \
            [model_data.Options_LEDET.field_map_files.Iref] * len(self.data_FiQuS_geo.Roxie_Data.coil.coils)
        for cond in model_data.Conductors:
            self.data_FiQuS_set.Model_Data_GS.conductors[cond.name] = MultipoleConductor(cable={'type': cond.cable.type})
            conductor = self.data_FiQuS_set.Model_Data_GS.conductors[cond.name]
            conductor.cable.bare_cable_width = cond.cable.bare_cable_width
            conductor.cable.bare_cable_height_mean = cond.cable.bare_cable_height_mean

        # --------- geometry ----------
        self.data_FiQuS.magnet.geometry = model_data.Options_FiQuS.multipole.geometry

        # ------------- mesh --------------
        self.data_FiQuS.magnet.mesh = model_data.Options_FiQuS.multipole.mesh

        # ------------- solve -------------
        self.data_FiQuS.magnet.solve.I_initial = \
            [model_data.Power_Supply.I_initial] * len(self.data_FiQuS_geo.Roxie_Data.coil.coils)
        self.data_FiQuS.magnet.solve.pro_template = model_data.Options_FiQuS.multipole.solve.pro_template

        # ------------- postproc ---------
        self.data_FiQuS.magnet.postproc = model_data.Options_FiQuS.multipole.postproc
