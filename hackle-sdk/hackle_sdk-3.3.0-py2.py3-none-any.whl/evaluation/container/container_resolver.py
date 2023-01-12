class ContainerResolver(object):

    def __init__(self, bucketer):
        self.bucketer = bucketer

    def is_user_in_container_group(self, container, bucket, experiment, user):
        identifier = user.identifiers.get(experiment.identifier_type)
        if identifier is None:
            return False

        slot = self.bucketer.bucketing(bucket, identifier)
        if slot is None:
            return False

        container_group = container.get_group_or_none(slot.variation_id)
        if container_group is None:
            raise Exception('ContainerGroup[{}]'.format(slot.variation_id))

        return experiment.id in container_group.experiments
