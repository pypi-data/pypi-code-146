import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ...._jsii import *


@jsii.enum(
    jsii_type="@aws-prototyping-sdk/aws-arch.aws_arch.DrawioSpec.Aws4.ShapeNames"
)
class ShapeNames(enum.Enum):
    '''
    :stability: experimental
    '''

    A1_INSTANCE = "A1_INSTANCE"
    '''
    :stability: experimental
    '''
    ACCESS_ANALYZER = "ACCESS_ANALYZER"
    '''
    :stability: experimental
    '''
    ACTION = "ACTION"
    '''
    :stability: experimental
    '''
    ACTIVATE = "ACTIVATE"
    '''
    :stability: experimental
    '''
    ACTUATOR = "ACTUATOR"
    '''
    :stability: experimental
    '''
    ADDON = "ADDON"
    '''
    :stability: experimental
    '''
    AD_CONNECTOR = "AD_CONNECTOR"
    '''
    :stability: experimental
    '''
    AGENT = "AGENT"
    '''
    :stability: experimental
    '''
    AGENT2 = "AGENT2"
    '''
    :stability: experimental
    '''
    ALARM = "ALARM"
    '''
    :stability: experimental
    '''
    ALEXA_ENABLED_DEVICE = "ALEXA_ENABLED_DEVICE"
    '''
    :stability: experimental
    '''
    ALEXA_FOR_BUSINESS = "ALEXA_FOR_BUSINESS"
    '''
    :stability: experimental
    '''
    ALEXA_SKILL = "ALEXA_SKILL"
    '''
    :stability: experimental
    '''
    ALEXA_SMART_HOME_SKILL = "ALEXA_SMART_HOME_SKILL"
    '''
    :stability: experimental
    '''
    ALEXA_VOICE_SERVICE = "ALEXA_VOICE_SERVICE"
    '''
    :stability: experimental
    '''
    ALL_PRODUCTS = "ALL_PRODUCTS"
    '''
    :stability: experimental
    '''
    AMI = "AMI"
    '''
    :stability: experimental
    '''
    AMPLIFY = "AMPLIFY"
    '''
    :stability: experimental
    '''
    AMPLIFY_AWS_AMPLIFY_STUDIO = "AMPLIFY_AWS_AMPLIFY_STUDIO"
    '''
    :stability: experimental
    '''
    ANALYTICS = "ANALYTICS"
    '''
    :stability: experimental
    '''
    APACHE_MXNET_ON_AWS = "APACHE_MXNET_ON_AWS"
    '''
    :stability: experimental
    '''
    API_GATEWAY = "API_GATEWAY"
    '''
    :stability: experimental
    '''
    APPFLOW = "APPFLOW"
    '''
    :stability: experimental
    '''
    APPLICATION = "APPLICATION"
    '''
    :stability: experimental
    '''
    APPLICATION_AUTO_SCALING = "APPLICATION_AUTO_SCALING"
    '''
    :stability: experimental
    '''
    APPLICATION_COST_PROFILER = "APPLICATION_COST_PROFILER"
    '''
    :stability: experimental
    '''
    APPLICATION_DISCOVERY_SERVICE = "APPLICATION_DISCOVERY_SERVICE"
    '''
    :stability: experimental
    '''
    APPLICATION_INTEGRATION = "APPLICATION_INTEGRATION"
    '''
    :stability: experimental
    '''
    APPLICATION_LOAD_BALANCER = "APPLICATION_LOAD_BALANCER"
    '''
    :stability: experimental
    '''
    APPS = "APPS"
    '''
    :stability: experimental
    '''
    APPSTREAM_20 = "APPSTREAM_20"
    '''
    :stability: experimental
    '''
    APPSYNC = "APPSYNC"
    '''
    :stability: experimental
    '''
    APP_CONFIG = "APP_CONFIG"
    '''
    :stability: experimental
    '''
    APP_MESH = "APP_MESH"
    '''
    :stability: experimental
    '''
    APP_RUNNER = "APP_RUNNER"
    '''
    :stability: experimental
    '''
    APP_WIZARD = "APP_WIZARD"
    '''
    :stability: experimental
    '''
    ARCHIVE = "ARCHIVE"
    '''
    :stability: experimental
    '''
    ARTIFACT = "ARTIFACT"
    '''
    :stability: experimental
    '''
    AR_VR = "AR_VR"
    '''
    :stability: experimental
    '''
    ATHENA = "ATHENA"
    '''
    :stability: experimental
    '''
    ATTRIBUTE = "ATTRIBUTE"
    '''
    :stability: experimental
    '''
    ATTRIBUTES = "ATTRIBUTES"
    '''
    :stability: experimental
    '''
    AUDIT_MANAGER = "AUDIT_MANAGER"
    '''
    :stability: experimental
    '''
    AUGMENTED_AI = "AUGMENTED_AI"
    '''
    :stability: experimental
    '''
    AURORA = "AURORA"
    '''
    :stability: experimental
    '''
    AURORA_INSTANCE = "AURORA_INSTANCE"
    '''
    :stability: experimental
    '''
    AURORA_INSTANCE_ALT = "AURORA_INSTANCE_ALT"
    '''
    :stability: experimental
    '''
    AUTOMATION = "AUTOMATION"
    '''
    :stability: experimental
    '''
    AUTOSCALING = "AUTOSCALING"
    '''
    :stability: experimental
    '''
    AUTO_SCALING = "AUTO_SCALING"
    '''
    :stability: experimental
    '''
    AUTO_SCALING2 = "AUTO_SCALING2"
    '''
    :stability: experimental
    '''
    AUTO_SCALING3 = "AUTO_SCALING3"
    '''
    :stability: experimental
    '''
    AWS_CLOUD = "AWS_CLOUD"
    '''
    :stability: experimental
    '''
    BACKINT_AGENT = "BACKINT_AGENT"
    '''
    :stability: experimental
    '''
    BACKUP = "BACKUP"
    '''
    :stability: experimental
    '''
    BACKUP_AWS_BACKUP_SUPPORT_FOR_AMAZON_S3 = "BACKUP_AWS_BACKUP_SUPPORT_FOR_AMAZON_S3"
    '''
    :stability: experimental
    '''
    BACKUP_AWS_BACKUP_SUPPORT_FOR_VMWARE_WORKLOADS = "BACKUP_AWS_BACKUP_SUPPORT_FOR_VMWARE_WORKLOADS"
    '''
    :stability: experimental
    '''
    BACKUP_BACKUP_PLAN = "BACKUP_BACKUP_PLAN"
    '''
    :stability: experimental
    '''
    BACKUP_BACKUP_RESTORE = "BACKUP_BACKUP_RESTORE"
    '''
    :stability: experimental
    '''
    BACKUP_COMPLIANCE_REPORTING = "BACKUP_COMPLIANCE_REPORTING"
    '''
    :stability: experimental
    '''
    BACKUP_COMPUTE = "BACKUP_COMPUTE"
    '''
    :stability: experimental
    '''
    BACKUP_DATABASE = "BACKUP_DATABASE"
    '''
    :stability: experimental
    '''
    BACKUP_GATEWAY = "BACKUP_GATEWAY"
    '''
    :stability: experimental
    '''
    BACKUP_PLAN = "BACKUP_PLAN"
    '''
    :stability: experimental
    '''
    BACKUP_RECOVERY_POINT_OBJECTIVE = "BACKUP_RECOVERY_POINT_OBJECTIVE"
    '''
    :stability: experimental
    '''
    BACKUP_RECOVERY_TIME_OBJECTIVE = "BACKUP_RECOVERY_TIME_OBJECTIVE"
    '''
    :stability: experimental
    '''
    BACKUP_RESTORE = "BACKUP_RESTORE"
    '''
    :stability: experimental
    '''
    BACKUP_STORAGE = "BACKUP_STORAGE"
    '''
    :stability: experimental
    '''
    BACKUP_VAULT = "BACKUP_VAULT"
    '''
    :stability: experimental
    '''
    BACKUP_VIRTUAL_MACHINE = "BACKUP_VIRTUAL_MACHINE"
    '''
    :stability: experimental
    '''
    BACKUP_VIRTUAL_MACHINE_MONITOR = "BACKUP_VIRTUAL_MACHINE_MONITOR"
    '''
    :stability: experimental
    '''
    BANK = "BANK"
    '''
    :stability: experimental
    '''
    BATCH = "BATCH"
    '''
    :stability: experimental
    '''
    BLOCKCHAIN = "BLOCKCHAIN"
    '''
    :stability: experimental
    '''
    BLOCKCHAIN_RESOURCE = "BLOCKCHAIN_RESOURCE"
    '''
    :stability: experimental
    '''
    BOTTLEROCKET = "BOTTLEROCKET"
    '''
    :stability: experimental
    '''
    BRAKET = "BRAKET"
    '''
    :stability: experimental
    '''
    BRAKET_CHANDELIER = "BRAKET_CHANDELIER"
    '''
    :stability: experimental
    '''
    BRAKET_CHIP = "BRAKET_CHIP"
    '''
    :stability: experimental
    '''
    BRAKET_NOISE_SIMULATOR = "BRAKET_NOISE_SIMULATOR"
    '''
    :stability: experimental
    '''
    BRAKET_QPU = "BRAKET_QPU"
    '''
    :stability: experimental
    '''
    BRAKET_SIMULATOR = "BRAKET_SIMULATOR"
    '''
    :stability: experimental
    '''
    BRAKET_SIMULATOR_1 = "BRAKET_SIMULATOR_1"
    '''
    :stability: experimental
    '''
    BRAKET_SIMULATOR_2 = "BRAKET_SIMULATOR_2"
    '''
    :stability: experimental
    '''
    BRAKET_SIMULATOR_3 = "BRAKET_SIMULATOR_3"
    '''
    :stability: experimental
    '''
    BRAKET_SIMULATOR_4 = "BRAKET_SIMULATOR_4"
    '''
    :stability: experimental
    '''
    BRAKET_STATE_VECTOR = "BRAKET_STATE_VECTOR"
    '''
    :stability: experimental
    '''
    BRAKET_TENSOR_NETWORK = "BRAKET_TENSOR_NETWORK"
    '''
    :stability: experimental
    '''
    BUCKET = "BUCKET"
    '''
    :stability: experimental
    '''
    BUCKET_WITH_OBJECTS = "BUCKET_WITH_OBJECTS"
    '''
    :stability: experimental
    '''
    BUDGETS = "BUDGETS"
    '''
    :stability: experimental
    '''
    BUDGETS_2 = "BUDGETS_2"
    '''
    :stability: experimental
    '''
    BUSINESS_APPLICATION = "BUSINESS_APPLICATION"
    '''
    :stability: experimental
    '''
    BYCICLE = "BYCICLE"
    '''
    :stability: experimental
    '''
    C4_INSTANCE = "C4_INSTANCE"
    '''
    :stability: experimental
    '''
    C5A = "C5A"
    '''
    :stability: experimental
    '''
    C5AD = "C5AD"
    '''
    :stability: experimental
    '''
    C5D = "C5D"
    '''
    :stability: experimental
    '''
    C5N_INSTANCE = "C5N_INSTANCE"
    '''
    :stability: experimental
    '''
    C5_INSTANCE = "C5_INSTANCE"
    '''
    :stability: experimental
    '''
    C6GD = "C6GD"
    '''
    :stability: experimental
    '''
    C6G_INSTANCE = "C6G_INSTANCE"
    '''
    :stability: experimental
    '''
    CACHED_VOLUME = "CACHED_VOLUME"
    '''
    :stability: experimental
    '''
    CACHE_NODE = "CACHE_NODE"
    '''
    :stability: experimental
    '''
    CAMERA = "CAMERA"
    '''
    :stability: experimental
    '''
    CAMERA2 = "CAMERA2"
    '''
    :stability: experimental
    '''
    CAR = "CAR"
    '''
    :stability: experimental
    '''
    CART = "CART"
    '''
    :stability: experimental
    '''
    CERTIFICATE_MANAGER = "CERTIFICATE_MANAGER"
    '''
    :stability: experimental
    '''
    CERTIFICATE_MANAGER_2 = "CERTIFICATE_MANAGER_2"
    '''
    :stability: experimental
    '''
    CERTIFICATE_MANAGER_3 = "CERTIFICATE_MANAGER_3"
    '''
    :stability: experimental
    '''
    CHANGE_SET = "CHANGE_SET"
    '''
    :stability: experimental
    '''
    CHATBOT = "CHATBOT"
    '''
    :stability: experimental
    '''
    CHECKLIST = "CHECKLIST"
    '''
    :stability: experimental
    '''
    CHECKLIST_COST = "CHECKLIST_COST"
    '''
    :stability: experimental
    '''
    CHECKLIST_FAULT_TOLERANT = "CHECKLIST_FAULT_TOLERANT"
    '''
    :stability: experimental
    '''
    CHECKLIST_PERFORMANCE = "CHECKLIST_PERFORMANCE"
    '''
    :stability: experimental
    '''
    CHECKLIST_SECURITY = "CHECKLIST_SECURITY"
    '''
    :stability: experimental
    '''
    CHIME = "CHIME"
    '''
    :stability: experimental
    '''
    CHIME_SDK = "CHIME_SDK"
    '''
    :stability: experimental
    '''
    CLASSIC_LOAD_BALANCER = "CLASSIC_LOAD_BALANCER"
    '''
    :stability: experimental
    '''
    CLIENT = "CLIENT"
    '''
    :stability: experimental
    '''
    CLIENT_VPN = "CLIENT_VPN"
    '''
    :stability: experimental
    '''
    CLOUD9 = "CLOUD9"
    '''
    :stability: experimental
    '''
    CLOUDENDURE_DISASTER_RECOVERY = "CLOUDENDURE_DISASTER_RECOVERY"
    '''
    :stability: experimental
    '''
    CLOUDENDURE_MIGRATION = "CLOUDENDURE_MIGRATION"
    '''
    :stability: experimental
    '''
    CLOUDFORMATION = "CLOUDFORMATION"
    '''
    :stability: experimental
    '''
    CLOUDFRONT = "CLOUDFRONT"
    '''
    :stability: experimental
    '''
    CLOUDFRONT_FUNCTIONS = "CLOUDFRONT_FUNCTIONS"
    '''
    :stability: experimental
    '''
    CLOUDHSM = "CLOUDHSM"
    '''
    :stability: experimental
    '''
    CLOUDSEARCH = "CLOUDSEARCH"
    '''
    :stability: experimental
    '''
    CLOUDSEARCH2 = "CLOUDSEARCH2"
    '''
    :stability: experimental
    '''
    CLOUDSHELL = "CLOUDSHELL"
    '''
    :stability: experimental
    '''
    CLOUDTRAIL = "CLOUDTRAIL"
    '''
    :stability: experimental
    '''
    CLOUDWATCH = "CLOUDWATCH"
    '''
    :stability: experimental
    '''
    CLOUDWATCH_2 = "CLOUDWATCH_2"
    '''
    :stability: experimental
    '''
    CLOUDWATCH_EVIDENTLY = "CLOUDWATCH_EVIDENTLY"
    '''
    :stability: experimental
    '''
    CLOUDWATCH_METRICS_INSIGHTS = "CLOUDWATCH_METRICS_INSIGHTS"
    '''
    :stability: experimental
    '''
    CLOUDWATCH_RUM = "CLOUDWATCH_RUM"
    '''
    :stability: experimental
    '''
    CLOUDWATCH_SYNTHETICS = "CLOUDWATCH_SYNTHETICS"
    '''
    :stability: experimental
    '''
    CLOUD_CONTROL_API = "CLOUD_CONTROL_API"
    '''
    :stability: experimental
    '''
    CLOUD_DEVELOPMENT_KIT = "CLOUD_DEVELOPMENT_KIT"
    '''
    :stability: experimental
    '''
    CLOUD_DIGITAL_INTERFACE = "CLOUD_DIGITAL_INTERFACE"
    '''
    :stability: experimental
    '''
    CLOUD_DIRECTORY = "CLOUD_DIRECTORY"
    '''
    :stability: experimental
    '''
    CLOUD_EXTENSION_ROS = "CLOUD_EXTENSION_ROS"
    '''
    :stability: experimental
    '''
    CLOUD_MAP = "CLOUD_MAP"
    '''
    :stability: experimental
    '''
    CLOUD_MAP_RESOURCE = "CLOUD_MAP_RESOURCE"
    '''
    :stability: experimental
    '''
    CLOUD_WAN = "CLOUD_WAN"
    '''
    :stability: experimental
    '''
    CLOUD_WAN_SEGMENT_NETWORK = "CLOUD_WAN_SEGMENT_NETWORK"
    '''
    :stability: experimental
    '''
    CLOUD_WAN_VIRTUAL_POP = "CLOUD_WAN_VIRTUAL_POP"
    '''
    :stability: experimental
    '''
    CLUSTER = "CLUSTER"
    '''
    :stability: experimental
    '''
    CODEARTIFACT = "CODEARTIFACT"
    '''
    :stability: experimental
    '''
    CODEBUILD = "CODEBUILD"
    '''
    :stability: experimental
    '''
    CODECOMMIT = "CODECOMMIT"
    '''
    :stability: experimental
    '''
    CODEDEPLOY = "CODEDEPLOY"
    '''
    :stability: experimental
    '''
    CODEGURU = "CODEGURU"
    '''
    :stability: experimental
    '''
    CODEGURU_2 = "CODEGURU_2"
    '''
    :stability: experimental
    '''
    CODEPIPELINE = "CODEPIPELINE"
    '''
    :stability: experimental
    '''
    CODESTAR = "CODESTAR"
    '''
    :stability: experimental
    '''
    COFFEE_POT = "COFFEE_POT"
    '''
    :stability: experimental
    '''
    COGNITO = "COGNITO"
    '''
    :stability: experimental
    '''
    COMMAND_LINE_INTERFACE = "COMMAND_LINE_INTERFACE"
    '''
    :stability: experimental
    '''
    COMPREHEND = "COMPREHEND"
    '''
    :stability: experimental
    '''
    COMPREHEND_MEDICAL = "COMPREHEND_MEDICAL"
    '''
    :stability: experimental
    '''
    COMPUTE = "COMPUTE"
    '''
    :stability: experimental
    '''
    COMPUTE_OPTIMIZER = "COMPUTE_OPTIMIZER"
    '''
    :stability: experimental
    '''
    CONFIG = "CONFIG"
    '''
    :stability: experimental
    '''
    CONNECT = "CONNECT"
    '''
    :stability: experimental
    '''
    CONNECTOR = "CONNECTOR"
    '''
    :stability: experimental
    '''
    CONTAINERS = "CONTAINERS"
    '''
    :stability: experimental
    '''
    CONTAINER_1 = "CONTAINER_1"
    '''
    :stability: experimental
    '''
    CONTAINER_2 = "CONTAINER_2"
    '''
    :stability: experimental
    '''
    CONTAINER_3 = "CONTAINER_3"
    '''
    :stability: experimental
    '''
    CONTAINER_REGISTRY_IMAGE = "CONTAINER_REGISTRY_IMAGE"
    '''
    :stability: experimental
    '''
    CONTROL_TOWER = "CONTROL_TOWER"
    '''
    :stability: experimental
    '''
    CORPORATE_DATA_CENTER = "CORPORATE_DATA_CENTER"
    '''
    :stability: experimental
    '''
    CORPORATE_DATA_CENTER2 = "CORPORATE_DATA_CENTER2"
    '''
    :stability: experimental
    '''
    CORRETTO = "CORRETTO"
    '''
    :stability: experimental
    '''
    COST_AND_USAGE_REPORT = "COST_AND_USAGE_REPORT"
    '''
    :stability: experimental
    '''
    COST_EXPLORER = "COST_EXPLORER"
    '''
    :stability: experimental
    '''
    COST_MANAGEMENT = "COST_MANAGEMENT"
    '''
    :stability: experimental
    '''
    CUSTOMER_ENABLEMENT = "CUSTOMER_ENABLEMENT"
    '''
    :stability: experimental
    '''
    CUSTOMER_ENGAGEMENT = "CUSTOMER_ENGAGEMENT"
    '''
    :stability: experimental
    '''
    CUSTOMER_GATEWAY = "CUSTOMER_GATEWAY"
    '''
    :stability: experimental
    '''
    CUSTOM_BILLING_MANAGER = "CUSTOM_BILLING_MANAGER"
    '''
    :stability: experimental
    '''
    CUSTOM_EVENT_BUS_RESOURCE = "CUSTOM_EVENT_BUS_RESOURCE"
    '''
    :stability: experimental
    '''
    D2_INSTANCE = "D2_INSTANCE"
    '''
    :stability: experimental
    '''
    D3EN_INSTANCE = "D3EN_INSTANCE"
    '''
    :stability: experimental
    '''
    D3_INSTANCE = "D3_INSTANCE"
    '''
    :stability: experimental
    '''
    DATABASE = "DATABASE"
    '''
    :stability: experimental
    '''
    DATABASE_MIGRATION_SERVICE = "DATABASE_MIGRATION_SERVICE"
    '''
    :stability: experimental
    '''
    DATABASE_MIGRATION_WORKFLOW_JOB = "DATABASE_MIGRATION_WORKFLOW_JOB"
    '''
    :stability: experimental
    '''
    DATASYNC = "DATASYNC"
    '''
    :stability: experimental
    '''
    DATA_ENCRYPTION_KEY = "DATA_ENCRYPTION_KEY"
    '''
    :stability: experimental
    '''
    DATA_EXCHANGE = "DATA_EXCHANGE"
    '''
    :stability: experimental
    '''
    DATA_EXCHANGE_FOR_APIS = "DATA_EXCHANGE_FOR_APIS"
    '''
    :stability: experimental
    '''
    DATA_LAKE_RESOURCE_ICON = "DATA_LAKE_RESOURCE_ICON"
    '''
    :stability: experimental
    '''
    DATA_PIPELINE = "DATA_PIPELINE"
    '''
    :stability: experimental
    '''
    DATA_SET = "DATA_SET"
    '''
    :stability: experimental
    '''
    DB_INSTANCE = "DB_INSTANCE"
    '''
    :stability: experimental
    '''
    DB_INSTANCE_READ_REPLICA = "DB_INSTANCE_READ_REPLICA"
    '''
    :stability: experimental
    '''
    DB_INSTANCE_STANDBY = "DB_INSTANCE_STANDBY"
    '''
    :stability: experimental
    '''
    DB_ON_INSTANCE = "DB_ON_INSTANCE"
    '''
    :stability: experimental
    '''
    DB_ON_INSTANCE2 = "DB_ON_INSTANCE2"
    '''
    :stability: experimental
    '''
    DEEPCOMPOSER = "DEEPCOMPOSER"
    '''
    :stability: experimental
    '''
    DEEPLENS = "DEEPLENS"
    '''
    :stability: experimental
    '''
    DEEPRACER = "DEEPRACER"
    '''
    :stability: experimental
    '''
    DEEP_LEARNING_AMIS = "DEEP_LEARNING_AMIS"
    '''
    :stability: experimental
    '''
    DEEP_LEARNING_CONTAINERS = "DEEP_LEARNING_CONTAINERS"
    '''
    :stability: experimental
    '''
    DEFAULT_EVENT_BUS_RESOURCE = "DEFAULT_EVENT_BUS_RESOURCE"
    '''
    :stability: experimental
    '''
    DENSE_COMPUTE_NODE = "DENSE_COMPUTE_NODE"
    '''
    :stability: experimental
    '''
    DENSE_STORAGE_NODE = "DENSE_STORAGE_NODE"
    '''
    :stability: experimental
    '''
    DEPLOYMENT = "DEPLOYMENT"
    '''
    :stability: experimental
    '''
    DEPLOYMENTS = "DEPLOYMENTS"
    '''
    :stability: experimental
    '''
    DESIRED_STATE = "DESIRED_STATE"
    '''
    :stability: experimental
    '''
    DESKTOP_AND_APP_STREAMING = "DESKTOP_AND_APP_STREAMING"
    '''
    :stability: experimental
    '''
    DETECTIVE = "DETECTIVE"
    '''
    :stability: experimental
    '''
    DEVELOPER_TOOLS = "DEVELOPER_TOOLS"
    '''
    :stability: experimental
    '''
    DEVELOPMENT_ENVIRONMENT = "DEVELOPMENT_ENVIRONMENT"
    '''
    :stability: experimental
    '''
    DEVICE_FARM = "DEVICE_FARM"
    '''
    :stability: experimental
    '''
    DEVOPS_GURU = "DEVOPS_GURU"
    '''
    :stability: experimental
    '''
    DEVOPS_GURU_INSIGHTS = "DEVOPS_GURU_INSIGHTS"
    '''
    :stability: experimental
    '''
    DIRECTORY_SERVICE = "DIRECTORY_SERVICE"
    '''
    :stability: experimental
    '''
    DIRECT_CONNECT = "DIRECT_CONNECT"
    '''
    :stability: experimental
    '''
    DISK = "DISK"
    '''
    :stability: experimental
    '''
    DISTRO_FOR_OPENTELEMETRY = "DISTRO_FOR_OPENTELEMETRY"
    '''
    :stability: experimental
    '''
    DOCUMENTDB_WITH_MONGODB_COMPATIBILITY = "DOCUMENTDB_WITH_MONGODB_COMPATIBILITY"
    '''
    :stability: experimental
    '''
    DOCUMENTS = "DOCUMENTS"
    '''
    :stability: experimental
    '''
    DOCUMENTS2 = "DOCUMENTS2"
    '''
    :stability: experimental
    '''
    DOOR_LOCK = "DOOR_LOCK"
    '''
    :stability: experimental
    '''
    DOWNLOAD_DISTRIBUTION = "DOWNLOAD_DISTRIBUTION"
    '''
    :stability: experimental
    '''
    DYNAMODB = "DYNAMODB"
    '''
    :stability: experimental
    '''
    DYNAMODB_DAX = "DYNAMODB_DAX"
    '''
    :stability: experimental
    '''
    DYNAMODB_STANDARD_ACCESS_TABLE_CLASS = "DYNAMODB_STANDARD_ACCESS_TABLE_CLASS"
    '''
    :stability: experimental
    '''
    DYNAMODB_STANDARD_INFREQUENT_ACCESS_TABLE_CLASS = "DYNAMODB_STANDARD_INFREQUENT_ACCESS_TABLE_CLASS"
    '''
    :stability: experimental
    '''
    DYNAMODB_STREAM = "DYNAMODB_STREAM"
    '''
    :stability: experimental
    '''
    EC2 = "EC2"
    '''
    :stability: experimental
    '''
    EC2_AWS_MICROSERVICE_EXTRACTOR_FOR_NET = "EC2_AWS_MICROSERVICE_EXTRACTOR_FOR_NET"
    '''
    :stability: experimental
    '''
    EC2_C6A_INSTANCE = "EC2_C6A_INSTANCE"
    '''
    :stability: experimental
    '''
    EC2_C6GN_INSTANCE = "EC2_C6GN_INSTANCE"
    '''
    :stability: experimental
    '''
    EC2_C6I_INSTANCE = "EC2_C6I_INSTANCE"
    '''
    :stability: experimental
    '''
    EC2_C7G_INSTANCE = "EC2_C7G_INSTANCE"
    '''
    :stability: experimental
    '''
    EC2_DL1_INSTANCE = "EC2_DL1_INSTANCE"
    '''
    :stability: experimental
    '''
    EC2_G5G_INSTANCE = "EC2_G5G_INSTANCE"
    '''
    :stability: experimental
    '''
    EC2_G5_INSTANCE = "EC2_G5_INSTANCE"
    '''
    :stability: experimental
    '''
    EC2_HPC6A_INSTANCE = "EC2_HPC6A_INSTANCE"
    '''
    :stability: experimental
    '''
    EC2_I4I_INSTANCE = "EC2_I4I_INSTANCE"
    '''
    :stability: experimental
    '''
    EC2_IM4GN_INSTANCE = "EC2_IM4GN_INSTANCE"
    '''
    :stability: experimental
    '''
    EC2_IMAGE_BUILDER = "EC2_IMAGE_BUILDER"
    '''
    :stability: experimental
    '''
    EC2_INSTANCE_CONTENTS = "EC2_INSTANCE_CONTENTS"
    '''
    :stability: experimental
    '''
    EC2_IS4GEN_INSTANCE = "EC2_IS4GEN_INSTANCE"
    '''
    :stability: experimental
    '''
    EC2_M1_MAC_INSTANCE = "EC2_M1_MAC_INSTANCE"
    '''
    :stability: experimental
    '''
    EC2_M6A_INSTANCE = "EC2_M6A_INSTANCE"
    '''
    :stability: experimental
    '''
    EC2_M6I_INSTANCE = "EC2_M6I_INSTANCE"
    '''
    :stability: experimental
    '''
    EC2_R6I_INSTANCE = "EC2_R6I_INSTANCE"
    '''
    :stability: experimental
    '''
    EC2_TRN1_INSTANCE = "EC2_TRN1_INSTANCE"
    '''
    :stability: experimental
    '''
    EC2_VT1_INSTANCE = "EC2_VT1_INSTANCE"
    '''
    :stability: experimental
    '''
    EC2_X2GD_INSTANCE = "EC2_X2GD_INSTANCE"
    '''
    :stability: experimental
    '''
    EC2_X2IDN_INSTANCE = "EC2_X2IDN_INSTANCE"
    '''
    :stability: experimental
    '''
    EC2_X2IEDN_INSTANCE = "EC2_X2IEDN_INSTANCE"
    '''
    :stability: experimental
    '''
    EC2_X2IEZN_INSTANCE = "EC2_X2IEZN_INSTANCE"
    '''
    :stability: experimental
    '''
    ECHO = "ECHO"
    '''
    :stability: experimental
    '''
    ECR = "ECR"
    '''
    :stability: experimental
    '''
    ECS = "ECS"
    '''
    :stability: experimental
    '''
    ECS_ANYWHERE = "ECS_ANYWHERE"
    '''
    :stability: experimental
    '''
    ECS_COPILOT_CLI = "ECS_COPILOT_CLI"
    '''
    :stability: experimental
    '''
    ECS_SERVICE = "ECS_SERVICE"
    '''
    :stability: experimental
    '''
    ECS_TASK = "ECS_TASK"
    '''
    :stability: experimental
    '''
    EDGE_LOCATION = "EDGE_LOCATION"
    '''
    :stability: experimental
    '''
    EFS_INFREQUENTACCESS = "EFS_INFREQUENTACCESS"
    '''
    :stability: experimental
    '''
    EFS_STANDARD = "EFS_STANDARD"
    '''
    :stability: experimental
    '''
    EKS = "EKS"
    '''
    :stability: experimental
    '''
    EKS_ANYWHERE = "EKS_ANYWHERE"
    '''
    :stability: experimental
    '''
    EKS_CLOUD = "EKS_CLOUD"
    '''
    :stability: experimental
    '''
    EKS_DISTRO = "EKS_DISTRO"
    '''
    :stability: experimental
    '''
    ELASTICACHE = "ELASTICACHE"
    '''
    :stability: experimental
    '''
    ELASTICACHE_FOR_MEMCACHED = "ELASTICACHE_FOR_MEMCACHED"
    '''
    :stability: experimental
    '''
    ELASTICACHE_FOR_REDIS = "ELASTICACHE_FOR_REDIS"
    '''
    :stability: experimental
    '''
    ELASTICSEARCH_SERVICE = "ELASTICSEARCH_SERVICE"
    '''
    :stability: experimental
    '''
    ELASTIC_BEANSTALK = "ELASTIC_BEANSTALK"
    '''
    :stability: experimental
    '''
    ELASTIC_BLOCK_STORE = "ELASTIC_BLOCK_STORE"
    '''
    :stability: experimental
    '''
    ELASTIC_BLOCK_STORE_AMAZON_DATA_LIFECYCLE_MANAGER = "ELASTIC_BLOCK_STORE_AMAZON_DATA_LIFECYCLE_MANAGER"
    '''
    :stability: experimental
    '''
    ELASTIC_BLOCK_STORE_VOLUME_GP3 = "ELASTIC_BLOCK_STORE_VOLUME_GP3"
    '''
    :stability: experimental
    '''
    ELASTIC_FABRIC_ADAPTER = "ELASTIC_FABRIC_ADAPTER"
    '''
    :stability: experimental
    '''
    ELASTIC_FILE_SYSTEM = "ELASTIC_FILE_SYSTEM"
    '''
    :stability: experimental
    '''
    ELASTIC_FILE_SYSTEM_INFREQUENT_ACCESS = "ELASTIC_FILE_SYSTEM_INFREQUENT_ACCESS"
    '''
    :stability: experimental
    '''
    ELASTIC_FILE_SYSTEM_INTELLIGENT_TIERING = "ELASTIC_FILE_SYSTEM_INTELLIGENT_TIERING"
    '''
    :stability: experimental
    '''
    ELASTIC_FILE_SYSTEM_ONE_ZONE = "ELASTIC_FILE_SYSTEM_ONE_ZONE"
    '''
    :stability: experimental
    '''
    ELASTIC_FILE_SYSTEM_ONE_ZONE_INFREQUENT_ACCESS = "ELASTIC_FILE_SYSTEM_ONE_ZONE_INFREQUENT_ACCESS"
    '''
    :stability: experimental
    '''
    ELASTIC_FILE_SYSTEM_ONE_ZONE_STANDARD = "ELASTIC_FILE_SYSTEM_ONE_ZONE_STANDARD"
    '''
    :stability: experimental
    '''
    ELASTIC_FILE_SYSTEM_STANDARD = "ELASTIC_FILE_SYSTEM_STANDARD"
    '''
    :stability: experimental
    '''
    ELASTIC_FILE_SYSTEM_STANDARD_INFREQUENT_ACCESS = "ELASTIC_FILE_SYSTEM_STANDARD_INFREQUENT_ACCESS"
    '''
    :stability: experimental
    '''
    ELASTIC_INFERENCE = "ELASTIC_INFERENCE"
    '''
    :stability: experimental
    '''
    ELASTIC_INFERENCE_2 = "ELASTIC_INFERENCE_2"
    '''
    :stability: experimental
    '''
    ELASTIC_IP_ADDRESS = "ELASTIC_IP_ADDRESS"
    '''
    :stability: experimental
    '''
    ELASTIC_LOAD_BALANCING = "ELASTIC_LOAD_BALANCING"
    '''
    :stability: experimental
    '''
    ELASTIC_NETWORK_ADAPTER = "ELASTIC_NETWORK_ADAPTER"
    '''
    :stability: experimental
    '''
    ELASTIC_NETWORK_INTERFACE = "ELASTIC_NETWORK_INTERFACE"
    '''
    :stability: experimental
    '''
    ELASTIC_TRANSCODER = "ELASTIC_TRANSCODER"
    '''
    :stability: experimental
    '''
    ELEMENTAL = "ELEMENTAL"
    '''
    :stability: experimental
    '''
    ELEMENTAL_LINK = "ELEMENTAL_LINK"
    '''
    :stability: experimental
    '''
    ELEMENTAL_MEDIACONNECT = "ELEMENTAL_MEDIACONNECT"
    '''
    :stability: experimental
    '''
    ELEMENTAL_MEDIACONVERT = "ELEMENTAL_MEDIACONVERT"
    '''
    :stability: experimental
    '''
    ELEMENTAL_MEDIALIVE = "ELEMENTAL_MEDIALIVE"
    '''
    :stability: experimental
    '''
    ELEMENTAL_MEDIAPACKAGE = "ELEMENTAL_MEDIAPACKAGE"
    '''
    :stability: experimental
    '''
    ELEMENTAL_MEDIASTORE = "ELEMENTAL_MEDIASTORE"
    '''
    :stability: experimental
    '''
    ELEMENTAL_MEDIATAILOR = "ELEMENTAL_MEDIATAILOR"
    '''
    :stability: experimental
    '''
    EMAIL = "EMAIL"
    '''
    :stability: experimental
    '''
    EMAIL_2 = "EMAIL_2"
    '''
    :stability: experimental
    '''
    EMAIL_NOTIFICATION = "EMAIL_NOTIFICATION"
    '''
    :stability: experimental
    '''
    EMR = "EMR"
    '''
    :stability: experimental
    '''
    EMR_ENGINE = "EMR_ENGINE"
    '''
    :stability: experimental
    '''
    EMR_ENGINE_MAPR_M3 = "EMR_ENGINE_MAPR_M3"
    '''
    :stability: experimental
    '''
    EMR_ENGINE_MAPR_M5 = "EMR_ENGINE_MAPR_M5"
    '''
    :stability: experimental
    '''
    EMR_ENGINE_MAPR_M7 = "EMR_ENGINE_MAPR_M7"
    '''
    :stability: experimental
    '''
    ENCRYPTED_DATA = "ENCRYPTED_DATA"
    '''
    :stability: experimental
    '''
    ENDPOINT = "ENDPOINT"
    '''
    :stability: experimental
    '''
    ENDPOINTS = "ENDPOINTS"
    '''
    :stability: experimental
    '''
    EVENT = "EVENT"
    '''
    :stability: experimental
    '''
    EVENTBRIDGE = "EVENTBRIDGE"
    '''
    :stability: experimental
    '''
    EVENTBRIDGE_CUSTOM_EVENT_BUS_RESOURCE = "EVENTBRIDGE_CUSTOM_EVENT_BUS_RESOURCE"
    '''
    :stability: experimental
    '''
    EVENTBRIDGE_DEFAULT_EVENT_BUS_RESOURCE = "EVENTBRIDGE_DEFAULT_EVENT_BUS_RESOURCE"
    '''
    :stability: experimental
    '''
    EVENTBRIDGE_SAAS_PARTNER_EVENT_BUS_RESOURCE = "EVENTBRIDGE_SAAS_PARTNER_EVENT_BUS_RESOURCE"
    '''
    :stability: experimental
    '''
    EVENTBRIDGE_SCHEMA = "EVENTBRIDGE_SCHEMA"
    '''
    :stability: experimental
    '''
    EVENTBRIDGE_SCHEMA_REGISTRY = "EVENTBRIDGE_SCHEMA_REGISTRY"
    '''
    :stability: experimental
    '''
    EVENT_EVENT_BASED = "EVENT_EVENT_BASED"
    '''
    :stability: experimental
    '''
    EVENT_RESOURCE = "EVENT_RESOURCE"
    '''
    :stability: experimental
    '''
    EVENT_TIME_BASED = "EVENT_TIME_BASED"
    '''
    :stability: experimental
    '''
    EXPRESS_WORKFLOW = "EXPRESS_WORKFLOW"
    '''
    :stability: experimental
    '''
    EXTERNAL_SDK = "EXTERNAL_SDK"
    '''
    :stability: experimental
    '''
    EXTERNAL_TOOLKIT = "EXTERNAL_TOOLKIT"
    '''
    :stability: experimental
    '''
    F1_INSTANCE = "F1_INSTANCE"
    '''
    :stability: experimental
    '''
    FACTORY = "FACTORY"
    '''
    :stability: experimental
    '''
    FARGATE = "FARGATE"
    '''
    :stability: experimental
    '''
    FAULT_INJECTION_SIMULATOR = "FAULT_INJECTION_SIMULATOR"
    '''
    :stability: experimental
    '''
    FILE_GATEWAY = "FILE_GATEWAY"
    '''
    :stability: experimental
    '''
    FILE_SYSTEM = "FILE_SYSTEM"
    '''
    :stability: experimental
    '''
    FILTERING_RULE = "FILTERING_RULE"
    '''
    :stability: experimental
    '''
    FINDING = "FINDING"
    '''
    :stability: experimental
    '''
    FINSPACE = "FINSPACE"
    '''
    :stability: experimental
    '''
    FIRETV = "FIRETV"
    '''
    :stability: experimental
    '''
    FIRETV_STICK = "FIRETV_STICK"
    '''
    :stability: experimental
    '''
    FIREWALL_MANAGER = "FIREWALL_MANAGER"
    '''
    :stability: experimental
    '''
    FLEET_MANAGEMENT = "FLEET_MANAGEMENT"
    '''
    :stability: experimental
    '''
    FLOW_LOGS = "FLOW_LOGS"
    '''
    :stability: experimental
    '''
    FORECAST = "FORECAST"
    '''
    :stability: experimental
    '''
    FORUMS = "FORUMS"
    '''
    :stability: experimental
    '''
    FRAUD_DETECTOR = "FRAUD_DETECTOR"
    '''
    :stability: experimental
    '''
    FREERTOS = "FREERTOS"
    '''
    :stability: experimental
    '''
    FSX = "FSX"
    '''
    :stability: experimental
    '''
    FSX_FILE_GATEWAY = "FSX_FILE_GATEWAY"
    '''
    :stability: experimental
    '''
    FSX_FOR_LUSTRE = "FSX_FOR_LUSTRE"
    '''
    :stability: experimental
    '''
    FSX_FOR_NETAPP_ONTAP = "FSX_FOR_NETAPP_ONTAP"
    '''
    :stability: experimental
    '''
    FSX_FOR_OPENZFS = "FSX_FOR_OPENZFS"
    '''
    :stability: experimental
    '''
    FSX_FOR_WINDOWS_FILE_SERVER = "FSX_FOR_WINDOWS_FILE_SERVER"
    '''
    :stability: experimental
    '''
    G3_INSTANCE = "G3_INSTANCE"
    '''
    :stability: experimental
    '''
    G4AD_INSTANCE = "G4AD_INSTANCE"
    '''
    :stability: experimental
    '''
    G4DN = "G4DN"
    '''
    :stability: experimental
    '''
    GAMEKIT = "GAMEKIT"
    '''
    :stability: experimental
    '''
    GAMELIFT = "GAMELIFT"
    '''
    :stability: experimental
    '''
    GAMESPARKS = "GAMESPARKS"
    '''
    :stability: experimental
    '''
    GAME_TECH = "GAME_TECH"
    '''
    :stability: experimental
    '''
    GAME_TECH2 = "GAME_TECH2"
    '''
    :stability: experimental
    '''
    GATEWAY = "GATEWAY"
    '''
    :stability: experimental
    '''
    GATEWAY_LOAD_BALANCER = "GATEWAY_LOAD_BALANCER"
    '''
    :stability: experimental
    '''
    GEAR = "GEAR"
    '''
    :stability: experimental
    '''
    GENERAL = "GENERAL"
    '''
    :stability: experimental
    '''
    GENERAL_ACCESS_POINTS = "GENERAL_ACCESS_POINTS"
    '''
    :stability: experimental
    '''
    GENERIC = "GENERIC"
    '''
    :stability: experimental
    '''
    GENERIC_DATABASE = "GENERIC_DATABASE"
    '''
    :stability: experimental
    '''
    GENERIC_FIREWALL = "GENERIC_FIREWALL"
    '''
    :stability: experimental
    '''
    GENOMICS_CLI = "GENOMICS_CLI"
    '''
    :stability: experimental
    '''
    GLACIER = "GLACIER"
    '''
    :stability: experimental
    '''
    GLACIER_DEEP_ARCHIVE = "GLACIER_DEEP_ARCHIVE"
    '''
    :stability: experimental
    '''
    GLOBAL_ACCELERATOR = "GLOBAL_ACCELERATOR"
    '''
    :stability: experimental
    '''
    GLOBAL_SECONDARY_INDEX = "GLOBAL_SECONDARY_INDEX"
    '''
    :stability: experimental
    '''
    GLUE = "GLUE"
    '''
    :stability: experimental
    '''
    GLUE_CRAWLERS = "GLUE_CRAWLERS"
    '''
    :stability: experimental
    '''
    GLUE_DATABREW = "GLUE_DATABREW"
    '''
    :stability: experimental
    '''
    GLUE_DATA_CATALOG = "GLUE_DATA_CATALOG"
    '''
    :stability: experimental
    '''
    GLUE_ELASTIC_VIEWS = "GLUE_ELASTIC_VIEWS"
    '''
    :stability: experimental
    '''
    GREENGRASS = "GREENGRASS"
    '''
    :stability: experimental
    '''
    GROUND_STATION = "GROUND_STATION"
    '''
    :stability: experimental
    '''
    GROUP_ACCOUNT = "GROUP_ACCOUNT"
    '''
    :stability: experimental
    '''
    GROUP_AUTO_SCALING_GROUP = "GROUP_AUTO_SCALING_GROUP"
    '''
    :stability: experimental
    '''
    GROUP_AVAILABILITY_ZONE = "GROUP_AVAILABILITY_ZONE"
    '''
    :stability: experimental
    '''
    GROUP_AWS_CLOUD = "GROUP_AWS_CLOUD"
    '''
    :stability: experimental
    '''
    GROUP_AWS_CLOUD_ALT = "GROUP_AWS_CLOUD_ALT"
    '''
    :stability: experimental
    '''
    GROUP_AWS_STEP_FUNCTIONS_WORKFLOW = "GROUP_AWS_STEP_FUNCTIONS_WORKFLOW"
    '''
    :stability: experimental
    '''
    GROUP_CORPORATE_DATA_CENTER = "GROUP_CORPORATE_DATA_CENTER"
    '''
    :stability: experimental
    '''
    GROUP_EC2_INSTANCE_CONTENTS = "GROUP_EC2_INSTANCE_CONTENTS"
    '''
    :stability: experimental
    '''
    GROUP_ELASTIC_BEANSTALK = "GROUP_ELASTIC_BEANSTALK"
    '''
    :stability: experimental
    '''
    GROUP_ELASTIC_LOAD_BALANCING = "GROUP_ELASTIC_LOAD_BALANCING"
    '''
    :stability: experimental
    '''
    GROUP_IOT_GREENGRASS = "GROUP_IOT_GREENGRASS"
    '''
    :stability: experimental
    '''
    GROUP_IOT_GREENGRASS_DEPLOYMENT = "GROUP_IOT_GREENGRASS_DEPLOYMENT"
    '''
    :stability: experimental
    '''
    GROUP_ON_PREMISE = "GROUP_ON_PREMISE"
    '''
    :stability: experimental
    '''
    GROUP_REGION = "GROUP_REGION"
    '''
    :stability: experimental
    '''
    GROUP_SECURITY_GROUP = "GROUP_SECURITY_GROUP"
    '''
    :stability: experimental
    '''
    GROUP_SPOT_FLEET = "GROUP_SPOT_FLEET"
    '''
    :stability: experimental
    '''
    GROUP_SUBNET = "GROUP_SUBNET"
    '''
    :stability: experimental
    '''
    GROUP_VPC = "GROUP_VPC"
    '''
    :stability: experimental
    '''
    GUARDDUTY = "GUARDDUTY"
    '''
    :stability: experimental
    '''
    H1_INSTANCE = "H1_INSTANCE"
    '''
    :stability: experimental
    '''
    HABANA_GAUDI = "HABANA_GAUDI"
    '''
    :stability: experimental
    '''
    HARDWARE_BOARD = "HARDWARE_BOARD"
    '''
    :stability: experimental
    '''
    HDFS_CLUSTER = "HDFS_CLUSTER"
    '''
    :stability: experimental
    '''
    HEALTHLAKE = "HEALTHLAKE"
    '''
    :stability: experimental
    '''
    HIGH_MEMORY_INSTANCE = "HIGH_MEMORY_INSTANCE"
    '''
    :stability: experimental
    '''
    HONEYCODE = "HONEYCODE"
    '''
    :stability: experimental
    '''
    HOSTED_ZONE = "HOSTED_ZONE"
    '''
    :stability: experimental
    '''
    HOUSE = "HOUSE"
    '''
    :stability: experimental
    '''
    HTTP2_PROTOCOL = "HTTP2_PROTOCOL"
    '''
    :stability: experimental
    '''
    HTTP_NOTIFICATION = "HTTP_NOTIFICATION"
    '''
    :stability: experimental
    '''
    HTTP_PROTOCOL = "HTTP_PROTOCOL"
    '''
    :stability: experimental
    '''
    I2 = "I2"
    '''
    :stability: experimental
    '''
    I3EN = "I3EN"
    '''
    :stability: experimental
    '''
    I3_INSTANCE = "I3_INSTANCE"
    '''
    :stability: experimental
    '''
    IDENTITY_AND_ACCESS_MANAGEMENT = "IDENTITY_AND_ACCESS_MANAGEMENT"
    '''
    :stability: experimental
    '''
    ILLUSTRATION_DESKTOP = "ILLUSTRATION_DESKTOP"
    '''
    :stability: experimental
    '''
    ILLUSTRATION_DEVICES = "ILLUSTRATION_DEVICES"
    '''
    :stability: experimental
    '''
    ILLUSTRATION_NOTIFICATION = "ILLUSTRATION_NOTIFICATION"
    '''
    :stability: experimental
    '''
    ILLUSTRATION_OFFICE_BUILDING = "ILLUSTRATION_OFFICE_BUILDING"
    '''
    :stability: experimental
    '''
    ILLUSTRATION_USERS = "ILLUSTRATION_USERS"
    '''
    :stability: experimental
    '''
    IMPORT_EXPORT = "IMPORT_EXPORT"
    '''
    :stability: experimental
    '''
    INF1 = "INF1"
    '''
    :stability: experimental
    '''
    INFERENTIA = "INFERENTIA"
    '''
    :stability: experimental
    '''
    INFREQUENT_ACCESS_STORAGE_CLASS = "INFREQUENT_ACCESS_STORAGE_CLASS"
    '''
    :stability: experimental
    '''
    INSPECTOR = "INSPECTOR"
    '''
    :stability: experimental
    '''
    INSTANCE = "INSTANCE"
    '''
    :stability: experimental
    '''
    INSTANCE2 = "INSTANCE2"
    '''
    :stability: experimental
    '''
    INSTANCES = "INSTANCES"
    '''
    :stability: experimental
    '''
    INSTANCES_2 = "INSTANCES_2"
    '''
    :stability: experimental
    '''
    INSTANCE_WITH_CLOUDWATCH = "INSTANCE_WITH_CLOUDWATCH"
    '''
    :stability: experimental
    '''
    INSTANCE_WITH_CLOUDWATCH2 = "INSTANCE_WITH_CLOUDWATCH2"
    '''
    :stability: experimental
    '''
    INTELLIGENT_TIERING = "INTELLIGENT_TIERING"
    '''
    :stability: experimental
    '''
    INTERACTIVE_VIDEO = "INTERACTIVE_VIDEO"
    '''
    :stability: experimental
    '''
    INTERNET = "INTERNET"
    '''
    :stability: experimental
    '''
    INTERNET_ALT1 = "INTERNET_ALT1"
    '''
    :stability: experimental
    '''
    INTERNET_ALT2 = "INTERNET_ALT2"
    '''
    :stability: experimental
    '''
    INTERNET_ALT22 = "INTERNET_ALT22"
    '''
    :stability: experimental
    '''
    INTERNET_GATEWAY = "INTERNET_GATEWAY"
    '''
    :stability: experimental
    '''
    INTERNET_OF_THINGS = "INTERNET_OF_THINGS"
    '''
    :stability: experimental
    '''
    INVENTORY = "INVENTORY"
    '''
    :stability: experimental
    '''
    IOT_1CLICK = "IOT_1CLICK"
    '''
    :stability: experimental
    '''
    IOT_ANALYTICS = "IOT_ANALYTICS"
    '''
    :stability: experimental
    '''
    IOT_ANALYTICS_CHANNEL = "IOT_ANALYTICS_CHANNEL"
    '''
    :stability: experimental
    '''
    IOT_ANALYTICS_DATA_STORE = "IOT_ANALYTICS_DATA_STORE"
    '''
    :stability: experimental
    '''
    IOT_ANALYTICS_PIPELINE = "IOT_ANALYTICS_PIPELINE"
    '''
    :stability: experimental
    '''
    IOT_BUTTON = "IOT_BUTTON"
    '''
    :stability: experimental
    '''
    IOT_CORE = "IOT_CORE"
    '''
    :stability: experimental
    '''
    IOT_DEVICE_DEFENDER = "IOT_DEVICE_DEFENDER"
    '''
    :stability: experimental
    '''
    IOT_DEVICE_DEFENDER_IOT_DEVICE_JOBS = "IOT_DEVICE_DEFENDER_IOT_DEVICE_JOBS"
    '''
    :stability: experimental
    '''
    IOT_DEVICE_GATEWAY = "IOT_DEVICE_GATEWAY"
    '''
    :stability: experimental
    '''
    IOT_DEVICE_JOBS_RESOURCE = "IOT_DEVICE_JOBS_RESOURCE"
    '''
    :stability: experimental
    '''
    IOT_DEVICE_MANAGEMENT = "IOT_DEVICE_MANAGEMENT"
    '''
    :stability: experimental
    '''
    IOT_EVENTS = "IOT_EVENTS"
    '''
    :stability: experimental
    '''
    IOT_EXPRESSLINK = "IOT_EXPRESSLINK"
    '''
    :stability: experimental
    '''
    IOT_FLEETWISE = "IOT_FLEETWISE"
    '''
    :stability: experimental
    '''
    IOT_GREENGRASS_ARTIFACT = "IOT_GREENGRASS_ARTIFACT"
    '''
    :stability: experimental
    '''
    IOT_GREENGRASS_COMPONENT = "IOT_GREENGRASS_COMPONENT"
    '''
    :stability: experimental
    '''
    IOT_GREENGRASS_COMPONENT_MACHINE_LEARNING = "IOT_GREENGRASS_COMPONENT_MACHINE_LEARNING"
    '''
    :stability: experimental
    '''
    IOT_GREENGRASS_COMPONENT_NUCLEUS = "IOT_GREENGRASS_COMPONENT_NUCLEUS"
    '''
    :stability: experimental
    '''
    IOT_GREENGRASS_COMPONENT_PRIVATE = "IOT_GREENGRASS_COMPONENT_PRIVATE"
    '''
    :stability: experimental
    '''
    IOT_GREENGRASS_COMPONENT_PUBLIC = "IOT_GREENGRASS_COMPONENT_PUBLIC"
    '''
    :stability: experimental
    '''
    IOT_GREENGRASS_INTERPROCESS_COMMUNICATION = "IOT_GREENGRASS_INTERPROCESS_COMMUNICATION"
    '''
    :stability: experimental
    '''
    IOT_GREENGRASS_PROTOCOL = "IOT_GREENGRASS_PROTOCOL"
    '''
    :stability: experimental
    '''
    IOT_GREENGRASS_RECIPE = "IOT_GREENGRASS_RECIPE"
    '''
    :stability: experimental
    '''
    IOT_GREENGRASS_STREAM_MANAGER = "IOT_GREENGRASS_STREAM_MANAGER"
    '''
    :stability: experimental
    '''
    IOT_LORAWAN_PROTOCOL = "IOT_LORAWAN_PROTOCOL"
    '''
    :stability: experimental
    '''
    IOT_OVER_THE_AIR_UPDATE = "IOT_OVER_THE_AIR_UPDATE"
    '''
    :stability: experimental
    '''
    IOT_ROBORUNNER = "IOT_ROBORUNNER"
    '''
    :stability: experimental
    '''
    IOT_SAILBOAT = "IOT_SAILBOAT"
    '''
    :stability: experimental
    '''
    IOT_SITEWISE = "IOT_SITEWISE"
    '''
    :stability: experimental
    '''
    IOT_SITEWISE_ASSET = "IOT_SITEWISE_ASSET"
    '''
    :stability: experimental
    '''
    IOT_SITEWISE_ASSET_HIERARCHY = "IOT_SITEWISE_ASSET_HIERARCHY"
    '''
    :stability: experimental
    '''
    IOT_SITEWISE_ASSET_MODEL = "IOT_SITEWISE_ASSET_MODEL"
    '''
    :stability: experimental
    '''
    IOT_SITEWISE_ASSET_PROPERTIES = "IOT_SITEWISE_ASSET_PROPERTIES"
    '''
    :stability: experimental
    '''
    IOT_SITEWISE_DATA_STREAMS = "IOT_SITEWISE_DATA_STREAMS"
    '''
    :stability: experimental
    '''
    IOT_THINGS_GRAPH = "IOT_THINGS_GRAPH"
    '''
    :stability: experimental
    '''
    IOT_THING_FREERTOS_DEVICE = "IOT_THING_FREERTOS_DEVICE"
    '''
    :stability: experimental
    '''
    IOT_THING_HUMIDITY_SENSOR = "IOT_THING_HUMIDITY_SENSOR"
    '''
    :stability: experimental
    '''
    IOT_THING_INDUSTRIAL_PC = "IOT_THING_INDUSTRIAL_PC"
    '''
    :stability: experimental
    '''
    IOT_THING_PLC = "IOT_THING_PLC"
    '''
    :stability: experimental
    '''
    IOT_THING_RELAY = "IOT_THING_RELAY"
    '''
    :stability: experimental
    '''
    IOT_THING_STACKLIGHT = "IOT_THING_STACKLIGHT"
    '''
    :stability: experimental
    '''
    IOT_THING_TEMPERATURE_HUMIDITY_SENSOR = "IOT_THING_TEMPERATURE_HUMIDITY_SENSOR"
    '''
    :stability: experimental
    '''
    IOT_THING_TEMPERATURE_SENSOR = "IOT_THING_TEMPERATURE_SENSOR"
    '''
    :stability: experimental
    '''
    IOT_THING_TEMPERATURE_VIBRATION_SENSOR = "IOT_THING_TEMPERATURE_VIBRATION_SENSOR"
    '''
    :stability: experimental
    '''
    IOT_THING_VIBRATION_SENSOR = "IOT_THING_VIBRATION_SENSOR"
    '''
    :stability: experimental
    '''
    IOT_TWINMAKER = "IOT_TWINMAKER"
    '''
    :stability: experimental
    '''
    IQ = "IQ"
    '''
    :stability: experimental
    '''
    ITEM = "ITEM"
    '''
    :stability: experimental
    '''
    ITEMS = "ITEMS"
    '''
    :stability: experimental
    '''
    KENDRA = "KENDRA"
    '''
    :stability: experimental
    '''
    KEYSPACES = "KEYSPACES"
    '''
    :stability: experimental
    '''
    KEY_MANAGEMENT_SERVICE = "KEY_MANAGEMENT_SERVICE"
    '''
    :stability: experimental
    '''
    KINESIS = "KINESIS"
    '''
    :stability: experimental
    '''
    KINESIS_DATA_ANALYTICS = "KINESIS_DATA_ANALYTICS"
    '''
    :stability: experimental
    '''
    KINESIS_DATA_FIREHOSE = "KINESIS_DATA_FIREHOSE"
    '''
    :stability: experimental
    '''
    KINESIS_DATA_STREAMS = "KINESIS_DATA_STREAMS"
    '''
    :stability: experimental
    '''
    KINESIS_VIDEO_STREAMS = "KINESIS_VIDEO_STREAMS"
    '''
    :stability: experimental
    '''
    LAKE_FORMATION = "LAKE_FORMATION"
    '''
    :stability: experimental
    '''
    LAMBDA = "LAMBDA"
    '''
    :stability: experimental
    '''
    LAMBDA_FUNCTION = "LAMBDA_FUNCTION"
    '''
    :stability: experimental
    '''
    LAYERS = "LAYERS"
    '''
    :stability: experimental
    '''
    LEX = "LEX"
    '''
    :stability: experimental
    '''
    LICENSE_MANAGER = "LICENSE_MANAGER"
    '''
    :stability: experimental
    '''
    LICENSE_MANAGER_APPLICATION_DISCOVERY = "LICENSE_MANAGER_APPLICATION_DISCOVERY"
    '''
    :stability: experimental
    '''
    LICENSE_MANAGER_LICENSE_BLENDING = "LICENSE_MANAGER_LICENSE_BLENDING"
    '''
    :stability: experimental
    '''
    LIGHTBULB = "LIGHTBULB"
    '''
    :stability: experimental
    '''
    LIGHTSAIL = "LIGHTSAIL"
    '''
    :stability: experimental
    '''
    LOCAL_ZONES = "LOCAL_ZONES"
    '''
    :stability: experimental
    '''
    LOCATION_SERVICE = "LOCATION_SERVICE"
    '''
    :stability: experimental
    '''
    LOCATION_SERVICE_GEOFENCE = "LOCATION_SERVICE_GEOFENCE"
    '''
    :stability: experimental
    '''
    LOCATION_SERVICE_MAP = "LOCATION_SERVICE_MAP"
    '''
    :stability: experimental
    '''
    LOCATION_SERVICE_PLACE = "LOCATION_SERVICE_PLACE"
    '''
    :stability: experimental
    '''
    LOCATION_SERVICE_ROUTES = "LOCATION_SERVICE_ROUTES"
    '''
    :stability: experimental
    '''
    LOCATION_SERVICE_TRACK = "LOCATION_SERVICE_TRACK"
    '''
    :stability: experimental
    '''
    LOGS = "LOGS"
    '''
    :stability: experimental
    '''
    LONG_TERM_SECURITY_CREDENTIAL = "LONG_TERM_SECURITY_CREDENTIAL"
    '''
    :stability: experimental
    '''
    LOOKOUT_FOR_EQUIPMENT = "LOOKOUT_FOR_EQUIPMENT"
    '''
    :stability: experimental
    '''
    LOOKOUT_FOR_METRICS = "LOOKOUT_FOR_METRICS"
    '''
    :stability: experimental
    '''
    LOOKOUT_FOR_VISION = "LOOKOUT_FOR_VISION"
    '''
    :stability: experimental
    '''
    LUMBERYARD = "LUMBERYARD"
    '''
    :stability: experimental
    '''
    M4_INSTANCE = "M4_INSTANCE"
    '''
    :stability: experimental
    '''
    M5A_INSTANCE = "M5A_INSTANCE"
    '''
    :stability: experimental
    '''
    M5DN_INSTANCE = "M5DN_INSTANCE"
    '''
    :stability: experimental
    '''
    M5D_INSTANCE = "M5D_INSTANCE"
    '''
    :stability: experimental
    '''
    M5N = "M5N"
    '''
    :stability: experimental
    '''
    M5N_INSTANCE = "M5N_INSTANCE"
    '''
    :stability: experimental
    '''
    M5ZN_INSTANCE = "M5ZN_INSTANCE"
    '''
    :stability: experimental
    '''
    M5_INSTANCE = "M5_INSTANCE"
    '''
    :stability: experimental
    '''
    M6GD_INSTANCE = "M6GD_INSTANCE"
    '''
    :stability: experimental
    '''
    M6G_INSTANCE = "M6G_INSTANCE"
    '''
    :stability: experimental
    '''
    MACHINE_LEARNING = "MACHINE_LEARNING"
    '''
    :stability: experimental
    '''
    MACIE = "MACIE"
    '''
    :stability: experimental
    '''
    MAC_INSTANCE = "MAC_INSTANCE"
    '''
    :stability: experimental
    '''
    MAINFRAME_MODERNIZATION = "MAINFRAME_MODERNIZATION"
    '''
    :stability: experimental
    '''
    MAINFRAME_MODERNIZATION_ANALYZER = "MAINFRAME_MODERNIZATION_ANALYZER"
    '''
    :stability: experimental
    '''
    MAINFRAME_MODERNIZATION_COMPILER = "MAINFRAME_MODERNIZATION_COMPILER"
    '''
    :stability: experimental
    '''
    MAINFRAME_MODERNIZATION_CONVERTER = "MAINFRAME_MODERNIZATION_CONVERTER"
    '''
    :stability: experimental
    '''
    MAINFRAME_MODERNIZATION_DEVELOPER = "MAINFRAME_MODERNIZATION_DEVELOPER"
    '''
    :stability: experimental
    '''
    MAINFRAME_MODERNIZATION_RUNTIME = "MAINFRAME_MODERNIZATION_RUNTIME"
    '''
    :stability: experimental
    '''
    MAINTENANCE_WINDOWS = "MAINTENANCE_WINDOWS"
    '''
    :stability: experimental
    '''
    MANAGED_APACHE_CASSANDRA_SERVICE = "MANAGED_APACHE_CASSANDRA_SERVICE"
    '''
    :stability: experimental
    '''
    MANAGED_BLOCKCHAIN = "MANAGED_BLOCKCHAIN"
    '''
    :stability: experimental
    '''
    MANAGED_MS_AD = "MANAGED_MS_AD"
    '''
    :stability: experimental
    '''
    MANAGED_SERVICES = "MANAGED_SERVICES"
    '''
    :stability: experimental
    '''
    MANAGED_SERVICE_FOR_GRAFANA = "MANAGED_SERVICE_FOR_GRAFANA"
    '''
    :stability: experimental
    '''
    MANAGED_SERVICE_FOR_PROMETHEUS = "MANAGED_SERVICE_FOR_PROMETHEUS"
    '''
    :stability: experimental
    '''
    MANAGED_STREAMING_FOR_KAFKA = "MANAGED_STREAMING_FOR_KAFKA"
    '''
    :stability: experimental
    '''
    MANAGED_WORKFLOWS_FOR_APACHE_AIRFLOW = "MANAGED_WORKFLOWS_FOR_APACHE_AIRFLOW"
    '''
    :stability: experimental
    '''
    MANAGEMENT_AND_GOVERNANCE = "MANAGEMENT_AND_GOVERNANCE"
    '''
    :stability: experimental
    '''
    MANAGEMENT_CONSOLE = "MANAGEMENT_CONSOLE"
    '''
    :stability: experimental
    '''
    MARKETPLACE = "MARKETPLACE"
    '''
    :stability: experimental
    '''
    MEDIA_SERVICES = "MEDIA_SERVICES"
    '''
    :stability: experimental
    '''
    MEDICAL_EMERGENCY = "MEDICAL_EMERGENCY"
    '''
    :stability: experimental
    '''
    MEMORYDB_FOR_REDIS = "MEMORYDB_FOR_REDIS"
    '''
    :stability: experimental
    '''
    MESH = "MESH"
    '''
    :stability: experimental
    '''
    MESSAGE = "MESSAGE"
    '''
    :stability: experimental
    '''
    MFA_TOKEN = "MFA_TOKEN"
    '''
    :stability: experimental
    '''
    MIGRATION_AND_TRANSFER = "MIGRATION_AND_TRANSFER"
    '''
    :stability: experimental
    '''
    MIGRATION_EVALUATOR = "MIGRATION_EVALUATOR"
    '''
    :stability: experimental
    '''
    MIGRATION_HUB = "MIGRATION_HUB"
    '''
    :stability: experimental
    '''
    MIGRATION_HUB_REFACTOR_SPACES_APPLICATIONS = "MIGRATION_HUB_REFACTOR_SPACES_APPLICATIONS"
    '''
    :stability: experimental
    '''
    MIGRATION_HUB_REFACTOR_SPACES_ENVIRONMENTS = "MIGRATION_HUB_REFACTOR_SPACES_ENVIRONMENTS"
    '''
    :stability: experimental
    '''
    MIGRATION_HUB_REFACTOR_SPACES_SERVICES = "MIGRATION_HUB_REFACTOR_SPACES_SERVICES"
    '''
    :stability: experimental
    '''
    MOBILE = "MOBILE"
    '''
    :stability: experimental
    '''
    MOBILE_APPLICATION = "MOBILE_APPLICATION"
    '''
    :stability: experimental
    '''
    MOBILE_CLIENT = "MOBILE_CLIENT"
    '''
    :stability: experimental
    '''
    MOBILE_HUB = "MOBILE_HUB"
    '''
    :stability: experimental
    '''
    MONITORING = "MONITORING"
    '''
    :stability: experimental
    '''
    MONITRON = "MONITRON"
    '''
    :stability: experimental
    '''
    MQ = "MQ"
    '''
    :stability: experimental
    '''
    MQTT_PROTOCOL = "MQTT_PROTOCOL"
    '''
    :stability: experimental
    '''
    MQ_BROKER = "MQ_BROKER"
    '''
    :stability: experimental
    '''
    MSK_AMAZON_MSK_CONNECT = "MSK_AMAZON_MSK_CONNECT"
    '''
    :stability: experimental
    '''
    MS_SQL_INSTANCE = "MS_SQL_INSTANCE"
    '''
    :stability: experimental
    '''
    MS_SQL_INSTANCE_ALTERNATE = "MS_SQL_INSTANCE_ALTERNATE"
    '''
    :stability: experimental
    '''
    MULTIMEDIA = "MULTIMEDIA"
    '''
    :stability: experimental
    '''
    MULTIPLE_VOLUMES_RESOURCE = "MULTIPLE_VOLUMES_RESOURCE"
    '''
    :stability: experimental
    '''
    MYSQL_DB_INSTANCE = "MYSQL_DB_INSTANCE"
    '''
    :stability: experimental
    '''
    MYSQL_DB_INSTANCE_ALTERNATE = "MYSQL_DB_INSTANCE_ALTERNATE"
    '''
    :stability: experimental
    '''
    NAMESPACE = "NAMESPACE"
    '''
    :stability: experimental
    '''
    NAT_GATEWAY = "NAT_GATEWAY"
    '''
    :stability: experimental
    '''
    NEPTUNE = "NEPTUNE"
    '''
    :stability: experimental
    '''
    NETWORKING_AND_CONTENT_DELIVERY = "NETWORKING_AND_CONTENT_DELIVERY"
    '''
    :stability: experimental
    '''
    NETWORK_ACCESS_CONTROL_LIST = "NETWORK_ACCESS_CONTROL_LIST"
    '''
    :stability: experimental
    '''
    NETWORK_FIREWALL = "NETWORK_FIREWALL"
    '''
    :stability: experimental
    '''
    NETWORK_FIREWALL_ENDPOINTS = "NETWORK_FIREWALL_ENDPOINTS"
    '''
    :stability: experimental
    '''
    NETWORK_LOAD_BALANCER = "NETWORK_LOAD_BALANCER"
    '''
    :stability: experimental
    '''
    NEURON_ML_SDK = "NEURON_ML_SDK"
    '''
    :stability: experimental
    '''
    NICE_DCV = "NICE_DCV"
    '''
    :stability: experimental
    '''
    NICE_ENGINFRAME = "NICE_ENGINFRAME"
    '''
    :stability: experimental
    '''
    NIMBLE_STUDIO = "NIMBLE_STUDIO"
    '''
    :stability: experimental
    '''
    NITRO_ENCLAVES = "NITRO_ENCLAVES"
    '''
    :stability: experimental
    '''
    NON_CACHED_VOLUME = "NON_CACHED_VOLUME"
    '''
    :stability: experimental
    '''
    NOTEBOOK = "NOTEBOOK"
    '''
    :stability: experimental
    '''
    OBJECT = "OBJECT"
    '''
    :stability: experimental
    '''
    OFFICE_BUILDING = "OFFICE_BUILDING"
    '''
    :stability: experimental
    '''
    ONE_ZONE_IA = "ONE_ZONE_IA"
    '''
    :stability: experimental
    '''
    OPEN_3D_ENGINE = "OPEN_3D_ENGINE"
    '''
    :stability: experimental
    '''
    OPSWORKS = "OPSWORKS"
    '''
    :stability: experimental
    '''
    OPSWORKS_APPS = "OPSWORKS_APPS"
    '''
    :stability: experimental
    '''
    OPSWORKS_PERMISSIONS = "OPSWORKS_PERMISSIONS"
    '''
    :stability: experimental
    '''
    OPTIMIZED_INSTANCE = "OPTIMIZED_INSTANCE"
    '''
    :stability: experimental
    '''
    ORACLE_DB_INSTANCE = "ORACLE_DB_INSTANCE"
    '''
    :stability: experimental
    '''
    ORACLE_DB_INSTANCE_ALTERNATE = "ORACLE_DB_INSTANCE_ALTERNATE"
    '''
    :stability: experimental
    '''
    ORGANIZATIONS = "ORGANIZATIONS"
    '''
    :stability: experimental
    '''
    ORGANIZATIONS_ACCOUNT = "ORGANIZATIONS_ACCOUNT"
    '''
    :stability: experimental
    '''
    ORGANIZATIONS_ACCOUNT2 = "ORGANIZATIONS_ACCOUNT2"
    '''
    :stability: experimental
    '''
    ORGANIZATIONS_MANAGEMENT_ACCOUNT = "ORGANIZATIONS_MANAGEMENT_ACCOUNT"
    '''
    :stability: experimental
    '''
    ORGANIZATIONS_MANAGEMENT_ACCOUNT2 = "ORGANIZATIONS_MANAGEMENT_ACCOUNT2"
    '''
    :stability: experimental
    '''
    ORGANIZATIONS_ORGANIZATIONAL_UNIT = "ORGANIZATIONS_ORGANIZATIONAL_UNIT"
    '''
    :stability: experimental
    '''
    ORGANIZATIONS_ORGANIZATIONAL_UNIT2 = "ORGANIZATIONS_ORGANIZATIONAL_UNIT2"
    '''
    :stability: experimental
    '''
    OUTPOSTS = "OUTPOSTS"
    '''
    :stability: experimental
    '''
    OUTPOSTS_1U_AND_2U_SERVERS = "OUTPOSTS_1U_AND_2U_SERVERS"
    '''
    :stability: experimental
    '''
    OUTPOSTS_FAMILY = "OUTPOSTS_FAMILY"
    '''
    :stability: experimental
    '''
    P2_INSTANCE = "P2_INSTANCE"
    '''
    :stability: experimental
    '''
    P3DN_INSTANCE = "P3DN_INSTANCE"
    '''
    :stability: experimental
    '''
    P3_INSTANCE = "P3_INSTANCE"
    '''
    :stability: experimental
    '''
    P4D_INSTANCE = "P4D_INSTANCE"
    '''
    :stability: experimental
    '''
    P4_INSTANCE = "P4_INSTANCE"
    '''
    :stability: experimental
    '''
    PANORAMA = "PANORAMA"
    '''
    :stability: experimental
    '''
    PARALLEL_CLUSTER = "PARALLEL_CLUSTER"
    '''
    :stability: experimental
    '''
    PARAMETER_STORE = "PARAMETER_STORE"
    '''
    :stability: experimental
    '''
    PATCH_MANAGER = "PATCH_MANAGER"
    '''
    :stability: experimental
    '''
    PEERING = "PEERING"
    '''
    :stability: experimental
    '''
    PERMISSIONS = "PERMISSIONS"
    '''
    :stability: experimental
    '''
    PERMISSIONS_2 = "PERMISSIONS_2"
    '''
    :stability: experimental
    '''
    PERSONALIZE = "PERSONALIZE"
    '''
    :stability: experimental
    '''
    PERSONAL_HEALTH_DASHBOARD = "PERSONAL_HEALTH_DASHBOARD"
    '''
    :stability: experimental
    '''
    PINPOINT = "PINPOINT"
    '''
    :stability: experimental
    '''
    PINPOINT_JOURNEY = "PINPOINT_JOURNEY"
    '''
    :stability: experimental
    '''
    POLICE_EMERGENCY = "POLICE_EMERGENCY"
    '''
    :stability: experimental
    '''
    POLICY = "POLICY"
    '''
    :stability: experimental
    '''
    POLLY = "POLLY"
    '''
    :stability: experimental
    '''
    POSTGRESQL_INSTANCE = "POSTGRESQL_INSTANCE"
    '''
    :stability: experimental
    '''
    PRIVATELINK = "PRIVATELINK"
    '''
    :stability: experimental
    '''
    PRIVATE_5G = "PRIVATE_5G"
    '''
    :stability: experimental
    '''
    PROFESSIONAL_SERVICES = "PROFESSIONAL_SERVICES"
    '''
    :stability: experimental
    '''
    PROTON = "PROTON"
    '''
    :stability: experimental
    '''
    QUANTUM_LEDGER_DATABASE = "QUANTUM_LEDGER_DATABASE"
    '''
    :stability: experimental
    '''
    QUANTUM_TECHNOLOGIES = "QUANTUM_TECHNOLOGIES"
    '''
    :stability: experimental
    '''
    QUESTION = "QUESTION"
    '''
    :stability: experimental
    '''
    QUEUE = "QUEUE"
    '''
    :stability: experimental
    '''
    QUICKSIGHT = "QUICKSIGHT"
    '''
    :stability: experimental
    '''
    R4_INSTANCE = "R4_INSTANCE"
    '''
    :stability: experimental
    '''
    R5AD_INSTANCE = "R5AD_INSTANCE"
    '''
    :stability: experimental
    '''
    R5A_INSTANCE = "R5A_INSTANCE"
    '''
    :stability: experimental
    '''
    R5B_INSTANCE = "R5B_INSTANCE"
    '''
    :stability: experimental
    '''
    R5D_INSTANCE = "R5D_INSTANCE"
    '''
    :stability: experimental
    '''
    R5GD_INSTANCE = "R5GD_INSTANCE"
    '''
    :stability: experimental
    '''
    R5N = "R5N"
    '''
    :stability: experimental
    '''
    R5N_INSTANCE = "R5N_INSTANCE"
    '''
    :stability: experimental
    '''
    R5_INSTANCE = "R5_INSTANCE"
    '''
    :stability: experimental
    '''
    R6G_INSTANCE = "R6G_INSTANCE"
    '''
    :stability: experimental
    '''
    RDN_INSTANCE = "RDN_INSTANCE"
    '''
    :stability: experimental
    '''
    RDS = "RDS"
    '''
    :stability: experimental
    '''
    RDS_INSTANCE = "RDS_INSTANCE"
    '''
    :stability: experimental
    '''
    RDS_INSTANCE_ALT = "RDS_INSTANCE_ALT"
    '''
    :stability: experimental
    '''
    RDS_MARIADB_INSTANCE = "RDS_MARIADB_INSTANCE"
    '''
    :stability: experimental
    '''
    RDS_MARIADB_INSTANCE_ALT = "RDS_MARIADB_INSTANCE_ALT"
    '''
    :stability: experimental
    '''
    RDS_MULTI_AZ = "RDS_MULTI_AZ"
    '''
    :stability: experimental
    '''
    RDS_MULTI_AZ_DB_CLUSTER = "RDS_MULTI_AZ_DB_CLUSTER"
    '''
    :stability: experimental
    '''
    RDS_MYSQL_INSTANCE = "RDS_MYSQL_INSTANCE"
    '''
    :stability: experimental
    '''
    RDS_MYSQL_INSTANCE_ALT = "RDS_MYSQL_INSTANCE_ALT"
    '''
    :stability: experimental
    '''
    RDS_ON_VMWARE = "RDS_ON_VMWARE"
    '''
    :stability: experimental
    '''
    RDS_ORACLE_INSTANCE = "RDS_ORACLE_INSTANCE"
    '''
    :stability: experimental
    '''
    RDS_ORACLE_INSTANCE_ALT = "RDS_ORACLE_INSTANCE_ALT"
    '''
    :stability: experimental
    '''
    RDS_PIOP = "RDS_PIOP"
    '''
    :stability: experimental
    '''
    RDS_PIOPS = "RDS_PIOPS"
    '''
    :stability: experimental
    '''
    RDS_POSTGRESQL_INSTANCE = "RDS_POSTGRESQL_INSTANCE"
    '''
    :stability: experimental
    '''
    RDS_POSTGRESQL_INSTANCE_ALT = "RDS_POSTGRESQL_INSTANCE_ALT"
    '''
    :stability: experimental
    '''
    RDS_PROXY = "RDS_PROXY"
    '''
    :stability: experimental
    '''
    RDS_PROXY_ALT = "RDS_PROXY_ALT"
    '''
    :stability: experimental
    '''
    RDS_SQL_SERVER_INSTANCE = "RDS_SQL_SERVER_INSTANCE"
    '''
    :stability: experimental
    '''
    RDS_SQL_SERVER_INSTANCE_ALT = "RDS_SQL_SERVER_INSTANCE_ALT"
    '''
    :stability: experimental
    '''
    REDSHIFT = "REDSHIFT"
    '''
    :stability: experimental
    '''
    REDSHIFT_ML = "REDSHIFT_ML"
    '''
    :stability: experimental
    '''
    REDSHIFT_RA3 = "REDSHIFT_RA3"
    '''
    :stability: experimental
    '''
    RED_HAT_OPENSHIFT = "RED_HAT_OPENSHIFT"
    '''
    :stability: experimental
    '''
    REGISTRY = "REGISTRY"
    '''
    :stability: experimental
    '''
    REKOGNITION = "REKOGNITION"
    '''
    :stability: experimental
    '''
    REKOGNITION_2 = "REKOGNITION_2"
    '''
    :stability: experimental
    '''
    REKOGNITION_IMAGE = "REKOGNITION_IMAGE"
    '''
    :stability: experimental
    '''
    REKOGNITION_VIDEO = "REKOGNITION_VIDEO"
    '''
    :stability: experimental
    '''
    REPLICATION = "REPLICATION"
    '''
    :stability: experimental
    '''
    REPLICATION_TIME_CONTROL = "REPLICATION_TIME_CONTROL"
    '''
    :stability: experimental
    '''
    REPORTED_STATE = "REPORTED_STATE"
    '''
    :stability: experimental
    '''
    REPOST = "REPOST"
    '''
    :stability: experimental
    '''
    RESCUE = "RESCUE"
    '''
    :stability: experimental
    '''
    RESERVED_INSTANCE_REPORTING = "RESERVED_INSTANCE_REPORTING"
    '''
    :stability: experimental
    '''
    RESILIENCE_HUB = "RESILIENCE_HUB"
    '''
    :stability: experimental
    '''
    RESOURCE = "RESOURCE"
    '''
    :stability: experimental
    '''
    RESOURCES = "RESOURCES"
    '''
    :stability: experimental
    '''
    RESOURCE_ACCESS_MANAGER = "RESOURCE_ACCESS_MANAGER"
    '''
    :stability: experimental
    '''
    ROBOMAKER = "ROBOMAKER"
    '''
    :stability: experimental
    '''
    ROBOTICS = "ROBOTICS"
    '''
    :stability: experimental
    '''
    ROLE = "ROLE"
    '''
    :stability: experimental
    '''
    ROUTER = "ROUTER"
    '''
    :stability: experimental
    '''
    ROUTE_53 = "ROUTE_53"
    '''
    :stability: experimental
    '''
    ROUTE_53_APPLICATION_RECOVERY_CONTROLLER = "ROUTE_53_APPLICATION_RECOVERY_CONTROLLER"
    '''
    :stability: experimental
    '''
    ROUTE_53_READINESS_CHECKS = "ROUTE_53_READINESS_CHECKS"
    '''
    :stability: experimental
    '''
    ROUTE_53_RESOLVER = "ROUTE_53_RESOLVER"
    '''
    :stability: experimental
    '''
    ROUTE_53_RESOLVER_DNS_FIREWALL = "ROUTE_53_RESOLVER_DNS_FIREWALL"
    '''
    :stability: experimental
    '''
    ROUTE_53_RESOLVER_QUERY_LOGGING = "ROUTE_53_RESOLVER_QUERY_LOGGING"
    '''
    :stability: experimental
    '''
    ROUTE_53_ROUTING_CONTROLS = "ROUTE_53_ROUTING_CONTROLS"
    '''
    :stability: experimental
    '''
    ROUTE_TABLE = "ROUTE_TABLE"
    '''
    :stability: experimental
    '''
    RULE = "RULE"
    '''
    :stability: experimental
    '''
    RULE_2 = "RULE_2"
    '''
    :stability: experimental
    '''
    RULE_3 = "RULE_3"
    '''
    :stability: experimental
    '''
    RUN_COMMAND = "RUN_COMMAND"
    '''
    :stability: experimental
    '''
    S3 = "S3"
    '''
    :stability: experimental
    '''
    S3_FILE_GATEWAY = "S3_FILE_GATEWAY"
    '''
    :stability: experimental
    '''
    S3_OBJECT_LAMBDA = "S3_OBJECT_LAMBDA"
    '''
    :stability: experimental
    '''
    S3_OBJECT_LAMBDA_ACCESS_POINTS = "S3_OBJECT_LAMBDA_ACCESS_POINTS"
    '''
    :stability: experimental
    '''
    S3_ON_OUTPOSTS = "S3_ON_OUTPOSTS"
    '''
    :stability: experimental
    '''
    S3_ON_OUTPOSTS_STORAGE = "S3_ON_OUTPOSTS_STORAGE"
    '''
    :stability: experimental
    '''
    S3_REPLICATION_TIME_CONTROL = "S3_REPLICATION_TIME_CONTROL"
    '''
    :stability: experimental
    '''
    S3_STORAGE_LENS = "S3_STORAGE_LENS"
    '''
    :stability: experimental
    '''
    SAAS_EVENT_BUS_RESOURCE = "SAAS_EVENT_BUS_RESOURCE"
    '''
    :stability: experimental
    '''
    SAGEMAKER = "SAGEMAKER"
    '''
    :stability: experimental
    '''
    SAGEMAKER_CANVAS = "SAGEMAKER_CANVAS"
    '''
    :stability: experimental
    '''
    SAGEMAKER_GROUND_TRUTH = "SAGEMAKER_GROUND_TRUTH"
    '''
    :stability: experimental
    '''
    SAGEMAKER_MODEL = "SAGEMAKER_MODEL"
    '''
    :stability: experimental
    '''
    SAGEMAKER_NOTEBOOK = "SAGEMAKER_NOTEBOOK"
    '''
    :stability: experimental
    '''
    SAGEMAKER_STUDIO_LAB = "SAGEMAKER_STUDIO_LAB"
    '''
    :stability: experimental
    '''
    SAGEMAKER_TRAIN = "SAGEMAKER_TRAIN"
    '''
    :stability: experimental
    '''
    SAML_TOKEN = "SAML_TOKEN"
    '''
    :stability: experimental
    '''
    SATELLITE = "SATELLITE"
    '''
    :stability: experimental
    '''
    SAVINGS_PLANS = "SAVINGS_PLANS"
    '''
    :stability: experimental
    '''
    SEARCH_DOCUMENTS = "SEARCH_DOCUMENTS"
    '''
    :stability: experimental
    '''
    SECRETS_MANAGER = "SECRETS_MANAGER"
    '''
    :stability: experimental
    '''
    SECURITY_GROUP = "SECURITY_GROUP"
    '''
    :stability: experimental
    '''
    SECURITY_HUB = "SECURITY_HUB"
    '''
    :stability: experimental
    '''
    SECURITY_HUB_FINDING = "SECURITY_HUB_FINDING"
    '''
    :stability: experimental
    '''
    SECURITY_IDENTITY_AND_COMPLIANCE = "SECURITY_IDENTITY_AND_COMPLIANCE"
    '''
    :stability: experimental
    '''
    SENSOR = "SENSOR"
    '''
    :stability: experimental
    '''
    SERVERLESS = "SERVERLESS"
    '''
    :stability: experimental
    '''
    SERVERLESS_APPLICATION_REPOSITORY = "SERVERLESS_APPLICATION_REPOSITORY"
    '''
    :stability: experimental
    '''
    SERVER_MIGRATION_SERVICE = "SERVER_MIGRATION_SERVICE"
    '''
    :stability: experimental
    '''
    SERVICE = "SERVICE"
    '''
    :stability: experimental
    '''
    SERVICE_CATALOG = "SERVICE_CATALOG"
    '''
    :stability: experimental
    '''
    SERVO = "SERVO"
    '''
    :stability: experimental
    '''
    SHADOW = "SHADOW"
    '''
    :stability: experimental
    '''
    SHIELD = "SHIELD"
    '''
    :stability: experimental
    '''
    SHIELD_SHIELD_ADVANCED = "SHIELD_SHIELD_ADVANCED"
    '''
    :stability: experimental
    '''
    SIGNER = "SIGNER"
    '''
    :stability: experimental
    '''
    SIMPLE_AD = "SIMPLE_AD"
    '''
    :stability: experimental
    '''
    SIMPLE_EMAIL_SERVICE = "SIMPLE_EMAIL_SERVICE"
    '''
    :stability: experimental
    '''
    SIMPLE_STORAGE_SERVICE_S3_GLACIER_INSTANT_RETRIEVAL = "SIMPLE_STORAGE_SERVICE_S3_GLACIER_INSTANT_RETRIEVAL"
    '''
    :stability: experimental
    '''
    SIMULATION = "SIMULATION"
    '''
    :stability: experimental
    '''
    SIMULATOR = "SIMULATOR"
    '''
    :stability: experimental
    '''
    SINGLE_SIGN_ON = "SINGLE_SIGN_ON"
    '''
    :stability: experimental
    '''
    SITE_TO_SITE_VPN = "SITE_TO_SITE_VPN"
    '''
    :stability: experimental
    '''
    SNAPSHOT = "SNAPSHOT"
    '''
    :stability: experimental
    '''
    SNOWBALL = "SNOWBALL"
    '''
    :stability: experimental
    '''
    SNOWBALL_EDGE = "SNOWBALL_EDGE"
    '''
    :stability: experimental
    '''
    SNOWCONE = "SNOWCONE"
    '''
    :stability: experimental
    '''
    SNOWMOBILE = "SNOWMOBILE"
    '''
    :stability: experimental
    '''
    SNS = "SNS"
    '''
    :stability: experimental
    '''
    SPOT_INSTANCE = "SPOT_INSTANCE"
    '''
    :stability: experimental
    '''
    SQL_PRIMARY = "SQL_PRIMARY"
    '''
    :stability: experimental
    '''
    SQL_REPLICA = "SQL_REPLICA"
    '''
    :stability: experimental
    '''
    SQL_WORKBENCH = "SQL_WORKBENCH"
    '''
    :stability: experimental
    '''
    SQS = "SQS"
    '''
    :stability: experimental
    '''
    SSL_PADLOCK = "SSL_PADLOCK"
    '''
    :stability: experimental
    '''
    STACK = "STACK"
    '''
    :stability: experimental
    '''
    STACK2 = "STACK2"
    '''
    :stability: experimental
    '''
    STANDARD_IA = "STANDARD_IA"
    '''
    :stability: experimental
    '''
    STATE_MANAGER = "STATE_MANAGER"
    '''
    :stability: experimental
    '''
    STEP_FUNCTIONS = "STEP_FUNCTIONS"
    '''
    :stability: experimental
    '''
    STORAGE = "STORAGE"
    '''
    :stability: experimental
    '''
    STORAGE_GATEWAY = "STORAGE_GATEWAY"
    '''
    :stability: experimental
    '''
    STREAMING_DISTRIBUTION = "STREAMING_DISTRIBUTION"
    '''
    :stability: experimental
    '''
    STS = "STS"
    '''
    :stability: experimental
    '''
    STS_ALTERNATE = "STS_ALTERNATE"
    '''
    :stability: experimental
    '''
    SUMERIAN = "SUMERIAN"
    '''
    :stability: experimental
    '''
    SUPPORT = "SUPPORT"
    '''
    :stability: experimental
    '''
    SYSTEMS_MANAGER = "SYSTEMS_MANAGER"
    '''
    :stability: experimental
    '''
    SYSTEMS_MANAGER_INCIDENT_MANAGER = "SYSTEMS_MANAGER_INCIDENT_MANAGER"
    '''
    :stability: experimental
    '''
    SYSTEMS_MANAGER_OPSCENTER = "SYSTEMS_MANAGER_OPSCENTER"
    '''
    :stability: experimental
    '''
    T2_INSTANCE = "T2_INSTANCE"
    '''
    :stability: experimental
    '''
    T3A_INSTANCE = "T3A_INSTANCE"
    '''
    :stability: experimental
    '''
    T3_INSTANCE = "T3_INSTANCE"
    '''
    :stability: experimental
    '''
    T4G_INSTANCE = "T4G_INSTANCE"
    '''
    :stability: experimental
    '''
    TABLE = "TABLE"
    '''
    :stability: experimental
    '''
    TAPE_GATEWAY = "TAPE_GATEWAY"
    '''
    :stability: experimental
    '''
    TAPE_STORAGE = "TAPE_STORAGE"
    '''
    :stability: experimental
    '''
    TEMPLATE = "TEMPLATE"
    '''
    :stability: experimental
    '''
    TEMPORARY_SECURITY_CREDENTIAL = "TEMPORARY_SECURITY_CREDENTIAL"
    '''
    :stability: experimental
    '''
    TENSORFLOW_ON_AWS = "TENSORFLOW_ON_AWS"
    '''
    :stability: experimental
    '''
    TEXTRACT = "TEXTRACT"
    '''
    :stability: experimental
    '''
    THERMOSTAT = "THERMOSTAT"
    '''
    :stability: experimental
    '''
    THINKBOX_DEADLINE = "THINKBOX_DEADLINE"
    '''
    :stability: experimental
    '''
    THINKBOX_DRAFT = "THINKBOX_DRAFT"
    '''
    :stability: experimental
    '''
    THINKBOX_FROST = "THINKBOX_FROST"
    '''
    :stability: experimental
    '''
    THINKBOX_KRAKATOA = "THINKBOX_KRAKATOA"
    '''
    :stability: experimental
    '''
    THINKBOX_SEQUOIA = "THINKBOX_SEQUOIA"
    '''
    :stability: experimental
    '''
    THINKBOX_STOKE = "THINKBOX_STOKE"
    '''
    :stability: experimental
    '''
    THINKBOX_XMESH = "THINKBOX_XMESH"
    '''
    :stability: experimental
    '''
    TIMESTREAM = "TIMESTREAM"
    '''
    :stability: experimental
    '''
    TOOLS_AND_SDKS = "TOOLS_AND_SDKS"
    '''
    :stability: experimental
    '''
    TOPIC = "TOPIC"
    '''
    :stability: experimental
    '''
    TOPIC_2 = "TOPIC_2"
    '''
    :stability: experimental
    '''
    TORCHSERVE = "TORCHSERVE"
    '''
    :stability: experimental
    '''
    TRADITIONAL_SERVER = "TRADITIONAL_SERVER"
    '''
    :stability: experimental
    '''
    TRAINING_CERTIFICATION = "TRAINING_CERTIFICATION"
    '''
    :stability: experimental
    '''
    TRAINIUM_INSTANCE = "TRAINIUM_INSTANCE"
    '''
    :stability: experimental
    '''
    TRANSCRIBE = "TRANSCRIBE"
    '''
    :stability: experimental
    '''
    TRANSFER_FAMILY = "TRANSFER_FAMILY"
    '''
    :stability: experimental
    '''
    TRANSFER_FOR_FTPS_RESOURCE = "TRANSFER_FOR_FTPS_RESOURCE"
    '''
    :stability: experimental
    '''
    TRANSFER_FOR_FTP_RESOURCE = "TRANSFER_FOR_FTP_RESOURCE"
    '''
    :stability: experimental
    '''
    TRANSFER_FOR_SFTP = "TRANSFER_FOR_SFTP"
    '''
    :stability: experimental
    '''
    TRANSFER_FOR_SFTP_RESOURCE = "TRANSFER_FOR_SFTP_RESOURCE"
    '''
    :stability: experimental
    '''
    TRANSIT_GATEWAY = "TRANSIT_GATEWAY"
    '''
    :stability: experimental
    '''
    TRANSIT_GATEWAY_ATTACHMENT = "TRANSIT_GATEWAY_ATTACHMENT"
    '''
    :stability: experimental
    '''
    TRANSLATE = "TRANSLATE"
    '''
    :stability: experimental
    '''
    TRAVEL = "TRAVEL"
    '''
    :stability: experimental
    '''
    TRUSTED_ADVISOR = "TRUSTED_ADVISOR"
    '''
    :stability: experimental
    '''
    USER = "USER"
    '''
    :stability: experimental
    '''
    USERS = "USERS"
    '''
    :stability: experimental
    '''
    UTILITY = "UTILITY"
    '''
    :stability: experimental
    '''
    VAULT = "VAULT"
    '''
    :stability: experimental
    '''
    VIRTUAL_GATEWAY = "VIRTUAL_GATEWAY"
    '''
    :stability: experimental
    '''
    VIRTUAL_NODE = "VIRTUAL_NODE"
    '''
    :stability: experimental
    '''
    VIRTUAL_PRIVATE_CLOUD = "VIRTUAL_PRIVATE_CLOUD"
    '''
    :stability: experimental
    '''
    VIRTUAL_ROUTER = "VIRTUAL_ROUTER"
    '''
    :stability: experimental
    '''
    VIRTUAL_SERVICE = "VIRTUAL_SERVICE"
    '''
    :stability: experimental
    '''
    VIRTUAL_TAPE_LIBRARY = "VIRTUAL_TAPE_LIBRARY"
    '''
    :stability: experimental
    '''
    VMWARE_CLOUD_ON_AWS = "VMWARE_CLOUD_ON_AWS"
    '''
    :stability: experimental
    '''
    VOLUME = "VOLUME"
    '''
    :stability: experimental
    '''
    VOLUME_GATEWAY = "VOLUME_GATEWAY"
    '''
    :stability: experimental
    '''
    VPC = "VPC"
    '''
    :stability: experimental
    '''
    VPC_ACCESS_POINTS = "VPC_ACCESS_POINTS"
    '''
    :stability: experimental
    '''
    VPC_CARRIER_GATEWAY = "VPC_CARRIER_GATEWAY"
    '''
    :stability: experimental
    '''
    VPC_NETWORK_ACCESS_ANALYZER = "VPC_NETWORK_ACCESS_ANALYZER"
    '''
    :stability: experimental
    '''
    VPC_PRIVATELINK = "VPC_PRIVATELINK"
    '''
    :stability: experimental
    '''
    VPC_REACHABILITY_ANALYZER = "VPC_REACHABILITY_ANALYZER"
    '''
    :stability: experimental
    '''
    VPC_TRAFFIC_MIRRORING = "VPC_TRAFFIC_MIRRORING"
    '''
    :stability: experimental
    '''
    VPN_CONNECTION = "VPN_CONNECTION"
    '''
    :stability: experimental
    '''
    VPN_GATEWAY = "VPN_GATEWAY"
    '''
    :stability: experimental
    '''
    WAF = "WAF"
    '''
    :stability: experimental
    '''
    WAF_BAD_BOT = "WAF_BAD_BOT"
    '''
    :stability: experimental
    '''
    WAF_BOT = "WAF_BOT"
    '''
    :stability: experimental
    '''
    WAF_BOT_CONTROL = "WAF_BOT_CONTROL"
    '''
    :stability: experimental
    '''
    WAF_LABELS = "WAF_LABELS"
    '''
    :stability: experimental
    '''
    WAF_MANAGED_RULE = "WAF_MANAGED_RULE"
    '''
    :stability: experimental
    '''
    WAF_RULE = "WAF_RULE"
    '''
    :stability: experimental
    '''
    WAVELENGTH = "WAVELENGTH"
    '''
    :stability: experimental
    '''
    WELL_ARCHITECTED_TOOL = "WELL_ARCHITECTED_TOOL"
    '''
    :stability: experimental
    '''
    WELL_ARCHITECT_TOOL = "WELL_ARCHITECT_TOOL"
    '''
    :stability: experimental
    '''
    WINDFARM = "WINDFARM"
    '''
    :stability: experimental
    '''
    WORKDOCS = "WORKDOCS"
    '''
    :stability: experimental
    '''
    WORKLINK = "WORKLINK"
    '''
    :stability: experimental
    '''
    WORKMAIL = "WORKMAIL"
    '''
    :stability: experimental
    '''
    WORKSPACES = "WORKSPACES"
    '''
    :stability: experimental
    '''
    WORKSPACES_WORKSPACES_WEB = "WORKSPACES_WORKSPACES_WEB"
    '''
    :stability: experimental
    '''
    X1E_INSTANCE = "X1E_INSTANCE"
    '''
    :stability: experimental
    '''
    X1_INSTANCE = "X1_INSTANCE"
    '''
    :stability: experimental
    '''
    X1_INSTANCE2 = "X1_INSTANCE2"
    '''
    :stability: experimental
    '''
    XRAY = "XRAY"
    '''
    :stability: experimental
    '''
    Z1D_INSTANCE = "Z1D_INSTANCE"
    '''
    :stability: experimental
    '''


__all__ = [
    "ShapeNames",
]

publication.publish()
