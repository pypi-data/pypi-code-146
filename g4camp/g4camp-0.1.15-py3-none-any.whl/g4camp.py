import sys, logging
logformat='[%(name)12s ] %(levelname)8s: %(message)s'
logging.basicConfig(format=logformat)

import pkg_resources
available_packages = [pkg.key for pkg in pkg_resources.working_set]
if 'geant4-pybind' in available_packages:
    from geant4_pybind import *
else:
    sys.exit("Package 'geant4_pybind' is not available.")

from g4camp.DetectorConstruction import DetectorConstruction
from g4camp.CustomPhysicsList import CustomPhysicsList
from g4camp.ActionInitialization import ActionInitialization
from g4camp.DataBuffer import DataBuffer

class g4camp:

    def __init__(self, physics="Custom", optics=True, primary_generator="gun", gun_args={},
                 multithread=False, thread_num=4):
        # By some reason multithread mode does not faster than serial mode
        # FIXME: number of threads can not be configured from here (why???)
        #
        self.log = logging.getLogger('g4camp')
        #
        super().__init__()
        self.optics = optics                        # switch on/off optic physics
        self.primary_generator = primary_generator  # can be 'gun' or 'gps'
        self.multithread=multithread
        self.thread_num=thread_num
        #
        self.data_buffer = DataBuffer()
        self.gps_macro = ""
        #
        self.ph_suppression_factor = 10 # must be integer
        self.skip_mode = 'fraction'     # 'fraction' (relative to E_init) or 'GeV' (absolute)
        self.skip_min = 0.              # min energy to skip particle (wrt. E_init or in GeV)
        self.skip_max = 1.e-2           # max energy to skip particle (wrt. E_init or in GeV)
        self.random_seed = 1
        self.det_height_m = 1500        # detector volume: cylinder height
        self.det_radius_m = 1500        # detector volume: cylinder radius
        # the following varialbes are to be set later
        self.E_skip_min = None          # min particle energy to skip
        self.E_skip_max = None          # max particle energy to skip
        self.E_init = None              # initial kinetic energy in GeV
        #
        self.physListOptions = {"FTFP_BERT": FTFP_BERT,
                                "QGSP_BERT": QGSP_BERT,
                                "QGSP_BIC": QGSP_BIC}
        #
        self.ph_counter = None
        #
        if multithread:
            self.runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.MT, thread_num)
        else:
            self.runManager = G4RunManagerFactory.CreateRunManager(G4RunManagerType.Serial)
        self.detConstruction = DetectorConstruction()
        if physics == "Custom": 
            self.physList = CustomPhysicsList(optics=self.optics)
        else:
            self.physList = self.physListOptions[physics]()
            if self.optics :
                self.log.error("Optics is only available with 'Custom' physics list")
                sys.exit()
        self.actInit = ActionInitialization(self, primary_generator=self.primary_generator, 
                                                  gun_args=gun_args)
        self.runManager.SetUserInitialization(self.detConstruction)
        self.runManager.SetUserInitialization(self.physList)
        self.runManager.SetUserInitialization(self.actInit)
        #
        self.setVerbose()
        self.setDefaultCuts()


    def configure(self):
        #self.actInit.stackingAction.SetPhotonSuppressionFactor(1./self.ph_fraction)
        if self.multithread: 
            UImanager.ApplyCommand(f"/run/numberOfThreads", [self.thread_num])
        if self.optics:
            self.configureOptics()
        self.detConstruction.SetHeight(self.det_height_m)
        self.detConstruction.SetRadius(self.det_radius_m)
        self.runManager.Initialize()
        #self.applyGeant4Command("/run/particle/dumpCutValues")
        if self.primary_generator == 'gps':
            self.applyGeant4Command("/control/execute", [self.gps_macro])
        G4Random.setTheSeed(self.random_seed)

    def setVerbose(self, control_verbose=0, tracking_verbose=0, run_verbose=0, 
                   em_process_verbose=0, had_process_verbose=0):
        self.applyGeant4Command("/control/verbose", [control_verbose])
        self.applyGeant4Command("/tracking/verbose", [tracking_verbose])
        self.applyGeant4Command("/run/verbose", [run_verbose])
        self.applyGeant4Command("/process/em/verbose", [em_process_verbose])
        self.applyGeant4Command("/process/had/verbose", [had_process_verbose])
        self.applyGeant4Command("/process/eLoss/verbose 0")
        self.applyGeant4Command("/particle/verbose 0")
        self.applyGeant4Command("/cuts/verbose 0")

    def setCut(self, particle, cut_value, cut_unit):
        # to be invoked before 'configure()'
        self.applyGeant4Command("/run/setCutForAGivenParticle", [particle, cut_value, cut_unit])

    def setDefaultCuts(self):
        # default cuts ensure all particle capable to produce Cherenkov light are tracked
        # i.e. E_threshold is about 260 keV (kinetic energy)
        self.setCut("e+", 0.055, "cm")
        self.setCut("e-", 0.055, "cm")
        self.setCut("gamma", 95., "cm")
        #self.applyGeant4Command("/cuts/setLowEdge", [760, "keV"]) # This can only lower energy limit

    def applyGeant4Command(self, command, arguments=[]):
        arg_string = ""
        for arg in arguments:
            arg_string += f" {arg}"
        UImanager = G4UImanager.GetUIpointer()
        UImanager.ApplyCommand(command + arg_string)
        #print(command + arg_string)

    def configureOptics(self):
        if not self.optics:
            self.log.warning("Optics is disabled")
            return
        self.applyGeant4Command("/process/optical/processActivation", ['Cerenkov', True])
        self.applyGeant4Command("/process/optical/processActivation", ['OpAbsorption', False])
        self.applyGeant4Command("/process/optical/processActivation", ['OpRayleigh', False])
        self.applyGeant4Command("/process/optical/processActivation", ['OpMieHG', False])
        self.applyGeant4Command("/process/optical/cerenkov/setStackPhotons", [True])

    def setGunParticle(self, pname):
        self.applyGeant4Command(f"/gun/particle {pname}")

    def setGunEnergy(self, ene_val, ene_unit):
        self.applyGeant4Command(f"/gun/energy {ene_val} {ene_unit}")

    def setGunPosition(self, x_val, y_val, z_val, pos_unit):
        self.applyGeant4Command(f"/gun/position {x_val} {y_val} {z_val} {pos_unit}")

    def setGunDirection(self, dx, dy, dz):
        self.applyGeant4Command(f"/gun/direction {dx} {dy} {dz}")

    def setGPSMacro(self, macro):
        if self.primary_generator != 'gps':
            self.log.warning("'primary_generator' was set to '{self.primary_generator}', switching it to 'gps'")
            self.primary_generator = 'gps'
        self.gps_macro = macro

    def setSkipMinMax(self, skip_min, skip_max):
        self.skip_min = skip_min
        self.skip_max = skip_max

    def setRandomSeed(self, val):
        self.random_seed = int(val)

    def setPhotonSuppressionFactor(self, val):
        self.ph_suppression_factor = float(val)

    def setDetectorHeight(self, val):
        self.det_height_m = val

    def setDetectorRadius(self, val):
        self.det_radius_m = val

    def run(self, n_events):
        self.log.debug(f"random seed: {G4Random.getTheSeed()}")
        for i in range(n_events):
            self.runManager.BeamOn(1)
            yield self.data_buffer
