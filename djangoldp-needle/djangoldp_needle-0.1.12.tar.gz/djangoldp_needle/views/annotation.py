from django.core.exceptions import SuspiciousOperation
from djangoldp.views import LDPViewSet, LDPNestedViewSet
from rest_framework.exceptions import ValidationError

from ..models import Annotation, NeedleActivity
from ..models.needle_activity import ACTIVITY_TYPE_FIRST_ANNOTATION_WITH_CONNECTIONS, \
    ACTIVITY_TYPE_FIRST_ANNOTATION_WITHOUT_CONNECTIONS
import json


class AnnotationViewset(LDPViewSet):
    def is_safe_create(self, user, validated_data, *args, **kwargs):
        # TODO: check new annotation owner by current user

        target_url_id = validated_data['target']['urlid']
        user_annotation_with_same_target_count = Annotation.objects.filter(creator=user).filter(
            target__urlid=target_url_id).count()

        if user_annotation_with_same_target_count > 0:
            raise ValidationError({'Attention': ['Vous avez déjà cette ressource dans votre fil.']})
        return True

def create_first_annotation_activity_annotation_with_connections(annotation):
    first_annotation_activity = NeedleActivity(activity_type=ACTIVITY_TYPE_FIRST_ANNOTATION_WITH_CONNECTIONS,
                                               title="Grâce à votre fiche, vous croisez déjà d'autres personnes",
                                               content="Découvrez leurs Fils pour faire de nouvelles trouvailles.",
                                               creator=annotation.creator)
    first_annotation_activity.save()


def create_first_annotation_activity_annotation_without_connections(annotation):
    new_annotation_target_activity = NeedleActivity(activity_type=ACTIVITY_TYPE_FIRST_ANNOTATION_WITHOUT_CONNECTIONS,
                                                    title="Votre fiche sort de l'ordinaire",
                                                    content="vous êtes la première personne à l'avoir ajoutée à votre Fil.\nAjoutez-en d'autres pour augmenter vos chances de croiser les Fils d'autres personnes, ou bien parcourez les carnets publics existants.",
                                                    creator=annotation.creator)
    new_annotation_target_activity.save()


def create_first_annotation_activity_first_annotation_with_connections(annotation):
    first_annotation_activity = NeedleActivity(activity_type=ACTIVITY_TYPE_FIRST_ANNOTATION_WITH_CONNECTIONS,
                                               title="Grâce à votre première fiche, vous croisez déjà d'autres personnes",
                                               content="Découvrez leurs Fils pour faire de nouvelles trouvailles.",
                                               creator=annotation.creator)
    first_annotation_activity.save()


def create_first_annotation_activity_first_annotation_without_connections(annotation):
    new_annotation_target_activity = NeedleActivity(activity_type=ACTIVITY_TYPE_FIRST_ANNOTATION_WITHOUT_CONNECTIONS,
                                                    title="Votre première fiche sort de l'ordinaire",
                                                    content="vous êtes la première personne à l'avoir ajoutée à votre Fil.\nAjoutez-en d'autres pour augmenter vos chances de croiser les Fils d'autres personnes, ou bien parcourez les carnets publics existants.",
                                                    creator=annotation.creator)
    new_annotation_target_activity.save()
