__version__ = '0.1.0'

import os
import jaydebeapi
from typing import List
from typing import Union

URL = {
    'DEV': 'jdbc:as400://seep900t/M3FDBDEV',
    'PRD': 'jdbc:as400://seep300v/M3FDBPRD',
    'TST': 'jdbc:as400://seep900t/M3FDBTST'
}

def connect(url: str, *args: List[Union[str, int, float]]) -> jaydebeapi.Connection:
    """
    url: str - The connection URL, jdbc:as400://[server]/[environment]
    args: args required by the server, such as username and password.
    
    Additional Notes:
    The url string will always be used to look-up the global URL dict,
    if a match is found, the url will be fetched from the dict. If no
    match the url will be passed along to the jaydebeapi.connect function.
    
    The *args are the driver_args list. For the M3 DB2 database, the
    first two arguments are user and password. Rest I do not know, and
    I have not found the docs for this.
    
    The function returns a jaydebe.Connection object which supports the
    use of a contect manager, which is the reconmended way, to ensure that
    the connection is closed after usage.
    
    Not passing the username and password will cause a java dialog to pop-up
    and ask for the credentials. Some times this will keep the python
    interpreter, so best to pass the user name and password as *args. 
    
    Example:
    ---------------------------------------------------------------------
    with connect('TST', 'nnckten', 'password') as conn:
        cursor = conn.cursor()
        cursor.execute("select * from ooline limit 1")
        print(cursor.fetchall())
    """
   
    try:
        url = URL[url]
        
    except KeyError:
        pass
                
    return jaydebeapi.connect(
        jclassname="com.ibm.as400.access.AS400JDBCDriver",
        url=url,
        driver_args=args,
        jars=''.join([os.path.dirname(__file__), '\\', 'jt400.jar'])
        #jars='./m3query/jt400.jar'
    )

