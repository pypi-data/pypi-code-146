from daggerml import Resource, register_tag


TAG = 'com.daggerml.resource.docker'
DAG_NAME = TAG
DAG_VERSION = 1


class DockerResource(Resource):
    def __init__(self, resource_id, executor, tag=TAG):
        super().__init__(resource_id, executor, tag)

    @property
    def url(self):
        return self.id

register_tag(TAG, DockerResource)
