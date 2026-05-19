from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库URL：使用SQLite文件数据库
# sqlite:/// 表示在当前目录创建 blog.db 文件
DATABASE_URL = "sqlite:///./blog.db"

# 创建数据库引擎
# connect_args={"check_same_thread": False} 是 SQLite 必需参数（允许多线程访问）
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# 监听连接事件，开启外键约束
# SQLite 默认关闭外键，需要手动执行 PRAGMA foreign_keys=ON
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# 创建会话工厂
# autocommit=False: 不会自动提交，需要手动 db.commit()
# autoflush=False: 不会自动刷新，减少不必要的数据库查询
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类，所有模型都继承这个类
Base = declarative_base()

# 依赖注入函数：供 FastAPI 路由使用
def get_db():
    """
    每次请求时创建一个新的数据库会话
    请求结束后自动关闭
    使用 yield 确保即使发生异常也会关闭连接
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
