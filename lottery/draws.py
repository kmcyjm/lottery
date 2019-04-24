
from sqlalchemy import Column, Integer, Date

from lottery.sqlalchemy_base import Base


class Draws(Base):
    """
    This Draws class is a representation of the 'draws' table
    """
    __tablename__ = 'draws'

    date = Column(Date, primary_key=True)
    newball1 = Column(Integer)
    newball2 = Column(Integer)
    newball3 = Column(Integer)
    newball4 = Column(Integer)
    newball5 = Column(Integer)
    luckystar1 = Column(Integer)
    luckystar2 = Column(Integer)

    def __init__(self, date, newball1, newball2, newball3, newball4, newball5, luckystar1, luckystar2):
        self.date = date
        self.newball1 = newball1
        self.newball2 = newball2
        self.newball3 = newball3
        self.newball4 = newball4
        self.newball5 = newball5
        self.luckystar1 = luckystar1
        self.luckystar2 = luckystar2
