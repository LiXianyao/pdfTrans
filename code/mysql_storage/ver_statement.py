# -*- coding: utf-8 -*-
from sqlalchemy import Column,String, Integer, ForeignKey, Date, Text, Boolean
from database  import Base,db_session
class VerStatement(Base):

    #表名
    __tablename__ ='ver_statement'
    #表结构
    id = Column(Integer,autoincrement=True, primary_key=True)
    mark_user = Column(String, nullable=True) # 数据的标记人
    pdf_no = Column(Integer, nullable=False) # pdf的页码
    pdf_path = Column(String, nullable=False)  # pdf的文件名
    mark_id = Column(Integer, nullable=False)  # 由pdf_path、pdf_no和mark_id构成一个独立三元组
    state = Column(Integer, default=0)  # 3种状态，未审核、审核中、审核完毕
    user_id = Column(Integer, nullable=True)  # 是审核数据的人的id！不是数据上传人
    # 查询构造器、、、
    query = db_session.query_property()

    def __init__(self, pdf_no, pdf_path, mark_id, mark_user=None):
        self.pdf_no = pdf_no
        self.pdf_path = pdf_path
        self.mark_id = mark_id
        if mark_user:
            self.mark_user = mark_user

    def __repr__(self):
        statement_dict = {
            u"pdf_no": self.pdf_no,
            u"pdf_path": self.pdf_path,
            u"stat_id": self.id
        }
        return str(statement_dict)

    def __dir__(self):
        statement_dict = {
            u"pdf_no": self.pdf_no,
            u"pdf_path": self.pdf_path,
            u"stat_id": self.id
        }
        return str(statement_dict)

