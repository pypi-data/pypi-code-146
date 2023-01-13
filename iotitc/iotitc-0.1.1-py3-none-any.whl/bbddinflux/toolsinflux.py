"""
Modulo orientado a la realizacion de operaciones en InfluxDB
"""

from datetime import datetime
from typing import Tuple, Optional, Union, Any
from influxdb import DataFrameClient
import pandas as pd
from dateutil.parser import parse


class ToolInflux:
    """Clase encargada de realizar conexiones a InfluxDB y ciertas operaciones concurrentes.
    En el caso de que se desee obtener todas las funcionalidades de la libreria python, se
    puede usar el metodo get_client() para obtener el cliente de la conexion"""

    def __init__(
        self,
        database: str,
        ip_address: str = "localhost",
        port: int = 8086,
        user: str = "root",
        password: str = "root",
        timeout: int = 20,
    ):
        """Devuelve un objeto la cual ha establecido conexion con una base
        de datos en concreto

        :param ip_address: IP de la base de datoss
        :type ip_address: str
        :param database: Nombre de la base de datos
        :type database: str
        :param port: Puerto de conexion con la base de datos, por defecto es 8086
        :type port: int, optcional
        :param user: Nombre de usuario de la base de datos, por defecto es "root"
        :type user: str, opcional
        :param password: Contraseña de la base de datos, por defecto es "root"
        :type password: str, opcional
        :return: Conexion con la base de datos
        :rtype: influxdb.dataframe_client.DataFrameClient
        """
        self.ip_address = ip_address
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.timeout = timeout

        self.client = self.connect_to_database()

        # si no existe la base de datos especificada al instanciar la clase, la crea
        if not any(
            [
                True if x["name"] == self.database else False
                for x in self.client.get_list_database()
            ]
        ):
            self.client.create_database(self.database)

    def connect_to_database(self):
        """Estbalece conexion con la base de datos
        por si los metodos de la clase ToolInflux no presenta ciertas funcionalidades

        :return: Cliente Influxdb
        :rtype: influxdb.dataframe_client.DataFrameClient
        """
        client = DataFrameClient(
            self.ip_address,
            self.port,
            self.user,
            self.password,
            self.database,
            self.timeout,
        )
        return client

    def get_client(self):
        """Devuelve el cliente que ha establecido conexion con la base de datos
        por si los metodos de la clase ToolInflux no presenta ciertas funcionalidades

        :return: Cliente Influxdb
        :rtype: influxdb.dataframe_client.DataFrameClient
        """
        return self.client

    def close_client(self):
        """Funcion encargada de cerrar la conexion instanciada"""
        self.client.close()

    def write_dataframe(self, dataframe: pd.DataFrame, table: str):
        """Escribe datos en la base de datos instanciada y en una tabla determinada

        :param dataframe: Objeto que contiene los datos
        :type dataframe: pd.DataFrame
        :param table: Nombre de la tabla en la que se quiere registrar
        :type table: str
        """
        # normalizo el index para que siempre tenga un unico
        #  formato ya que eso se reflejan en las querys con python
        dataframe.index = pd.to_datetime(
            dataframe.index.map(lambda x: parse(str(x)).strftime("%Y-%m-%d %H:%M:%S"))
        )

        # y ahora registro los datos
        self.client.write_points(dataframe, table)

    def get_last_index(self, table: str) -> Union[datetime, None]:
        """Devuelve la fecha del ultimo registro de una tabla determinada

        :param table: Nombre de la tabla en la que se quiere registrar
        :type table: str
        :return: Objeto datetime en el caso de que la tabla exista y hayan datos.
        En caso contrario devuelve como valor el objeto None
        :rtype: Union[datetime, None]
        """
        try:
            # datetime_now = datetime.now()
            # try:
            # obtengo los nombres de las columnas de la tabla
            cols_table = self.client.query(f"SELECT LAST(*) FROM {table}")[
                table
            ].columns
            # elimino el prefijo "last_" que le añade influx
            cols_table = [x.split("last_")[-1] for x in cols_table]

            # creo un bucle que recorra la tabla, columna a columna para
            # pode robtener el index ya que si lo hago con mas de una columna
            # influx devuelve in index nulo (por defecto, año 1970)
            list_index = list()
            for feature in cols_table:
                query = f"SELECT LAST({feature}) FROM {table}"
                dataframe_query = self.client.query(query=query)[table]
                list_index.append(dataframe_query.index[0])

            # devuelvo el index mas reciente
            tmin = min(list_index)
            return parse(str(tmin.to_pydatetime()))

        except KeyError:  # error que se lanza porque no hay ningun registro
            return None

    def __get_table_with_window(
        self,
        table: str,
        measure: str = "*",
        window_time: Tuple[int, str] = (48, "h"),
        group_by: str = "2m",
        query: Optional[str] = None,
        format_index: Optional[str] = None,
    ) -> pd.DataFrame:
        """Funcion encargada de leer la base de datos InfluxDB y devolver los datos
        de una query determinada en formato DataFrame

        :param table: Nombre de la tabla
        :type table: str
        :param measure: Medidas de las tabla instanciada, por defecto "*".
                        Nota: solo admite por ahora una medida o "*"
        :type measure: str, opcional
        :param window_time: Periodo de tiempo que se desea seleccionar, por defecto (24, "h")
                            - s: segundos
                            - m: minutos
                            - h: horas
                            - w: semana
                            - M: mes
                            - y: Año
        :type window_time: tuple[int, str], opcional
        :param group_by: Configura la agrupación de los datos, por defecto "2m"
                         - s: segundos
                         - m: minutos
                         - h: horas
                         - w: semana
                         - M: mes
                         - y: Año
        :type group_by: str, opcional
        :param query: Si no es False se debe de introducir la query que se
                      desea aplicar, en caso contrario selecciona todos los datos.
                      Por defecto es False
        :type query: False | str, opcional
        :param format_index: Si no es False se debe de introducir el nuevo formato
                             que se desea aplicar al indice de la tabla, por defecto False
        :type format_index: False | str, opcional
        :return: DataFrame con los datos correspondiente a la query introducida
        :rtype: DataFrame
        """
        # en el caso de que salte un error...
        try:
            # si es falso...
            if isinstance(query, type(None)):
                if (
                    measure == "*"
                ):  # y quiero coger todas las columnas, aplico la siguiente query
                    # esta query dice: que seleccione la media de las variables * de la tabla x de
                    # las ultimas 24h (por defecto) y las agrupe esos valores medios en una ventana
                    # de datos de 2 minutos, ademas de que rellene los valores nulos
                    query_string = f'SELECT mean({measure}) FROM "{table}" \
                        WHERE time >= now() - {str(window_time[0])}{window_time[1]} and time <= now() \
                            GROUP BY time({group_by}) fill(null)'
                else:  # sino aplico esta otra query
                    # aqui la query es igual a la anterior pero si no se especifica *
                    # la sintaxis cambia ya que hay que poner dobles comillas en measure
                    query_string = f'SELECT mean("{measure}") FROM "{table}" \
                        WHERE time >= now() - {str(window_time[0])}{window_time[1]} and time <= now() \
                            GROUP BY time({group_by}) fill(null)'
            if isinstance(query, str):
                # en el caso que se quiera pasar una query personalizada 100%...
                query_string = query

            # obtengo el dataframe resultante
            df_query = self.client.query(query_string)[table]

            # modifico el formato del indice por si es de interes
            if isinstance(format_index, str):
                df_query.index = df_query.index.map(
                    lambda x: parse(str(x)).strftime(format_index)
                )

            return df_query
        except KeyError:  # si no hay esta tabla...
            # quiero que me devuelva un dataframe aunque sea vacio
            # ya que si o si quiero que me devuelva un dataframe
            return pd.DataFrame()

    def set_query(
        self,
        table: str,
        col: str = "*",
        selector: Optional[str] = None,
        aggregation: Optional[str] = None,
        time: Optional[Tuple[datetime, datetime]] = None,
        group_by: Optional[str] = None,
    ) -> str:
        """Devuelve una query lista para ejecutar en InfluxDB

        :param table: Nombre de la tabla en la que se quiere registrar
        :type table: str
        :param col: Especifica el nombre de columna. En el caso de que sea '*', eso quiere decir que selecciona todas las columnas. Por defecto '*'
        :type col: str, opcional
        :param selector: Tipo de selector que se quiere aplicar. Para mas informacion: https://runebook.dev/es/docs/influxdata/influxdb/v1.3/query_language/functions/index. Por defecto None
        :type selector: Optional[str], opcional
        :param aggregation: Tipo de operacion que se quiere aplicar. Para mas informacion: https://runebook.dev/es/docs/influxdata/influxdb/v1.3/query_language/functions/index. Por defecto None
        :type aggregation: Optional[str], opcional
        :param time: Especifica en formato datetime o string con formato de fecha desde donde se quieren extraer los datos (pasando solo una fecha) o si se desea extraer datos entre un periodo de fecha en concreto (pasando dos fechas: start and end), Por defecto None
        :type time: Optional[Tuple[datetime, datetime]], opcional
        :param group_by: Agrupacion de los datos que se desea realizar. Es obligatorio que tenga una operacion de agregacion especificada. Por defecto None
        :type group_by: Optional[str], opcional
        :return: Query lista para ejecutar en InfluxDB y obtener los datos
        :rtype: str
        """

        # funcion que pasa de str/datetime a timestamp
        # con el formato estrcito de grafana para la
        # query
        def datetime_to_timestamp_grafana(datetime_obj):
            if isinstance(datetime_obj, str):
                time_parse_or_dt = parse(datetime_obj)
            else:
                time_parse_or_dt = datetime_obj
            timestamp_wf = str(time_parse_or_dt.timestamp()).split(".")
            return int(timestamp_wf[0] + timestamp_wf[1][:3])

        # En esta version, o solo puede haber selector o aggregation
        if isinstance(selector, str) and isinstance(aggregation, type(None)):
            if col == "*":
                selector_q = f" {selector.upper()}({col}) "
            else:
                selector_q = f' {selector.upper()}("{col}") '
            aggregation_q = " "
            col_q = ""
        elif isinstance(aggregation, str) and isinstance(selector, type(None)):
            if col == "*":
                aggregation_q = f" {aggregation.upper()}({col}) "
            else:
                aggregation_q = f' {aggregation.upper()}("{col}") '
            selector_q = " "
            col_q = ""
        # en el caso de que no haya ningun selector o aggregation o hayan ambas
        # lo cual en esta version no esta permitido, comenta que se elimina ambas
        # operaciones y aplica simplemente SELECT *
        else:
            print(
                "En esta version solo se puede tener o un selector o una agregacion\n \
            Se configura selector & aggregation a ''"
            )
            selector_q = " "
            aggregation_q = " "
            col_q = f" {col} "

        # Si el time no es una tupla pero si un datetime o un strin con
        # formato de fecha, entra en el condicional
        if not isinstance(time, tuple):
            time_start = datetime_to_timestamp_grafana(time)
            # si solo hay una fecha se supone que estoy diciendo desde donde
            # quiero los datos y que me coja hasta el momento actual, now()
            time_q = f" WHERE time >= {time_start}ms and time <= now() "
        # en el caso de que si haya una tupla con dos valores, se supone
        # que estoy especificando un rango de fechas
        else:
            time_0 = datetime_to_timestamp_grafana(time[0])
            time_1 = datetime_to_timestamp_grafana(time[1])
            # verifico que el rango de fechas se paso primero
            # la fecha mas antigua y luego la fecha mas reciente
            if time_0 < time_1:
                time_start = time_0
                time_end = time_1
            else:
                time_start = time_1
                time_end = time_0
            time_q = f" WHERE time >= {time_start}ms and time <= {time_end}ms "

        # en el caso de que se haya añadido alguna operacion agregada ya que
        # ES OBLIGATORIO, especifico si quiero agruparlos con algun tipo de
        # frecuencia, por ejemplo: 10s, 3m, 4h, 10d
        if isinstance(group_by, str) and not aggregation_q == " ":
            group_by_q = f" GROUP BY time({group_by}) "
        else:
            group_by_q = " "

        # finalmente devuelvo la query ya construida
        return (
            "SELECT"
            + col_q
            + selector_q
            + aggregation_q
            + f"FROM {table}"
            + time_q
            + group_by_q
            + "fill(null)"
        )

    def __get_table_between_dates(
        self,
        table: str,
        start_date: Union[str, datetime],
        measure: str = "*",
        group_by: str = "2m",
        query: Optional[str] = None,
        format_index: Optional[str] = None,
    ) -> pd.DataFrame:
        """_summary_

        :param table: _description_
        :type table: str
        :param start_date: _description_
        :type start_date: Union[str,datetime]
        :param measure: _description_, Por defecto "*"
        :type measure: str, opcional
        :param group_by: _description_, Por defecto "2m"
        :type group_by: str, opcional
        :param query: _description_, Por defecto None
        :type query: Optional[str], opcional
        :param format_index: _description_, Por defecto None
        :type format_index: Optional[str], opcional
        :return: _description_
        :rtype: pd.DataFrame
        """
        # si es falso...
        if isinstance(query, type(None)) and start_date is not None:
            # paso el formato a datetime.datetime si o si
            if not isinstance(start_date, datetime):
                start_date_to_datetime = parse(start_date)
            else:
                start_date_to_datetime = start_date

            # lo convierto a timestamp con una longitud estricta de 13 numeros
            timestamp_wf = str(start_date_to_datetime.timestamp()).split(".")
            # cojo el primer elemento que es de 10 numeros + el segundo elemento
            # que selecciono solamente los 3 primeros numeros = 13
            timestamp = int(timestamp_wf[0] + timestamp_wf[1][:3])

            if measure == "*":
                # y quiero coger todas las columnas, aplico la siguiente query
                # esta query dice: que seleccione la media de las variables * de la tabla x de
                # las ultimas 24h (por defecto) y las agrupe esos valores medios en una ventana
                # de datos de 2 minutos, ademas de que rellene los valores nulos
                query_string = f'SELECT mean({measure}) FROM "{table}" \
                    WHERE time >= {timestamp}ms and time <= now() \
                        GROUP BY time({group_by}) fill(null)'
            else:  # sino aplico esta otra query
                # aqui la query es igual a la anterior pero si no se especifica *
                # la sintaxis cambia ya que hay que poner dobles comillas en measure
                query_string = f'SELECT mean("{measure}") FROM "{table}" \
                    WHERE time >= {timestamp}ms and time <= now() \
                        GROUP BY time({group_by}) fill(null)'
        elif isinstance(query, str):
            # en el caso que se quiera pasar una query personalizada 100%...
            query_string = query
        else:
            query_string = f'SELECT mean(*) FROM "{table}" \
                GROUP BY time({group_by}) fill(null)'

        # obtengo el dataframe resultante
        df_query = self.client.query(query_string)[table]

        # modifico el formato del indice por si es de interes
        if isinstance(format_index, str):
            df_query.index = df_query.index.map(
                lambda x: parse(str(x)).strftime(format_index)
            )
        return df_query

    def get_table(
        self,
        query: str,
        table: Optional[str] = None,
        return_dataframe: bool = False,
        format_index: Optional[str] = None,
    ) -> Union[pd.DataFrame, dict]:
        """Ejecuta una query y devuelve un objeto con los datos

        :param query: Consulta a realizar (puede provenir de set_query())
        :type query: str
        :param table: Nombre de la tabla en la que se quiere registrar
        :type table: str
        :param return_dataframe: True si quiero que me devuelva un DataFrame, por defecto False
        :type return_dataframe: bool, opcional
        :param format_index: Formato en el que quiero que se presente el indice del dataframe, por defecto None
        :type format_index: Optional[str], opcional
        :return: Datos de la query
        :rtype: Union[pd.DataFrame, dict]
        """

        # obtengo el dict de la query
        df_query = self.client.query(query)
        # lo paso a dataframe si lo pido
        if not isinstance(table, type(None)) and return_dataframe:
            df_query = df_query[table]

        # modifico el formato del indice por si es de interes
        if isinstance(format_index, str):
            df_query.index = df_query.index.map(
                lambda x: parse(str(x)).strftime(format_index)
            )
        return df_query


if __name__ == "__main__":
    # SCRIPT EJEMPLO

    # conecto con el cliente
    raspberry_shelly = ToolInflux(ip_address="10.141.188.140", database="shelly_test")

    # conecto con el servidor local
    local_shelly = ToolInflux(database="shelly_test")

    # obtengo los clientes de cada uno por si a caso
    client_raspberry_shelly = raspberry_shelly.get_client()
    client_local_shelly = local_shelly.get_client()

    # miro cual es el ultimo registro del local
    # si la tabla no existe no devuelve nada
    gli = local_shelly.get_last_index(table="data_shelly")

    # obtengo los datos y los vuelco en un dataframe
    df = raspberry_shelly.get_table_between_dates(table="data_shelly", start_date=gli)

    # escribo los datos en la bbdd local
    local_shelly.write_dataframe(df, table="data_shelly")
