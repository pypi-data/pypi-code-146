from geant4_pybind import *

#from particle import Particle
#particle = Particle.from_pdgid(pdgid)
#mass = particle.mass

class SteppingAction(G4UserSteppingAction):

  def __init__(self, app):
    super().__init__()
    self.app  = app
    self.data_buffer = app.data_buffer

  def UserSteppingAction(self, aStep):
    aTrack = aStep.GetTrack()
    particle = aTrack.GetDefinition()
    pdgid = particle.GetPDGEncoding()
    uid = aTrack.GetTrackID()
    parent_uid = aTrack.GetParentID()
    pre_step_point = aStep.GetPreStepPoint()
    post_step_point = aStep.GetPostStepPoint()
    position = post_step_point.GetPosition()/m
    time = post_step_point.GetGlobalTime()/ns
    momentum = post_step_point.GetMomentum()/GeV
    Etot1 = pre_step_point.GetTotalEnergy()/GeV
    #Ekin1 = pre_step_point.GetKineticEnergy()/GeV
    Etot2 = post_step_point.GetTotalEnergy()/GeV
    #Ekin2 = post_step_point.GetKineticEnergy()/GeV
    # Save every track point
    if Etot1 > self.app.E_skip_min and Etot1 > 0.76e-3 and position.z > 0.:
      # keep step end point
      self.data_buffer.AddTrackPoint(uid, parent_uid, pdgid, position.x, position.y, position.z, time, Etot2)
