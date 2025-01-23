from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    """基础模型类"""
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        """自动生成表名"""
        return cls.__name__.lower()
