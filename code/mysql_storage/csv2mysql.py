#-*-encoding:utf8-*-#

from entity_mark import EntityMark
from relation_mark import RelationMark
from ver_statement import VerStatement
from database import db_session
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

csv_dir = "../../csv/"
def entity2mysql(time_dir):
    file_path = csv_dir + "entity/%s/entity.csv"%(time_dir)
    f = open(file_path, "r")
    data = csv.reader(f)
    nrows = 0
    entityList = []
    print u"----> 开始存储实体数据..."
    duplicate_cnt = 0
    for row in data:
        nrows += 1
        pdf_path = row[0].strip()
        pdf_page = int(row[1].strip())
        mark_id = int(row[2].strip())
        statement = db_session.query(VerStatement).filter(
            VerStatement.pdf_path == pdf_path,
            VerStatement.pdf_no   == pdf_page,
            VerStatement.mark_id  == mark_id
        ).first()
        if statement != None: ## 一般情况下不该存在同名元组
            duplicate_cnt += 1
            continue
        statement = VerStatement(pdf_no=pdf_page, pdf_path=pdf_path, mark_id = mark_id)
        db_session.add(statement)
        db_session.commit()

        stat_id = statement.id

        content = "".join([ seg.strip() for seg in row[3:]])
        newEntity = EntityMark(content, stat_id)
        entityList.append(newEntity)
    db_session.add_all(entityList)
    db_session.commit()
    del entityList[:]
    print u"----> 实体数据存储完毕，总共存储数据%d行, 冲突id共%d行" % (nrows, duplicate_cnt)

def relation2mysql(time_dir):
    file_path = csv_dir + "relation/%s/relation.csv"%(time_dir)
    f = open(file_path, "r")
    data = csv.reader(f)
    nrows = 0
    relationList = []
    print u"----> 开始存储关系数据..."
    cnt_suc = 0
    for row in data:
        nrows += 1
        pdf_path = row[0].strip()
        pdf_page = int(row[1].strip())
        mark_id = int(row[2].strip())
        statement = db_session.query(VerStatement).filter(
            VerStatement.pdf_path == pdf_path,
            VerStatement.pdf_no   == pdf_page,
            VerStatement.mark_id  == mark_id
        ).first()
        assert (statement != None) # 必须存在对应的entity

        stat_id = statement.id
        relation_no = row[4].strip()
        relation_no = int(relation_no)
        content = "".join([ seg.strip() for seg in row[5:]])

        newRelation = RelationMark(content, relation_no, stat_id)
        relationList.append(newRelation)
        cnt_suc += 1
    db_session.add_all(relationList)
    db_session.commit()
    del relationList[:]
    print u"----> 关系数据存储完毕，总共存储数据%d行，数据异常共%d行" % (cnt_suc, nrows - cnt_suc)


if __name__=="__main__":
    dir = "20190609"
    entity2mysql(dir)
    relation2mysql(dir)
