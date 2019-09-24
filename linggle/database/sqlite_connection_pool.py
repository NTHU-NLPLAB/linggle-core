from queue import Queue
import sqlite3


class SqliteConnectionPool:
    def __init__(self, db_file=":memory:", init_size=4):
        self.db_file = db_file
        self.conn_queue = Queue()
        self.size = init_size
        for _ in range(init_size):
            self.conn_queue.put(sqlite3.connect(self.db_file))

    def _get_conn(self):
        while True:
            conn = self.conn_queue.get()
            if conn:
                return conn
            # TODO: wait

    def execute(self, *args, **kwargs):
        conn = self._get_conn()
        r = conn.execute(*args, **kwargs)
        return r
