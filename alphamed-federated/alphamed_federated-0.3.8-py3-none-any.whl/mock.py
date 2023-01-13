import sqlite3
from hashlib import sha1
from typing import List, Optional
from uuid import uuid4

from .loggers import logger

__all__ = ['mock_context', 'is_mock_mode', 'mock_node_id', 'mock_nodes']


_MOCK_DB = '.mock.db'
_mock_conn = sqlite3.connect(_MOCK_DB, check_same_thread=False)
_mock_conn.row_factory = sqlite3.Row
_mock_cur = _mock_conn.cursor()


def _table_exists(name: str):
    try:
        _mock_cur.execute(f'SELECT 1 FROM `{name}`')
        return True
    except sqlite3.OperationalError:
        return False


def _init_mock_db():
    _mock_cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS contracts (
            contract_id    INTEGER   PRIMARY KEY  AUTOINCREMENT,
            target         CHAR(50)  NOT NULL,
            message_title  CHAR(50)  NOT NULL,
            content        TEXT      NOT NULL,
            message_time   INT       NOT NULL,
            channel        CHAR(20)  NOT NULL
        )
        '''
    )
    _mock_cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS contract_consume_cursors (
            cursor_id    INT       PRIMARY KEY,
            node_id      CHAR(50)  NOT NULL,
            cursor       INT       NOT NULL
        )
        '''
    )
    _mock_cur.connection.commit()


class mock_context:

    __mock_mode = False
    __nodes = []
    __node_id = None

    def __init__(self,
                 clean: bool = False,
                 id: str = None,
                 nodes: List[str] = None) -> None:
        """Set running context into mock mode.

        Args:
            clean:
                Whether to clean all historical data, and begin from a very clean.
            id:
                A unique ID of the node this process mocks. If not specified, a random
                one will be assigned each time.
            nodes:
                The ID list of ALL node which take part in this mock task. If specified,
                query_nodes returns this list, otherwise it returns an empty list.
                It's all right to use all FAKE ID values but they must not be duplicate.
        """
        assert isinstance(clean, bool), f'clean must be a bool value instead of `{clean}`.'
        assert id is None or isinstance(id, str), f'id must be a str value instead of `{id}`.'
        assert (
            nodes is None or (isinstance(nodes, list)
                              and all(isinstance(_node, str) for _node in nodes))
        ), f'nodes must be a str list instead of `{nodes}`.'

        self.clean = clean
        self.id = id or str(uuid4())
        self.nodes = nodes

    def __enter__(self):
        mock_context._mock_context__mock_mode = True
        if self.nodes:
            mock_context._mock_context__nodes = self.nodes
        else:
            logger.warn('Without specifying nodes, query_nodes returns an empty list.')
        mock_context._mock_context__node_id = self.id

        if self.clean:
            _mock_cur.execute('DELETE FROM contract_consume_cursors WHERE 1=1')
            _mock_cur.execute('DELETE FROM contracts WHERE 1=1')
            _mock_cur.connection.commit()
        self._init_contract_cursor(node_id=self.id)

    def _init_contract_cursor(self, node_id: str):
        is_exist = _mock_cur.execute(
            'SELECT 1 FROM contract_consume_cursors WHERE node_id=?',
            (node_id,)
        ).fetchone()
        if is_exist is None:
            _mock_cur.execute(
                '''
                INSERT INTO contract_consume_cursors (node_id, cursor)
                VALUES (?, ?)
                ''',
                (node_id, 0)
            )
            _mock_cur.connection.commit()

    def __exit__(self, *exc):
        mock_context._mock_context__mock_mode = False
        mock_context._mock_context__nodes = []
        mock_context._mock_context__node_id = None


def is_mock_mode():
    return mock_context._mock_context__mock_mode


def mock_nodes():
    return mock_context._mock_context__nodes


def mock_node_id():
    return mock_context._mock_context__node_id


def _put_mock_contract(targets: List[str],
                       message_title: str,
                       content: str,
                       message_time: int,
                       channel: str) -> str:
    _mock_cur.executemany(
        '''
        INSERT INTO contracts (target, message_title, content, message_time, channel)
        VALUES (?, ?, ?, ?, ?)
        ''',
        [(_target, message_title, content, message_time, channel) for _target in targets]
    )
    _mock_cur.connection.commit()
    max_id = _mock_cur.execute(
        'SELECT MAX(contract_id) FROM contracts'
    ).fetchone()['MAX(contract_id)']
    return sha1(str(max_id).encode()).hexdigest()


def _get_mock_contract(node_id: str, channel: str) -> Optional[str]:
    cursor = _mock_cur.execute(
        'SELECT cursor FROM contract_consume_cursors WHERE node_id=?', (node_id,)
    ).fetchone()['cursor']
    contract = _mock_cur.execute(
        '''
        SELECT contract_id, content
        FROM contracts
        WHERE contract_id>:cursor
        AND (target=:node_id or target='*')
        AND channel=:channel
        ORDER BY contract_id
        ''',
        {'cursor': cursor, 'node_id': node_id, 'channel': channel}
    ).fetchone()
    if contract is None:
        return None

    new_cursor = contract['contract_id']
    _mock_cur.execute(
        'UPDATE contract_consume_cursors SET cursor=:new_cursor WHERE node_id=:node_id',
        {'new_cursor': new_cursor, 'node_id': node_id}
    )
    _mock_cur.connection.commit()
    return contract['content']


_init_mock_db()
