# -*- coding:utf-8 -*_
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker
import time
import ConfigParser
cf = ConfigParser.ConfigParser()
cf.read("supervisor.conf")
DB_FILE = cf.get("supervisor", "DB_FILE")
engine = create_engine('sqlite:///' + DB_FILE, connect_args={'check_same_thread': False}, convert_unicode=True)
Base = declarative_base()

class File(Base):

    __tablename__= 'filescheck'
    # 指定id映射到id字段; id字段为整型，为主键
    id = Column(Integer, primary_key=True)
    # 指定name映射到name字段; name字段为字符串类形，
    filename = Column(String(255))
    hash = Column(String(32))
    type = Column(String(10))
    check_result = Column(String(10))
    created_at = Column(String(32))
    def __repr__(self):
        return "<User(filename='%s', hash='%s', type='%s', check_result='%s', created_at='%s')>" % (
                   self.filename, self.hash, self.type, self.check_result, self.created_at)


# Session = sessionmaker(bind=engine)
# # session = Session()
# # a_flie = session.query(File).filter_by(hash='md5sum').first()
# # print (a_flie)
# # # ed_file = File(filename='event.src_path', hash='aaaa1111', created_at=time.strftime('%Y-%m-%d %H:%M:%S'))
# # # session.add(ed_file)
# # session.commit()
# # session.close()
