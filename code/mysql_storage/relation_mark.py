# -*- coding: utf-8 -*-
from sqlalchemy import Column,String, Integer, ForeignKey, Date, Text, Boolean
from database import Base,db_session
class RelationMark(Base):

    #表名
    __tablename__ ='relation_mark'
    #表结构
    id = Column(Integer,autoincrement=True, primary_key=True)
    content = Column(Text, nullable=False)
    passed = Column(Boolean, default=False)  # 是否审核通过
    relation_no = Column(String(255), nullable=True)
    relation_name = Column(String(255), nullable=True)
    reviewed = Column(Boolean, default=False)  # 是否被审核过
    ver_date = Column(Date, nullable=True)
    user_id = Column(Integer, nullable=True)  # 是审核数据的人的id！不是数据上传人
    # 查询构造器、、、
    query = db_session.query_property()

    def __init__(self, content, relation_name, relation_no):
        self.content = content
        self.relation_name = relation_name
        self.relation_no = relation_no

    def __repr__(self):
        relation_dict = {
            u"relation_no": self.relation_no,
            u"relation_name": self.relation_name,
            u"content": self.content
        }
        return str(relation_dict)

    def __dir__(self):
        relation_dict = {
            u"relation_no": self.relation_no,
            u"relation_name": self.relation_name,
            u"content": self.content
        }
        return str(relation_dict)

