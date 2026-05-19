from database import engine, Base
from models import Category, Article  # 导入模型，确保被注册到 Base

def init_database():
    """初始化数据库：创建所有表"""
    print("正在创建数据库表...")
    
    # 创建所有继承自 Base 的表
    Base.metadata.create_all(bind=engine)
    
    print("✅ 数据库表创建成功！")
    print("表列表:", Base.metadata.tables.keys())

if __name__ == "__main__":
    init_database()
