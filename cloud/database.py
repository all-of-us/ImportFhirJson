from sqlalchemy import engine, event, orm  # root packages
from sqlalchemy.dialects import postgresql
from sqlalchemy import Column, Integer, MetaData, String  # column types

import config

_PG_DRIVER = 'postgresql+pg8000'
_PG_PORT = 5432  # TODO: make configurable

_RESOURCE_FILE_TABLE = 'resource_files'


class Connection:
    def __init__(self, conf: config.Config):
        self._engine = engine.create_engine(
            engine.url.URL.create(
                drivername=_PG_DRIVER,
                username=conf.pg.user,
                password=conf.pg.password,
                host=conf.pg.host,
                port=_PG_PORT,
                database=conf.pg.database,
            ),
            connect_args={
                'timeout': 10,
            }
        )

    def open_session(self) -> orm.Session:
        """
        open_session returns a new session for immediate use
        TODO: probably hacky AF.
        :return:
        """
        sess = orm.sessionmaker(bind=self._engine)()  # type: orm.Session
        return sess


BaseModel = orm.declarative_base()


class ResourceFile(BaseModel):
    """
    ResourceFile represents the raw contents of an uploaded FHIR resource to the GCS bucket
    """
    __tablename__ = _RESOURCE_FILE_TABLE

    id = Column(Integer, primary_key=True, comment='The primariest of keys')
    resource_type = Column(String, nullable=False, comment='Type of FHIR Resource contained in this file')
    resource_id = Column(String, nullable=False, comment='ID of FHIR Resource contained in this file')
    object_path = Column(String, nullable=False, comment='Full path to FHIR file within bucket')
    uploaded = Column(String, nullable=False, comment='Date file uploaded to GCS bucket')
    meta = Column(postgresql.JSONB, nullable=True, comment='Raw JSON contents of FHIR JSON file')
    bucket = Column(String, nullable=False, comment='Name of GCS bucket file is present in')

    def __repr__(self):
        return self.meta
