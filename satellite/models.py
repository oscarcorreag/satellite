import uuid
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel


class EventErrComm(DjangoCassandraModel):
    uid_ev = columns.TimeUUID(primary_key=True, default=uuid.uuid1)
    eve_name = columns.Text()
    mis_clock = columns.BigInt()
    seq_number = columns.Integer()


class HelloComm(DjangoCassandraModel):
    uid_he = columns.TimeUUID(primary_key=True, default=uuid.uuid1)
    battery = columns.Text()
    boom1_vbus = columns.Text()
    boom2_vbus = columns.Text()
    mis_clock = columns.BigInt()
    mts_vbus = columns.Text()
    n15v_tm = columns.BigInt()
    ope_mode = columns.Text()
    p15v_tm = columns.BigInt()
    p3v3_tm = columns.BigInt()
    p5v_tm = columns.BigInt()
    rw_p5v = columns.BigInt()
    seq_number = columns.Integer()
    ttc_stat = columns.Text()


class HouseKeepComm(DjangoCassandraModel):
    uid_hk = columns.TimeUUID(primary_key=True, default=uuid.uuid1)
    battery = columns.Text()
    boom1_vbus = columns.Text()
    boom2_vbus = columns.Text()
    mis_clock = columns.BigInt()
    mts_vbus = columns.Text()
    n15v_tm = columns.BigInt()
    ope_mode = columns.Text()
    p15v_tm = columns.BigInt()
    p3v3_tm = columns.BigInt()
    p5v_tm = columns.BigInt()
    rw_p5v = columns.BigInt()
    seq_number = columns.Integer()
    ttc_stat = columns.Text()
