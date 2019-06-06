# -*- coding: utf-8 -*-
from sqlalchemy import Column,String, Integer, ForeignKey, Date, Text, Boolean
from database  import Base,db_session
class EntityMark(Base):

    #表名
    __tablename__ ='entity_mark'
    #表结构
    id = Column(Integer,autoincrement=True, primary_key=True)
    content = Column(Text, nullable=False)
    origin_content = Column(Text, nullable=False)
    passed = Column(Integer, default=-1)  # 是否审核通过
    reviewed = Column(Integer, default=0)  # 是否被审核过
    ver_date = Column(Date, nullable=True)
    stat_id = Column(Integer, nullable=False) # 与ver_statement关联的主键，唯一标识一句原文
    description = Column(String, nullable=True) # 审核意见
    verify_result = Column(Integer, nullable=False, default=-1) # 审核结果标识，-1是未审核，0~3分别为：接受、修改后接受、拒绝、修改后拒绝

    # 查询构造器、、、
    query = db_session.query_property()

    def __init__(self, content, stat_id):
        self.content = content
        self.origin_content = content
        self.stat_id = stat_id

    def __repr__(self):
        entity_dict = {
            u"content": self.content,
            u"origin_content": self.origin_content,
            u"stat_id": self.stat_id
        }
        return str(entity_dict)

    def __dir__(self):
        entity_dict = {
            u"content": self.content,
            u"origin_content": self.origin_content,
            u"stat_id": self.stat_id
        }
        return str(entity_dict)

