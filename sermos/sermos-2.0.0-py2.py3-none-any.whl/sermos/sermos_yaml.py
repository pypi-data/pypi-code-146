""" Definition of the `sermos.yaml` file. This is only relevant/used for
managed deployments through Sermos.ai. If self-hosting, safely disregard this
yaml format, no `sermos.yaml` is required for your application.

If using, a basic file may look like::

    imageConfig:
        - name: private-worker-image
          imageUri: rhoai/private-worker-image:latest
          registryDomain: index.docker.io/v1/
          registryUser: rhoai
          registryPassword: abc123
        - name: public-api-image
          imageUri: myregistry/public-api-image

    environmentVariables:
        - name: GLOBAL_ENV_VAR
            value: globally-available-env-var

    serviceConfig:
        - name: demo-api
          serviceType: external
          serviceId: ${SERVICE_ID_API}  # Rendered using `sermos deploy` if available in the environment.
          imageName: public-api-image
          command: gunicorn --log-level info -k gevent -b 0.0.0.0:5000 sermos_demo_client.app:create_app()
          port: 5000
          replicaCount: 1
          cpuLimit: 0.5
          memoryLimit: 0.5
          environmentVariables:
            - name: FLASK_SECRET_KEY
              value: ${FLASK_SECRET_KEY}
        - name: sermos-worker
          serviceType: celery-worker
          serviceId: ${SERVICE_ID_WORKER}
          imageName: private-worker-image
          command: celery -A sermos_demo_client.celery worker --without-gossip --without-mingle -c '1' -l INFO --queue default-task-queue
          replicaCount: 1
          cpuLimit: 0.5
          memoryLimit: 0.5
          registeredTasks:
            - handler: sermos_demo_client.workers.demo_worker.demo_worker_task
            - handler: sermos_demo_client.workers.demo_worker.demo_model_task
          environmentVariables:
            - name: WORKER_NAME
              value: sermos-worker

    pipelines:
        demo-pipeline:
            name: demo-pipeline
            description: Demo Pipeline.
            schemaVersion: 1
            config:
                dagAdjacency:
                    node_a:
                        - node_b
                        - node_c
                metadata:
                    maxRetry: 3
                    maxTtl: 60
                    queue: default-task-queue
                taskDefinitions:
                    node_a:
                        handler: sermos_demo_client.workers.demo_pipeline.demo_pipeline_node_a
                    node_b:
                        handler: sermos_demo_client.workers.demo_pipeline.demo_pipeline_node_b
                        queue: node-b-queue
                    node_c:
                        handler: sermos_demo_client.workers.demo_pipeline.demo_pipeline_node_c

    scheduledTasks:
        demo-model-task:
            name: Demo Model Task
            enabled: true
            config:
                scheduleType: interval
                task: sermos_demo_client.workers.demo_worker.demo_model_task
                queue: default-task-queue
                schedule:
                    every: 60
                    period: seconds
            schemaVersion: 1

"""
import re
import os
import logging
import pkg_resources
import yaml
from urllib.parse import urlparse
from yaml.loader import SafeLoader
from marshmallow import Schema, fields, pre_load, EXCLUDE, INCLUDE,\
    validates_schema
from marshmallow.validate import OneOf, Range
from marshmallow.exceptions import ValidationError
from sermos.constants import SERMOS_YAML_PATH
from sermos.pipeline_config_schema import BasePipelineSchema
from sermos.schedule_config_schema import BaseScheduleSchema

logger = logging.getLogger(__name__)


class InvalidSermosConfig(Exception):
    pass


class MissingSermosConfig(Exception):
    pass


class InvalidImageConfig(Exception):
    pass


class ExcludeUnknownSchema(Schema):
    class Meta:
        unknown = EXCLUDE


class EnvironmentVariableSchema(ExcludeUnknownSchema):
    """ A single environment variables (singular)
    """
    name = fields.String(required=True,
                         description="Environment variable name.",
                         example="MY_ENV_VAR")
    value = fields.String(required=True,
                          description="Environment variable value.",
                          example="my special value")


class EnvironmentVariablesSchema(Schema):
    """ Multiple environment variables (plural)
    """
    environmentVariables = fields.List(
        fields.Nested(EnvironmentVariableSchema, required=True),
        description="List of name/value environment variable pairs available "
        "to the scope of this service.",
        required=False)


class ServiceRequestsSchema(Schema):

    replicaCount = fields.Integer(
        required=False,
        description="Baseline (min) scale of this service to have available.",
        default=1,
        example=1)
    cpuRequest = fields.Float(
        required=False,
        description="Requested CPUs to be available for each replica.",
        default=0.5,
        example="0.5")
    memoryRequest = fields.Float(
        required=False,
        description=
        "Requested memory (in GB) to be available for each replica.",
        default=0.5,
        example="0.5 (means half of 1 GB)")
    ephemeralStorageRequest = fields.Float(
        required=False,
        description="Requested ephemeral storage (in GB) to "
        "be available for each replica.",
        default=8,
        example="2 (means 2 GB)")
    cpuLimit = fields.Float(
        required=False,
        description="Maximum CPUs to be available for each replica.",
        default=0.5,
        example="0.5")
    memoryLimit = fields.Float(
        required=False,
        description="Maximum memory (in GB) to be available for each replica.",
        default=0.5,
        example="0.5 (means half of 1 GB)")
    ephemeralStorageLimit = fields.Float(
        required=False,
        description="Maximum ephemeral storage (in GB) to "
        "be available for each replica.",
        default=8,
        example="2 (means 2 GB)")


class SermosServiceHealthCheckSchema(Schema):
    healthCheckType = fields.String(required=False,
                                    description="Type of health check to use.",
                                    example="TCP or HTTP",
                                    validate=OneOf(['TCP', 'HTTP']))
    healthCheckPort = fields.Integer(
        required=False,
        description="Port (and targetPort) for health check.",
        validate=Range(min_inclusive=1, max_inclusive=65535),
        example=8080)
    healthCheckPath = fields.String(
        required=False,
        description="Path to access on the HTTP Server.",
        example="/healthz",
        default='/')
    healthCheckInitialDelaySeconds = fields.Integer(
        required=False,
        description="Number of seconds after the container has started before\
         health check probes are initiated.",
        example=0,
        default=0,
        validate=Range(min_inclusive=0))
    healthCheckPeriodSeconds = fields.Integer(
        required=False,
        description="How often (in seconds) to perform the health check probe.",
        example=10,
        default=10,
        validate=Range(min_inclusive=1))
    healthCheckTimeoutSeconds = fields.Integer(
        required=False,
        description="Number of seconds after which the health check "
        "probe times out",
        example=1,
        default=1,
        validate=Range(min_inclusive=1))
    healthCheckSuccessThreshold = fields.Integer(
        required=False,
        description="Minimum consecutive successes for the health check "
        "probe to be considered successful after having failed.",
        example=1,
        default=1,
        validate=Range(min_inclusive=1))
    healthCheckFailureThreshold = fields.Integer(
        required=False,
        description="Maximum consecutive failures for the health check "
        "probe.  Service will restart upon threshold met.",
        example=3,
        default=3,
        validate=Range(min_inclusive=1))


class NameSchema(Schema):
    """ Validated name string field.
    """
    name = fields.String(
        required=True,
        description="Name for service or image. Must include "
        "only alphanumeric characters along with `_` and `-`.",
        example="my-service-name")

    @pre_load
    def validate_characters(self, item, **kwargs):
        """ Ensure name field conforms to allowed characters
        """
        valid_chars = r'^[\w\d\-\_]+$'
        if not bool(re.match(valid_chars, item['name'])):
            raise ValueError(
                f"Invalid name: {item['name']}. Only alphanumeric characters "
                "allowed along with `-` and `_`.")
        return item


class SermosImageConfigSchema(NameSchema):
    imageUri = fields.String(
        required=False,
        description="The Docker Image URI. Tag is optional, if excluded, "
        "`latest` is used.",
        example="rhoai/public-image ; rhoai/private-image:0.0.0")
    registryDomain = fields.String(
        required=False,
        description="Optional - Registry domain when using a private image "
        "that requires authentication. When using private images, all of "
        "registryDomain, registryUser, and registryPassword are required.",
        example="index.docker.io")
    registryUser = fields.String(
        required=False,
        description="Optional - Registry username when using a private image "
        "that requires authentication. When using private images, all of "
        "registryDomain, registryUser, and registryPassword are required.",
        example="rhoai")
    registryPassword = fields.String(
        required=False,
        description="Optional - Registry password when using a private image "
        "that requires authentication. When using private images, all of "
        "registryDomain, registryUser, and registryPassword are required."
        "NOTE: Strongly recommended to use environment "
        "variable interpolation in your sermos.yaml file, do not commit "
        "unencrypted secrets to a git repository. "
        "e.g. repositoryPassword: ${DOCKER_REPOSITORY_PASSWORD}",
        example="abc123!")


class SermosSharedConfigSchema(Schema):
    """ Attributes shared across internal and external service types
    """
    serviceId = fields.String(
        required=False,
        _required=False,
        description="The serviceId provided by Sermos. Find in admin console. "
        "Ensure this exists if you want a stable serviceId for purposes of "
        "proxying, etc. If you don't include this in your sermos.yaml, it "
        "will be overloaded/regenerated each deployment. That's fine in most "
        "scenarios.",
        example="dry-gorge-8018")

    command = fields.String(
        required=False,
        _required=True,
        description="Command to be run as container CMD. Can be ''.",
        example="gunicorn -b 0.0.0.0:5000 package.app:create_app()")

    port = fields.Integer(
        required=False,
        _required=True,
        description="Port (and targetPort) to direct traffic.",
        example=5000)


class SermosExternalConfigSchema(SermosSharedConfigSchema):
    """ Attributes required for serviceType: external

        Note: Schema lists these are not required in order for this to be used
        as a mixin to SermosServiceConfigSchema. The validation is done
        programmatically based on serviceType.
    """
    customDns = fields.String(
        required=False,
        _required=False,
        description="Custom CNAME record that points to Sermos. The "
        "destination DNS record will be shown to you in the Sermos Admin "
        "console when creating a new External Service. For example, create a "
        "CNAME record (myapp.mydomain.com) and point to the provided Cluster "
        "DNS (e.g. sermos-eks11.sermos.ai). Sermos Cloud will not allow you to "
        "deploy this external service if you have not properly set up your "
        "DNS record beforehand. If this is not set, Sermos Cloud will provide "
        "a custom external DNS record in the form of "
        "[serviceId].[destination.cluster.domain], "
        "e.g. happy-whale-d17783.sermos.io NOTE: do not include protocol "
        "(e.g. http/https).",
        example="myapp.mydomain.com or None")


class SermosInternalSchema(SermosSharedConfigSchema):
    """ Attributes required for serviceType: internal

        Note: Schema lists these are not required in order for this to be used
        as a mixin to SermosServiceConfigSchema. The validation is done
        programmatically based on serviceType.
    """
    protocol = fields.String(required=False,
                             _required=True,
                             description="Protocol to use.",
                             example="TCP",
                             validate=OneOf(['TCP', 'UDP']))


class SermosRegisteredTaskDetailConfigSchema(Schema):
    handler = fields.String(
        required=True,
        description="Full path to the Method handles work / pipeline tasks.",
        example="sermos_customer_client.workers.worker_group.useful_worker")

    event = fields.Raw(
        required=False,
        unknown=INCLUDE,
        description="Arbitrary user data, passed through `event` arg in task.")


class SermosCeleryWorkerConfigSchema(Schema):
    """ Attributes required for serviceType: celery-worker

        Note: Schema lists these are not required in order for this to be used
        as a mixin to SermosServiceConfigSchema. The validation is done
        programmatically based on serviceType.
    """
    command = fields.String(
        required=False,
        _required=True,
        description="Command to be run as container CMD.",
        example="celery -A mypkg.celery.celery worker --queue my-queue")

    registeredTasks = fields.List(
        fields.Nested(SermosRegisteredTaskDetailConfigSchema, required=True),
        required=False,
        _required=True,
        description="List of task handlers to register for to your Sermos app."
    )


# Mapping of serviceType keys to their respective schema
service_types = {
    'external': SermosExternalConfigSchema,
    'internal': SermosInternalSchema,
    'celery-worker': SermosCeleryWorkerConfigSchema
}


class SermosServiceConfigSchema(ExcludeUnknownSchema, ServiceRequestsSchema,
                                EnvironmentVariablesSchema,
                                SermosExternalConfigSchema,
                                SermosInternalSchema,
                                SermosCeleryWorkerConfigSchema, NameSchema,
                                SermosServiceHealthCheckSchema):
    """ Base service config object definition for workers and internal/external
        services.
    """
    imageName = fields.String(
        required=True,
        description="Specify the name of the base image to use for this "
        "service.",
        example="custom-worker-name")

    serviceType = fields.String(required=True,
                                description="Type of Service",
                                example="external; internal; celery-worker",
                                validate=OneOf(service_types.keys()))


def _validate_image_config(image_dict: dict) -> bool:
    """ Validate proper use of private/public docker image definitions
    """
    required_for_private = ('registryDomain', 'registryUser',
                            'registryPassword')
    if any(key in image_dict for key in required_for_private) \
            and not all(key in image_dict for key in required_for_private):
        raise InvalidImageConfig(
            "All of registryDomain, registryUser, registryPassword are "
            "required when using private docker images. Review "
            f"image `{image_dict['name']}`")
    return True


def _validate_custom_dns(service_dict: dict) -> bool:
    """ Validate customDns field in an external service.

        Can't include protocol, must be a valid domain.

        Valid: foo.bar.com / foo-api.my-domain.co.uk
        Invalid: https://foo.bar.com

        NOTE: This will not validate that it's an operational DNS record, that
        will happen if deploying to Sermos Cloud. So, something like
        "foo" will pass this validation but is obviously not a valid
        DNS record. This is very basic, only using urlparse for now, so it will
        accept funky stuff like `x-y-z` - that'll be verified downstream before
        a deployment is allowed to go through.
    """
    dns_record = service_dict.get('customDns', None)
    if not dns_record:
        return True  # Empty / not set is fine

    # We only want a value that parses as a path with no other values parsed
    parsed_url_dict = urlparse(dns_record)._asdict()
    for k in parsed_url_dict:
        if k != 'path' and parsed_url_dict[k] != '':
            raise InvalidImageConfig(
                "customDns value should not include "
                "any protocol or other URL elements, it should be in form "
                "api.mydomain.com")
        if k == 'path' and parsed_url_dict[k] == '':
            raise InvalidImageConfig("customDns should be in form "
                                     "api.mydomain.com")
    return True


class SermosYamlSchema(ExcludeUnknownSchema, EnvironmentVariablesSchema):
    """ The primary `sermos.yaml` file schema. This defines all available
        properties in a valid Sermos configuration file.
    """

    imageConfig = fields.List(fields.Nested(SermosImageConfigSchema,
                                            required=True),
                              required=True,
                              description="List of available base images. At "
                              "least one image must be defined. The 'name' "
                              "of the image is used in each service defined "
                              "in `serviceConfig`")

    serviceConfig = fields.List(
        fields.Nested(SermosServiceConfigSchema,
                      required=True,
                      description="Core service configuration."),
        description="List of services for Sermos to manage.",
        required=True)

    pipelines = fields.Dict(keys=fields.String(),
                            values=fields.Nested(BasePipelineSchema),
                            description="List of pipelines",
                            required=False)

    scheduledTasks = fields.Dict(keys=fields.String(),
                                 values=fields.Nested(BaseScheduleSchema),
                                 description="List of scheduled tasks",
                                 required=False)

    def validate_errors(self, schema: Schema, value: dict):
        """ Run Marshmallow validate() and raise if any errors
        """
        schema = schema()
        errors = schema.validate(value)
        if len(errors.keys()) > 0:
            raise ValidationError(errors)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        """ Additional validation.

            Nested fields that are not required are not validated by Marshmallow
            by default. Do a single level down of validation for now.

            Each serviceType has attributes that are required but are listed
            as not required in the marshmallow schema. Validate here.
        """
        # Vaidate nested
        key_schema_pairs = (
            ('imageConfig', SermosImageConfigSchema),
            ('environmentVariables', EnvironmentVariableSchema),
            ('serviceConfig', SermosServiceConfigSchema),
        )
        for k_s in key_schema_pairs:
            val = data.get(k_s[0], None)
            if val is not None:
                if type(val) == list:
                    for v in val:
                        self.validate_errors(k_s[1], v)
                else:
                    self.validate_errors(k_s[1], val)

        # Validate the services. We list every service schema field as not
        # required in order to use them as mixins for a generic service object,
        # however, they ARE required, so validate here using the custom
        # metadata property `_required`. Default to value of `required`.
        service_image_names = []
        for service in data.get('serviceConfig'):
            service_type = service['serviceType']
            schema = service_types[service_type]
            for field in schema().fields:
                try:
                    if schema().fields[field].metadata.get(
                            '_required',
                            getattr(schema().fields[field], 'required')):
                        assert field in service
                except AssertionError:
                    raise ValidationError(
                        f"`{field}` missing in {service_type} definition.")

            if service_type == 'external':
                _validate_custom_dns(service)

            service_image_names.append(service['imageName'])

        # Validate imageConfig and get list of image names
        image_names = []
        for image in data.get('imageConfig'):
            image_names.append(image['name'])
            _validate_image_config(image)

        # Verify each imageName referenced in each service exists in imageConfig
        try:
            assert set(service_image_names).issubset(image_names)
        except AssertionError:
            raise InvalidImageConfig(
                "Mismatched imageName in at least one "
                f"service ({service_image_names}) compared to images available "
                f"in imageConfig ({image_names})")

        # Validate unique pipeline ids
        if 'pipelines' in data:
            pipeline_ids = set()
            for pipeline_id, pipeline_data in data['pipelines'].items():
                if pipeline_id in pipeline_ids:
                    raise ValidationError("All pipeline ids must be unique!")
                pipeline_ids.add(pipeline_id)
                schema_version = pipeline_data['schemaVersion']
                PipelineSchema = \
                    BasePipelineSchema.get_by_version(schema_version)
                self.validate_errors(PipelineSchema, pipeline_data)

        # Validate unique scheduled tasks names
        if 'scheduledTasks' in data:
            task_ids = set()
            for task_id, task_data in data['scheduledTasks'].items():
                if task_id in task_ids:
                    raise ValidationError("All schedule ids must be unique!")
                task_ids.add(task_id)
                schema_version = task_data['schemaVersion']
                TaskSchema = BaseScheduleSchema.get_by_version(schema_version)
                self.validate_errors(TaskSchema, task_data)


class YamlPatternConstructor():
    """ Adds a pattern resolver + constructor to PyYaml.

        Typical/deault usage is for parsing environment variables
        in a yaml file but this can be used for any pattern you provide.

        See: https://pyyaml.org/wiki/PyYAMLDocumentation
    """
    def __init__(self,
                 env_var_pattern: str = None,
                 add_constructor: bool = True):
        self.env_var_pattern = env_var_pattern
        if self.env_var_pattern is None:
            # Default pattern is: ${VAR:default}
            self.env_var_pattern = r'^\$\{(.*)\}$'
        self.path_matcher = re.compile(self.env_var_pattern)

        if add_constructor:
            self.add_constructor()

    def _path_constructor(self, loader, node):
        """ Extract the matched value, expand env variable,
            and replace the match

            TODO: Would need to update this (specifically the parsing) if any
            pattern other than our default (or a highly compatible variation)
            is provided.
        """
        # Try to match the correct env variable pattern in this node's value
        # If the value does not match the pattern, return None (which means
        # this node will not be parsed for ENV variables and instead just
        # returned as-is).
        env_var_name = re.match(self.env_var_pattern, node.value)
        try:
            env_var_name = env_var_name.group(1)
        except AttributeError:
            return None

        # If we get down here, then the 'node.value' matches our specified
        # pattern, so try to parse. env_var_name is the value inside ${...}.
        # Split on `:`, which is our delimiter for default values.
        env_var_name_split = env_var_name.split(':')

        # Attempt to retrieve the environment variable...from the environment
        env_var = os.environ.get(env_var_name_split[0], None)

        if env_var is None:  # Nothing found in environment
            # If a default was provided (e.g. VAR:default), return that.
            # We join anything after first element because the default
            # value might be a URL or something with a colon in it
            # which would have 'split' above
            if len(env_var_name_split) > 1:
                return ":".join(env_var_name_split[1:])
            return 'unset'  # Return 'unset' if not in environ nor default
        return env_var

    def add_constructor(self):
        """ Initialize PyYaml with ability to resolve/load environment
            variables defined in a yaml template when they exist in
            the environment.

            Add to SafeLoader in addition to standard Loader.
        """
        # Add the `!env_var` tag to any scalar (value) that matches the
        # pattern self.path_matcher. This allows the template to be much more
        # intuitive vs needing to add !env_var to the beginning of each value
        yaml.add_implicit_resolver('!env_var', self.path_matcher)
        yaml.add_implicit_resolver('!env_var',
                                   self.path_matcher,
                                   Loader=SafeLoader)

        # Add constructor for the tag `!env_var`, which is a function that
        # converts a node of a YAML representation graph to a native Python
        # object.
        yaml.add_constructor('!env_var', self._path_constructor)
        yaml.add_constructor('!env_var',
                             self._path_constructor,
                             Loader=SafeLoader)


def parse_config_file(sermos_yaml: str):
    """ Parse the `sermos.yaml` file when it's been loaded.

        Arguments:
            sermos_yaml (required): String of loaded sermos.yaml file.
    """
    YamlPatternConstructor()  # Add our env variable parser
    try:
        sermos_yaml_schema = SermosYamlSchema()
        # First suss out yaml issues
        sermos_config = yaml.safe_load(sermos_yaml)
        # Then schema issues
        sermos_config = sermos_yaml_schema.load(sermos_config)
    except ValidationError as e:
        msg = "Invalid Sermos configuration due to {}"\
            .format(e.messages)
        logger.error(msg)
        raise InvalidSermosConfig(msg)
    except InvalidImageConfig as e:
        msg = "Invalid imageConfig configuration due to {}"\
            .format(e)
        logger.error(msg)
        raise InvalidImageConfig(msg)
    except Exception as e:
        msg = "Invalid Sermos configuration, likely due to invalid "\
            "YAML formatting ..."
        logger.exception("{} {}".format(msg, e))
        raise InvalidSermosConfig(msg)
    return sermos_config


def load_sermos_config(sermos_yaml_filename: str = None, as_dict: bool = True):
    """ Load and parse the `sermos.yaml` file. Issue usable exceptions for
        known error modes so bootstrapping can handle appropriately.

        Arguments:
            sermos_yaml_filename (optional): Relative path to find your
                `sermos.yaml` configuration file. Defaults to `sermos.yaml`
                which should be found relative to invocation.
            as_dict (optional): If true (default), return the loaded sermos
                configuration as a dictionary. If false, return the loaded
                string value of the yaml file.
    """
    if sermos_yaml_filename is None:
        sermos_yaml_filename = SERMOS_YAML_PATH

    logger.info(f"Loading `sermos.yaml` from file location "
                f"`{sermos_yaml_filename}` ...")
    sermos_config = None

    try:
        with open(sermos_yaml_filename, 'r') as f:
            sermos_yaml = f.read()
            sermos_config = parse_config_file(sermos_yaml)
    except InvalidSermosConfig as e:
        raise
    except InvalidImageConfig as e:
        raise
    except FileNotFoundError as e:
        msg = "Sermos config file could not be found at path {} ...".format(
            sermos_yaml_filename)
        raise MissingSermosConfig(msg)
    except IsADirectoryError as e:
        msg = "sermos_yaml_filename is a directory, config file not found"
        raise MissingSermosConfig(msg)
    except Exception as e:
        raise e
    if as_dict:
        return sermos_config
    return yaml.safe_dump(sermos_config)
