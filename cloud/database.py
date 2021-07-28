import datetime
from typing import Optional

from sqlalchemy import engine, event, orm  # root packages
from sqlalchemy.dialects import postgresql
from sqlalchemy import Column, Integer, String, TIMESTAMP  # column types

import config
import fhir
import gcf

_PG_DRIVER = 'postgresql+pg8000'
_PG_PORT = 5432  # TODO: make configurable

_RESOURCE_FILE_TABLE = 'resource_files'


class Manager:
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

    def insert_single_entity(self, entity) -> None:
        """
            insert_single_entity wraps the creation of a new session and single entity persistence

           :param entity: Entity to be persisted
           :return: None, exceptions are always re-thrown in the event of one.
           """
        db_sess = self.open_session()
        try:
            # add entity to session
            db_sess.add(entity)
            # flush entity to db's buffer
            db_sess.flush()
            # attempt to commit changes
            db_sess.commit()
        except Exception as e:
            db_sess.rollback()
            raise e
        finally:
            db_sess.close()


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
    uploaded = Column(TIMESTAMP(timezone=True), nullable=False, comment='Date file uploaded to GCS bucket')
    inserted = Column(TIMESTAMP(timezone=True), nullable=False, comment='Date record inserted into DB')
    meta = Column(postgresql.JSONB, nullable=True, comment='Raw JSON contents of FHIR JSON file')
    bucket = Column(String, nullable=False, comment='Name of GCS bucket file is present in')

    def __repr__(self):
        return self.meta


def create_psql_resource_entity(fhir_resource: fhir.Resource, object_meta: gcf.ObjectMeta) -> ResourceFile:
    """
    create_psql_resource_entity constructs a new ResourceFile entity, ready to be persisted into postgres

    :param fhir_resource: Source resource file
    :param object_meta: Object location metadata
    :return: Constructed ResourceFile instance
    """

    # construct new ResourceFile
    resource_file = ResourceFile()

    # populate
    resource_file.resource_id = fhir_resource.resource_id
    resource_file.resource_type = fhir_resource.resource_type
    resource_file.object_path = object_meta.path
    resource_file.uploaded = object_meta.created
    resource_file.inserted = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    resource_file.meta = fhir_resource.raw
    # dumb pythonic ways are dumb.
    resource_file.bucket = object_meta.bucket

    return resource_file


def fetch_fhir_psql_resource(dbm: Manager, resource_id: str) -> Optional[ResourceFile]:
    """
    fetch_fhir_psql_resource returns true if a row is found in the DB with a given Resource ID

    :param dbm: Existing database connection
    :param resource_id: ID of resource to attempt to fetch from PSQL
    :return: returns ResourceFile or None if one was not found
    """
    db_sess = dbm.open_session()
    db_query = db_sess.query(ResourceFile) \
        .filter_by(resource_id=resource_id) \
        .order_by(ResourceFile.inserted.desc())  # type: Query
    res = db_query.one_or_none()
    db_sess.close()
    return res