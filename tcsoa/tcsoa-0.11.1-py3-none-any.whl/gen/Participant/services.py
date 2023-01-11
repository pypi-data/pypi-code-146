from tcsoa.gen.Participant._2018_11.services import ParticipantService as imp0
from tcsoa.base import TcService


class ParticipantService(TcService):
    addParticipants = imp0.addParticipants
    reassignParticipants = imp0.reassignParticipants
    removeParticipants = imp0.removeParticipants
