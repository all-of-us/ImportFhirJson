import os

# gcp envvars
ENV_FUNCTION_TARGET = 'FUNCTION_TARGET'
ENV_FUNCTION_SIGNATURE_TYPE = 'FUNCTION_SIGNATURE_TYPE'
ENV_K_SERVICE = 'K_SERVICE'
ENV_K_REVISION = 'K_REVISION'
ENV_PORT = 'PORT'

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
        self.function_target = os.environ.get(ENV_FUNCTION_TARGET)
        self.function_signature_type = os.environ.get(ENV_FUNCTION_SIGNATURE_TYPE)
        self.k_service = os.environ.get(ENV_K_SERVICE)
        self.k_revision = os.environ.get(ENV_K_REVISION)
        self.port = os.environ.get(ENV_PORT)


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