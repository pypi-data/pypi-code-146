#!/usr/bin/env python
import ssl

import aiomysql

from vps.auth import Accounts

ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ctx.load_verify_locations(cafile=Accounts.ssl_cert)
dbname = "vpsstatus"

async def create_pool():
    return await aiomysql.create_pool(
        host=Accounts.host,
        port=3306,
        user=Accounts.username,
        password=Accounts.password,
        db=Accounts.database,
        ssl=ctx,
    )

async def load_data(key:str, limits:int=10000):
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT * FROM {} WHERE `key` = '{}' ORDER BY `id` DESC LIMIT {}".format(dbname, key, limits))
            resp = await cur.fetchall() 
            return resp


async def delete_old_than_hours(hours:int=1):
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            cmd = 'DELETE FROM {} WHERE `create_time` < DATE_SUB(NOW(), INTERVAL {} HOUR)'.format(dbname, hours)
            resp = await cur.execute(cmd)
            await conn.commit()
            return resp

async def insert_once(key: str, value: str):
    pool = await create_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            cmd = 'INSERT INTO {} (`key`, `value`) VALUES ("{}", "{}") ON DUPLICATE KEY UPDATE `value` = "{}"'.format(dbname, key, value, value)
            resp = await cur.execute(cmd)
            await conn.commit()
            return resp
