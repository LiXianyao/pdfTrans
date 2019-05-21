#-*-encoding:utf8-*-#

from entity_mark import EntityMark
from relation_mark import RelationMark
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
    for row in data:
        nrows += 1
        content = "".join([ seg.strip() for seg in row])
        newEntity = EntityMark(content)
        entityList.append(newEntity)
    db_session.add_all(entityList)
    db_session.commit()
    del entityList[:]
    print u"----> 实体数据存储完毕，总共存储数据%d行" % (nrows)

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
        try:  # 利用关系编号测试数据行是否有问题
            content = "".join([ seg.strip() for seg in row[:-2]])
            relation_no = row[-1].strip()
            relation_no = int(relation_no)
            assert (relation_no >0)
        except:
            print u"--->>!!第%d行数据发现异常，请检查，异常数据如下: " % (nrows)
            print "".join(row)
            continue
        newRelation = RelationMark(content, relation_no)
        relationList.append(newRelation)
        cnt_suc += 1
    db_session.add_all(relationList)
    db_session.commit()
    del relationList[:]
    print u"----> 关系数据存储完毕，总共存储数据%d行，数据异常共%d行" % (cnt_suc, nrows - cnt_suc)


if __name__=="__main__":
    dir = "20190512"
    entity2mysql(dir)
    relation2mysql(dir)
