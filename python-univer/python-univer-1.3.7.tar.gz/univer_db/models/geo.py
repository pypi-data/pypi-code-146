from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from univer_db.orm import get_base


Base = get_base()


class AbiturientRegAtsType(Base):
    """
    Тип адреса абитуриента
    """
    __tablename__ = 'abiturient_reg_ats_types'

    # Идентификатор
    id = Column(Integer, primary_key=True)

    # Наименование
    value_ru = Column(String(100))
    value_kz = Column(String(100))
    value_en = Column(String(100))

    # Код
    code = Column(Integer)

    # Актуальный
    actual = Column(Integer)

    def __repr__(self):
        return f'<AbiturientRegAtsType {self} (id={self.id} code={self.code} actual={self.actual})>'
    
    def __str__(self):
        return self.value_ru


class AbiturientRegAts(Base):
    """
    Адрес абитуриента
    """
    __tablename__ = 'abiturient_reg_ats'

    # Идентификатор
    id = Column(Integer, primary_key=True)

    # Родитель
    parent_id = Column(ForeignKey('abiturient_reg_ats.id'))
    parent = relationship('AbiturientRegAts', remote_side=[id])

    # Родители
    parents = Column(String(100))

    # Тип
    type_id = Column('d_ats_type_id', ForeignKey('abiturient_reg_ats_types.id'))
    type = relationship('AbiturientRegAtsType')

    # Наименование
    name_ru = Column('name_rus', String(240))
    name_kz = Column('name_kaz', String(240))
    name_en = Column('name_eng', String(240))

    # RCO
    rco = Column(String(20))

    # КАТО
    cato = Column(String(20))

    # Актуальный
    actual = Column(Integer)

    def __repr__(self):
        return f'<AbiturientRegAts {self} (id={self.id} parent_id={self.parent_id} type_id={self.type_id} actual={self.actual})>'
    
    def __str__(self):
        return self.name_ru
