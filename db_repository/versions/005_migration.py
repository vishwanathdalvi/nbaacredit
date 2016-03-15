from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
co_po_map = Table('co_po_map', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('uniqueID', String(length=80)),
    Column('coursecode', String(length=64)),
    Column('coursename', String(length=120)),
    Column('facultyname_1', String(length=64)),
    Column('facultyname_2', String(length=64)),
    Column('facultyname_3', String(length=64)),
    Column('facultyname_4', String(length=64)),
    Column('classname', String(length=64)),
    Column('examsession', String(length=10)),
    Column('pointfaculty', String(length=64)),
    Column('whenmodified', DateTime),
    Column('whomodified', String(length=64)),
    Column('description', String(length=300)),
    Column('courseoutcome_1', String(length=300)),
    Column('courseoutcome_2', String(length=300)),
    Column('courseoutcome_3', String(length=300)),
    Column('courseoutcome_4', String(length=300)),
    Column('courseoutcome_5', String(length=300)),
    Column('courseoutcome_6', String(length=300)),
    Column('outcomeKlevel_1', String(length=10)),
    Column('outcomeKlevel_2', String(length=10)),
    Column('outcomeKlevel_3', String(length=10)),
    Column('outcomeKlevel_4', String(length=10)),
    Column('outcomeKlevel_5', String(length=10)),
    Column('outcomeKlevel_6', String(length=10)),
    Column('copocorr', PickleType),
    Column('coqcorr', PickleType),
    Column('bool_done', Integer),
    Column('bool_uploaded', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['co_po_map'].columns['bool_uploaded'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['co_po_map'].columns['bool_uploaded'].drop()
