#!/usr/bin/env python
# -*- coding: utf-8 -*-
from starlette.responses import UJSONResponse
from fastapi import FastAPI, Header

import firebase_admin
from firebase_admin.auth import verify_id_token
import psycopg2
import os


INSERT_CMD = "INSERT INTO access_log VALUES(%s, %s, %s, to_timestamp(%s/1000.0));"


settings = {
    'dbname': os.environ.get('PGDATABASE', 'linggle'),
    'host': os.environ.get('PGHOST', 'localhost'),
    'user': os.environ.get('PGUSER', 'linggle'),
    'password': os.environ.get('PGPASSWORD', ''),
    'port': int(os.environ.get('PGPORT', 5432))
}


app = FastAPI()
# cred = credentials.Certificate(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
firebase_admin.initialize_app()
conn = psycopg2.connect(**settings)


@app.get("/log/{action}/{query:path}", response_class=UJSONResponse)
def log_access(action: str, query: str, time: int = None, usertokenid: str = Header(None)):
    uid = verify_id_token(usertokenid)['uid'] if usertokenid else None
    return add_log(action, query, uid, time)


def add_log(action, query, uid=None, time=None):
    with conn.cursor() as cursor:
        res = cursor.execute(INSERT_CMD, (action, query, uid, time))
        conn.commit()
        return res
