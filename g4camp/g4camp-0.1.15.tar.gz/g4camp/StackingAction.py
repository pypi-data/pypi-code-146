from geant4_pybind import *
import numpy as np

class StackingAction(G4UserStackingAction):

  def __init__(self, app):
    super().__init__()
    self.app = app
    self.data_buffer = app.data_buffer
    self.E_init = app.E_init
    self.ph_suppression_factor = app.ph_suppression_factor
    # Cherenkov threshold
    n = 1.35
    self.cerenkov_threshold_factor = 1./(1.-n**2)
    self.cerenkov_threshold_e = 511*keV * self.cerenkov_threshold_factor
    # E_th = mc^2 / sqrt(1-1/n^2),
    # where n = 1.35 for water, so 1/sqrt(1-1/n^2) = 1.4885
    #   for e+/e- E_th = 760 keV
    #   for mu    E_th = 157 MeV

  def ClassifyNewTrack(self, track):
    # If /process/optical/cerenkov/setTrackSecondariesFirst is set to True
    # then tracks are stacked even in the middle of their life,
    # so this method is invoked not only on particle creation.
    # This is temporary used to skip particles based on their energy,
    # because the possibility to kill particle in Stepping action is not 
    # yet available (G4Track.SetTrackStatus() is not yet pythonized).
    uid = track.GetTrackID()
    parent_uid = track.GetParentID()
    position = track.GetPosition()/m
    time = track.GetGlobalTime()/ns
    pdgid = track.GetDefinition().GetPDGEncoding()
    momentum = track.GetMomentum()/GeV
    Etot = track.GetTotalEnergy()/GeV
    Ekin = track.GetKineticEnergy()/GeV
    # 
    # = Primary particles =======================
    #
    if uid == 1 and track.GetCurrentStepNumber() == 0: # only primary particle at the start point
      self.ph_suppression_factor = self.app.ph_suppression_factor
      self.app.E_init = Ekin
      self.app.E_skip_min = self.app.skip_min
      self.app.E_skip_max = self.app.skip_max
      if self.app.skip_mode == "fraction":
        self.app.E_skip_min *= self.app.E_init
        self.app.E_skip_max *= self.app.E_init
      self.data_buffer.AddTrackPoint(uid, parent_uid, pdgid, position.x, position.y, position.z, time, Etot)
      #
      particle_name = track.GetDefinition().GetParticleName()
      energy_sting = G4BestUnit(Ekin*GeV, "Energy")
      x,y,z = position.x, position.y, position.z
      px, py, pz = momentum.x, momentum.y, momentum.z
      pmag = np.sqrt(px**2+py**2+pz**2)
      px, py, pz = px/pmag, py/pmag, pz/pmag
      self.app.log.info(f"{particle_name}:  Ekin={energy_sting}  position=({x:.1f}, {y:.1f}, {z:.1f}) m\
  direction=({px:.1f}, {py:.1f}, {pz:.1f}) ")
      return G4ClassificationOfNewTrack.fUrgent
    #
    # = Optical photons =========================
    #
    # - Store info and kill
    #
    try:
        track.GetDefinition()
    except:
        print("could not get definition")
        
    if track.GetDefinition() == G4OpticalPhoton.OpticalPhoton():
      if self.app.ph_counter%self.ph_suppression_factor == 0:
        position = track.GetPosition()/m
        direction = track.GetMomentumDirection()
        time = track.GetGlobalTime()/ns
        wavelength = 1.23984193*1.e-6/Etot # in nm
        ph = np.array([position.x, position.y, position.z,
                       time,
                       direction.x, direction.y, direction.z,
                       wavelength])
        self.data_buffer.AddPhoton(ph)
        #if parent_uid != 1: print(f"{time:.4f} photon    parent uid: {parentuid}")
      self.app.ph_counter += 1
      return G4ClassificationOfNewTrack.fKill
    #
    #
    # = All particles except optical photons ====
    #
    # === kill if z < 0
    if position.z < 0.:
      return G4ClassificationOfNewTrack.fKill
    #
    # === store particle data for e- and e+ if E_skip_min < Etot < E_skip_max
    elif Etot > self.app.E_skip_min and Etot <= self.app.E_skip_max and uid != 1 \
         and track.GetDefinition() in [G4Electron.Electron(), G4Positron.Positron()]:
      self.app.data_buffer.AddParticle(parent_uid, pdgid, position.x, position.y, position.z, time,
                                       momentum.x, momentum.y, momentum.z, Etot)
      #print(f"{time:.4f}   = to kill =    uid: {uid},  parent uid: {parent_uid}, {pdgid}, energy: {Ekin:.4f}")
      return G4ClassificationOfNewTrack.fKill
    #
    # kill slow neutrions (E < 1 GeV)
    elif track.GetDefinition() == G4Neutron.Neutron() and Etot < 1:
      return G4ClassificationOfNewTrack.fKill
    #
    # === propagete other particles and store their tracks 
    else:
      self.data_buffer.AddTrackPoint(uid, parent_uid, pdgid, position.x, position.y, position.z, time, Etot)
      return G4ClassificationOfNewTrack.fUrgent

