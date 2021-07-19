import json
import os

# gcp envvars
ENV_ENTRY_POINT = 'ENTRY_POINT'
ENV_GCP_PROJECT = 'GCP_PROJECT'
ENV_FUNCTION_TRIGGER_TYPE = 'FUNCTION_TRIGGER_TYPE'
ENV_FUNCTION_NAME = 'FUNCTION_NAME'
ENV_FUNCTION_MEMORY_MB = 'FUNCTION_MEMORY_MB'
ENV_FUNCTION_TIMEOUT_SEC = 'FUNCTION_TIMEOUT_SEC'
ENV_FUNCTION_IDENTITY = 'FUNCTION_IDENTITY'
ENV_FUNCTION_REGION = 'FUNCTION_REGION'

# custom envvars
ENV_PG_HOST = 'PG_HOST'
ENV_PG_SCHEMA = 'PG_SCHEMA'
ENV_PG_USER = 'PG_USER'
ENV_PG_PASSWORD = 'PG_PASSWORD'


class GCPConfig:
    """
    GCPConfig contains all envvars automatically exposed by the "newer" gcp cloud func runtimes
    """

    def __init__(self):
        self.entry_point = os.environ.get(ENV_ENTRY_POINT)
        self.gcp_project = os.environ.get(ENV_GCP_PROJECT)
        self.function_trigger_type = os.environ.get(ENV_FUNCTION_TRIGGER_TYPE)
        self.function_name = os.environ.get(ENV_FUNCTION_NAME)
        self.function_memory_mb = os.environ.get(ENV_FUNCTION_MEMORY_MB)
        self.function_timeout_sec = os.environ.get(ENV_FUNCTION_TIMEOUT_SEC)
        self.function_identity = os.environ.get(ENV_FUNCTION_IDENTITY)
        self.function_region = os.environ.get(ENV_FUNCTION_REGION)


class PGConfig:
    """
    PGConfig contains all necessary PSQL configuration
    """

    def __init__(self):
        self.host = os.environ.get(ENV_PG_HOST)
        self.schema = os.environ.get(ENV_PG_SCHEMA)
        self.user = os.environ.get(ENV_PG_USER)
        self.password = os.environ.get(ENV_PG_PASSWORD)


class Config:
    """
    Config is the root container for all configurations present for this cloud func
    """

    def __init__(self):
        self.gcp = GCPConfig()
        self.pg = PGConfig()
