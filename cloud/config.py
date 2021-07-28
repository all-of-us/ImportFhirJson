import os

# custom envvars
ENV_PG_HOST = 'PG_HOST'
ENV_PG_SCHEMA = 'PG_SCHEMA'
ENV_PG_USER = 'PG_USER'
ENV_PG_PASSWORD = 'PG_PASSWORD'
ENV_PG_DATABASE = 'PG_DATABASE'

# timezone
ENV_TZ = 'TZ'

# gcf x_google envvars
ENV_X_GOOGLE_CODE_LOCATION = 'X_GOOGLE_CODE_LOCATION'
ENV_X_GOOGLE_CONTAINER_LOGGING_ENABLED = 'X_GOOGLE_CONTAINER_LOGGING_ENABLED'
ENV_X_GOOGLE_ENTRY_POINT = 'X_GOOGLE_ENTRY_POINT'
ENV_X_GOOGLE_FUNCTION_IDENTITY = 'X_GOOGLE_FUNCTION_IDENTITY'
ENV_X_GOOGLE_FUNCTION_MEMORY_MB = 'X_GOOGLE_FUNCTION_MEMORY_MB'
ENV_X_GOOGLE_FUNCTION_NAME = 'X_GOOGLE_FUNCTION_NAME'
ENV_X_GOOGLE_FUNCTION_REGION = 'X_GOOGLE_FUNCTION_REGION'
ENV_X_GOOGLE_FUNCTION_TIMEOUT_SEC = 'X_GOOGLE_FUNCTION_TIMEOUT_SEC'
ENV_X_GOOGLE_FUNCTION_TRIGGER_TYPE = 'X_GOOGLE_FUNCTION_TRIGGER_TYPE'
ENV_X_GOOGLE_FUNCTION_VERSION = 'X_GOOGLE_FUNCTION_VERSION'
ENV_X_GOOGLE_GCLOUD_PROJECT = 'X_GOOGLE_GCLOUD_PROJECT'
ENV_X_GOOGLE_GCP_PROJECT = 'X_GOOGLE_GCP_PROJECT'
ENV_X_GOOGLE_LOAD_ON_START = 'X_GOOGLE_LOAD_ON_START'
ENV_X_GOOGLE_SUPERVISOR_HOSTNAME = 'X_GOOGLE_SUPERVISOR_HOSTNAME'
ENV_X_GOOGLE_SUPERVISOR_INTERNAL_PORT = 'X_GOOGLE_SUPERVISOR_INTERNAL_PORT'
ENV_X_GOOGLE_WORKER_PORT = 'X_GOOGLE_WORKER_PORT'

# gcf function_ envvars
ENV_FUNCTION_IDENTITY = 'FUNCTION_IDENTITY'
ENV_FUNCTION_MEMORY_MB = 'FUNCTION_MEMORY_MB'
ENV_FUNCTION_NAME = 'FUNCTION_NAME'
ENV_FUNCTION_REGION = 'FUNCTION_REGION'
ENV_FUNCTION_TIMEOUT_SEC = 'FUNCTION_TIMEOUT_SEC'
ENV_FUNCTION_TRIGGER_TYPE = 'FUNCTION_TRIGGER_TYPE'

# misc gcp envvars
ENV_HOME = 'HOME'
ENV_LC_CTYPE = 'LC_CTYPE'
ENV_PATH = 'PATH'
ENV_VIRTUAL_ENV = 'VIRTUAL_ENV'
ENV_WORKER_PORT = 'WORKER_PORT'


class GCFConfig:
    """
    GCFConfig contains gcf-specific config
    """

    def __init__(self):
        self.codeLocation = os.getenv(ENV_X_GOOGLE_CODE_LOCATION)
        self.containerLoggingEnabled = os.getenv(ENV_X_GOOGLE_CONTAINER_LOGGING_ENABLED, '').lower() == 'true'
        self.entryPoint = os.getenv(ENV_X_GOOGLE_ENTRY_POINT)
        self.functionIdentity = os.getenv(ENV_X_GOOGLE_FUNCTION_IDENTITY)
        self.functionMemoryMB = int(os.getenv(ENV_X_GOOGLE_FUNCTION_MEMORY_MB, 0))
        self.functionName = os.getenv(ENV_X_GOOGLE_FUNCTION_NAME)
        self.functionRegion = os.getenv(ENV_X_GOOGLE_FUNCTION_REGION)
        self.functionTimeoutSec = os.getenv(ENV_X_GOOGLE_FUNCTION_TIMEOUT_SEC)
        self.functionTriggerType = os.getenv(ENV_X_GOOGLE_FUNCTION_TRIGGER_TYPE)
        self.functionVersion = int(os.getenv(ENV_X_GOOGLE_FUNCTION_VERSION, 0))
        self.gcloudProject = os.getenv(ENV_X_GOOGLE_GCLOUD_PROJECT)
        self.gcpProject = os.getenv(ENV_X_GOOGLE_GCP_PROJECT)  # todo: redundant, which is the one to keep?
        self.loadOnStart = os.getenv(ENV_X_GOOGLE_LOAD_ON_START, '').lower() == 'true'
        self.supervisorHostname = os.getenv(ENV_X_GOOGLE_SUPERVISOR_HOSTNAME)
        self.supervisorInternalPort = int(os.getenv(ENV_X_GOOGLE_SUPERVISOR_INTERNAL_PORT, 0))
        self.workerPort = int(os.getenv(ENV_X_GOOGLE_WORKER_PORT, 0))


class PGConfig:
    """
    PGConfig contains all necessary PSQL configuration
    """

    def __init__(self):
        self.host = os.getenv(ENV_PG_HOST)
        self.schema = os.getenv(ENV_PG_SCHEMA)
        self.user = os.getenv(ENV_PG_USER)
        self.password = os.getenv(ENV_PG_PASSWORD)
        self.database = os.getenv(ENV_PG_DATABASE)


class Config:
    """
    Config is the root container for all configurations present for this cloud func
    """

    def __init__(self):
        # init psql config
        self.pg = PGConfig()

        # init gcf config
        self.gcf = GCFConfig()

        # some gcf configs i don't feel like building another type for
        self.home_path = os.getenv(ENV_HOME)
        self.path = os.getenv(ENV_PATH)
        self.virtual_env = os.getenv(ENV_VIRTUAL_ENV)
        self.worker_port = int(os.getenv(ENV_WORKER_PORT, 0))

        # i set this one specifically, mebe bad idea?
        self.tz_locale_string = os.getenv(ENV_TZ)
