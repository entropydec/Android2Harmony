from orm.DatabaseModels import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session


class SqlHelper:
    engine = create_engine('mysql+pymysql://root:root@127.0.0.1:3306/se_project?charset=utf8')

    @classmethod
    def get_entity(cls, table_cls: Base, **kwargs):
        with cls.create_session() as session:
            entity = session.query(table_cls).filter_by(**kwargs).first()
            return entity

    @classmethod
    def get_entities(cls, table_cls: Base, **kwargs):
        with cls.create_session() as session:
            entities = session.query(table_cls).filter_by(**kwargs).all()
            return entities

    @classmethod
    def exists(cls, table_cls: Base, **kwargs):
        with cls.create_session() as session:
            return session.query(table_cls).filter_by(**kwargs).scalar() is not None

    @classmethod
    def add(cls, table_cls: Base, **kwargs):
        with cls.create_session() as session:
            session.add(table_cls(**kwargs))
            session.commit()

    @classmethod
    def add_return_key(cls, table_cls: Base, primary_key, **kwargs):
        with cls.create_session() as session:
            obj = table_cls(**kwargs)
            session.add(obj)
            session.flush()
            key = eval(f"obj.{primary_key}")
            session.commit()
            return key

    @classmethod
    def add_all(cls, table_cls: Base, *args):
        objects = [table_cls(**kwargs) for kwargs in args]
        with cls.create_session() as session:
            session.add_all(objects)
            session.commit()

    @classmethod
    def delete(cls, table_cls, **kwargs):
        with cls.create_session() as session:
            session.query(table_cls).filter_by(**kwargs).delete()
            session.commit()

    @classmethod
    def update(cls, table_cls, new_fields, **kwargs):
        with cls.create_session() as session:
            session.query(table_cls).filter_by(**kwargs).update(new_fields)
            session.commit()

    @classmethod
    def init_db(cls, override=False):
        # 在这里导入定义模型所需要的所有模块，这样它们就会正确的注册在
        # 元数据上。否则你就必须在调用 init_db() 之前导入它们。
        from orm.DatabaseModels import Base
        if override:
            Base.metadata.drop_all(bind=cls.engine)
        Base.metadata.create_all(bind=cls.engine)

    @classmethod
    def create_session(cls) -> Session:
        try:
            session_factory = sessionmaker(bind=cls.engine)
            print('successfully created an sqlsession')
            Session = scoped_session(session_factory)
            return Session()  # it will create a thread-local session
        except Exception as e:
            print(e)
            print('fail to created an sqlsession')


if __name__ == '__main__':
    SqlHelper.init_db(True)
    from orm.DatabaseModels import TableUser

    SqlHelper.add(TableUser, email='root', name='root', pwd='root', priority=0,
                  max_buffer_size=314572800)
