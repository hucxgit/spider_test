#coding=utf-8
import sys
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.Utils.Utils import Utils

reload(sys)
sys.setdefaultencoding('utf8')

class DaoMapper(object):
    
    """docstring for DaoMapper"""
    def __init__(self,db=None):
        super(DaoMapper, self).__init__()
        util = Utils(env="DEV")
        # 初始化数据库连接:
        db = util.db if db is None else db
        url = 'mysql+mysqlconnector://'+util.root+':'+util.password+'@'+util.host+'/'+db+"?charset=utf8"
        print(url)
        engine = create_engine(url,echo=True,pool_size=5)
        # 创建DBSession类型:
        DBSession = sessionmaker(bind=engine)

        self.DBSession = DBSession

    def operationUpdateSql(self, sql=None):
        t0 = time.time()
        try:
            # 创建session对象:
            session = self.DBSession()
            # 添加到session:
            session.execute(sql.encode('utf-8'))
            session.commit()
        except Exception as e:
            print("update20 exception")
            print(e)
            pass
        finally:
            print("finally")
            # 关闭session:
            session.close()
        print("update take time" + str(time.time() - t0) + " secs")
        pass
    #执行查找操作
    def operationSql(self,sql=None):
        t0 = time.time()
        try:
            # 创建session对象:
            session = self.DBSession()
            # 添加到session:
            result = session.execute(sql).fetchall()
            session.commit()
            return result
        except:
            pass
        finally:
            # 关闭session:
            print("finally")
            session.close()
        print("query take time" + str(time.time() - t0) + " secs")
        pass
    def operationQuery(self):
        from lib.Model import ExternalPointLongitudelatitude
        #ret = session.query(Users).filter_by(name='alex').all()
        t0 = time.time()
        try:
            # 创建session对象:
            session = self.DBSession()
            # 添加到session:
            result = session.query(ExternalPointLongitudelatitude).all()
            return result
        except:
            pass
        finally:
            # 关闭session:
            print("finally")
            session.close()
        print("operationQuery take time" + str(time.time() - t0) + " secs")
        pass

    #更新数据



    #insert数据    
    def insertObject(self,object=None):
        t0 = time.time()
        try:
            # 创建session对象:
            session = self.DBSession()
            # 添加到session:
            session.add(object)
            # 提交即保存到数据库:
            session.commit()
        except:
            pass
        finally:
            # 关闭session:
            session.close()
        print("insert take time" + str(time.time() - t0) + " secs")  
        pass  
    #批量插入数据    
    def insertObjects(self,objects=None):
        t0 = time.time()
        try:
            # 创建session对象:
            session = self.DBSession()
            session.bulk_save_objects(objects)
            session.commit()
        except:
            pass
        finally:
            # 关闭session:
            session.close()
        print("batch take time" + str(time.time() - t0) + " secs")  
        pass     
