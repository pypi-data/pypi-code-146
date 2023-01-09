from djangoldp.views import LDPViewSet
from ..models import NeedleActivity
from ..models.needle_activity import ACTIVITY_TYPE_NEW_USER


class NeedleActivityViewset(LDPViewSet):
    # TODO: check change only read
    pass


def create_welcome_needle_activity(user):
    welcome = NeedleActivity(activity_type=ACTIVITY_TYPE_NEW_USER, title="Ajoutez une première Fiche à votre Fil",
                             content="Quelles sont les dernières trouvailles marquantes que vous ayez faites sur le web ?",
                             creator=user)
    welcome.save()
