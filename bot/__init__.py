from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


'''Comments before every execution'''
@event.listens_for(Engine, "before_cursor_execute")
def comment_sql_calls(conn, cursor, statement, parameters,
                                    context, executemany):
    print('executing: ' + statement + ' with parameters: ' + str(parameters))

'''Creating an engine'''
engine = create_engine("sqlite+pysqlite:///:memory:", echo=False, future=True)

db=Session(engine)

def run_app():
    
    pass