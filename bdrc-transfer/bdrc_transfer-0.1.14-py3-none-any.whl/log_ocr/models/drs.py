"""
Sources:
toth to https://stackoverflow.com/questions/33743379/sqlalchemy-timestamp-on-update-extra
    create_time = Column(TIMESTAMP, nullable=False, server_default=sqlalchemy.func.now())
    update_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

"""

import sqlalchemy
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, DateTime, text
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.dialects.mysql import (
    BIGINT,
    # BINARY,
    # BIT,
    # BLOB,
    # BOOLEAN,
    # CHAR,
    # DATE,
    # DATETIME,
    # DECIMAL,
    # DECIMAL,
    # DOUBLE,
    # ENUM,
    # FLOAT,
    # INTEGER,
    # LONGBLOB,
    LONGTEXT,
    # MEDIUMBLOB,
    # MEDIUMINT,
    # MEDIUMTEXT,
    # NCHAR,
    # NUMERIC,
    # NVARCHAR,
    # REAL,
    # SET,
    # SMALLINT,
    # TEXT,
    # TIME,
    TIMESTAMP,
    # TINYBLOB,
    # TINYINT,
    # TINYTEXT,
    # VARBINARY,
    # VARCHAR,
    # YEAR,
)

Base = declarative_base()

class TimestampMixin:
    """
    Injects created and update times
    Tip o the hat to https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/mixins.html
    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

class Works(Base):
    __tablename__ = "Works"
    workId = Column(Integer, primary_key=True, autoincrement=True)
    WorkName = Column(String(45))
    WorkSize = Column(BIGINT)
    HOLLIS = Column(String(45))
    WorkFileCount = Column(BIGINT)
    WorkImageFileCount = Column(BIGINT)
    WorkImageTotalFileSize = Column(BIGINT)
    WorkNonImageFileCount = Column(BIGINT)
    WorkNonImageTotalFileSize = Column(BIGINT)

    volumes = relationship("Volumes", back_populates='work')
#    gb_metadata = relationship("GBMetadata", back_populates='work')

    create_time = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __repr__(self) -> str:
        return f"id: {self.workId}:{self.WorkName}"


class Volumes(Base):
    __tablename__ = 'Volumes'
    volumeId = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String(45))
    workId = Column(Integer, ForeignKey('Works.workId'))


    work = relationship("Works", back_populates='volumes')
    gb_downloads = relationship("GbDownload", back_populates='volume')
    gb_content = relationship("GbContent", back_populates='volume')
    gb_state = relationship('GbState', back_populates='volume')
    gb_dist = relationship('GbDistribution', back_populates='volume')
    gb_unpack = relationship('GbUnpack', back_populates='volume')


    create_time = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __repr__(self):
        return f"<volume(ig):{self.label} id: {self.volumeId}>"



class GbMetadata(Base):
    """
    xxx = GbMetaDataTrack(work_id = workId,upload_time = some_time)
    Record the upload of a work's metadata to GB: columns
    `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    `update_time` timestamp NULL DEFAULT NULL,
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `work_id` int(11) DEFAULT NULL,
    `upload_time` datetime NOT NULL,
    `upload_result` int(11) DEFAULT NULL,
    """
    __tablename__ = 'GB_Metadata_Track'
    id: Column = Column(Integer, primary_key=True, autoincrement=True)
    work_id = Column(Integer, ForeignKey('Works.workId'))
    upload_time = Column(TIMESTAMP)
    upload_result = Column(Integer)

#    work = relationship('Works', back_populates='gb_metadata')

    create_time = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __repr__(self):
        return f"<id: {self.id} upload time:{self.upload_time} work: {self.work}>"


class GbContent(Base):
    """
    Records the steps in an **image group's** process. Captures the steps that **this service**
    has performed
    """
    __tablename__ = 'GB_Content_Track'
    id = Column(Integer, primary_key=True, autoincrement=True)
    volume_id = Column(Integer, ForeignKey('Volumes.volumeId'))
    job_step = Column(String(45))
    step_time = Column(DateTime)
    step_rc = Column(Integer)
    gb_log = Column(LONGTEXT)

    volume = relationship('Volumes', back_populates='gb_content')

    create_time = Column(TIMESTAMP, nullable=False, server_default=sqlalchemy.func.now())
    update_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __repr__(self):
        return f"<id: {self.id} step: {self.job_step} step time {self.step_time} volume:{self.volume}"

class GbState(Base):
    """
    Records raw google book data as we poll for it. Captures the state of Google's processing
    volume_id   int  FK Volumes.volumeId
    job_state    varchar(45)    -- name of the page reporting this activity
    state_date  datetime        -- observation datetime
    gb_log      longtext        -- other columns in the row, as json dict. The programmer has to manually
                                    determine the columns from the visual page - they do not come down in the
                                    text version
    """
    __tablename__ = 'GB_Content_State'
    volume_id = Column(Integer,  ForeignKey('Volumes.volumeId'), primary_key=True)
    job_state = Column(String(45), primary_key=True)
    gb_log = Column(LONGTEXT)
    state_date = Column(TIMESTAMP, primary_key=True)

    volume = relationship('Volumes', back_populates='gb_state')

    create_time = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    def __repr__(self):
        return f"<volume: {self.volume} state:{self.state}>"


class GbDownload(Base):
    __tablename__ = "GB_Downloads"
    id: Column = Column(Integer, primary_key=True, autoincrement=True)
    volume_id = Column(Integer, ForeignKey('Volumes.volumeId'))
    download_object_name = Column(String(255))
    download_path = Column(String(255))
    download_time = Column(TIMESTAMP)
    create_time = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    update_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    volume = relationship('Volumes', back_populates='gb_downloads')

    def __repr__(self):
        return f"<volume: {self.volume.label} path: {self.download_path} time: {self.download_time}>"

class GbReadyTrack(TimestampMixin, Base):
    """
    Queue of items ready to be acted on
    """
    __tablename__ = 'GB_Ready_Track'
    target_id = Column(Integer, comment='Id in specific tabel, varies with activity')
    activity = Column(String(50), comment="Supported activities: download unpack")


class GbUnpack(TimestampMixin, Base):
    __tablename__ = "GB_Unpack"
    volume_id = Column(Integer, ForeignKey('Volumes.volumeId'))
    unpack_object_name = Column(String(255))
    unpacked_path = Column(String(255))
    unpack_time = Column(TIMESTAMP)
    volume = relationship('Volumes', back_populates='gb_unpack')


class GbDistribution(TimestampMixin, Base):
    """
    Records the steps in an **image group's** process. Captures the steps that **this service**
    has performed
    """
    __tablename__ = 'GB_Distribution'

    volume_id = Column(Integer, ForeignKey('Volumes.volumeId'))
    dist_time = Column(TIMESTAMP)
    src = Column(String(255))
    dest = Column(String(255))

    volume = relationship('Volumes', back_populates='gb_dist')

    def __repr__(self):
        return f"<id: {self.id} dist_time {self.dist_time} volume:{self.volume}>"


