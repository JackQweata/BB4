from sqlalchemy import create_engine, Column, Integer, ForeignKey, String, Table, BigInteger
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import config

engine = create_engine(config.BD_CONNECT)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

problem_topic_association = Table(
    'problem_topic_association',
    Base.metadata,
    Column('problem_id', Integer, ForeignKey('problems.id'), primary_key=True),
    Column('topic_id', Integer, ForeignKey('topic_problems.id'), primary_key=True)
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    telegram = Column(BigInteger)
    last_message = Column(BigInteger)


class Problems(Base):
    __tablename__ = 'problems'

    id = Column(Integer, primary_key=True)
    contestId = Column(String(35))
    title = Column(String(150))
    count_solutions = Column(Integer)

    complexity_id = Column(Integer, ForeignKey('complexity.id'))
    complexity = relationship("Complexity")
    topics = relationship('TopicProblems', secondary=problem_topic_association, back_populates='problems')


class Complexity(Base):
    __tablename__ = 'complexity'

    id = Column(Integer, primary_key=True)
    values = Column(Integer)


class TopicProblems(Base):
    __tablename__ = 'topic_problems'

    id = Column(Integer, primary_key=True)
    values = Column(String(150))

    problems = relationship('Problems', secondary=problem_topic_association, back_populates='topics')

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.id == other.id


Base.metadata.create_all(engine)
