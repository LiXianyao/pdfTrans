#-*-encoding:utf8-*-#

from entity_mark import EntityMark
from relation_mark import RelationMark
from database import db_session
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

csv_dir = "../../csv/"
def entity2mysql(time_dir):
    file_path = csv_dir + "entity/%s/entity.csv"%(time_dir)
    f = open(file_path, "r")
    data = pd.read_csv(f, header=-1)
    nrows = len(data)
    entityList = []
    print u"----> 开始存储实体数据..."
    for row in range(nrows):
        content = data[0][row].strip()
        newEntity = EntityMark(content)
        entityList.append(newEntity)
    db_session.add_all(entityList)
    db_session.commit()
    del entityList[:]
    print u"----> 实体数据存储完毕，总共存储数据%d行" % (nrows)

def relation2mysql(time_dir):
    file_path = csv_dir + "relation/%s/relation.csv"%(time_dir)
    f = open(file_path, "r")
    data = pd.read_csv(f, header=-1, converters={0:str, 1:str, 2:str})
    nrows = len(data)
    relationList = []
    print u"----> 开始存储关系数据..."
    cnt_suc = 0
    for row in range(nrows):
        content = data[0][row].strip()
        relation_name = data[1][row].strip()
        relation_no = data[2][row].strip()
        try: # 利用关系编号测试数据行是否有问题
            relation_no = int(relation_no)
            assert (relation_no >0)
        except:
            print u"--->>!!第%d行数据发现异常，请检查，异常数据如下: " % (row)
            print data.iloc[row]
            continue
        newRelation = RelationMark(content, relation_name, relation_no)
        relationList.append(newRelation)
        cnt_suc += 1
    db_session.add_all(relationList)
    db_session.commit()
    del relationList[:]
    print u"----> 关系数据存储完毕，总共存储数据%d行，数据异常共%d行" % (cnt_suc, nrows - cnt_suc)


if __name__=="__main__":
    dir = "20190501"
    #entity2mysql(dir)
    relation2mysql(dir)