# external modules used
import os
import sqlalchemy as sqla
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import QueuePool


# path to database file
DB_path = os.path.join(os.getcwd(), 'database', 'database.db')


# this function creates 2 database engines, one in RAM and one is secondary storage
def create_engines(echo):
    # echo means, should all the queries be printed out
    
    # caution with below code, could cause unexpected behavior if not thread safe, further research needed
    # I don't know much about threading in python, I find it confusing due to complexities around the global interpreter lock
    # as a result I had to just try various arguments to create these engines in a way that allowed me to use them with my flask server
    persistent_DB_engine = sqla.create_engine(
        'sqlite:///' + DB_path,
        echo=echo,
        poolclass=QueuePool,
        connect_args={'check_same_thread': False}
    )

    volatile_RAM_engine = sqla.create_engine(
        "sqlite:///:memory:",
        echo=echo,
        poolclass=QueuePool,
        connect_args={'check_same_thread': False}
    )
    return {
        "persistent_DB_engine": persistent_DB_engine,
        "volatile_RAM_engine": volatile_RAM_engine
    }


# this function safely terminates the database connection
def end_engines(engines):
    for engine in engines.values():
        engine.dispose()

# this function creates a session to access the database
def create_session(engine):
    return scoped_session(sessionmaker(bind=engine))

# this function safely ends a session
def end_session(session):
    session.commit()
    session.close()

