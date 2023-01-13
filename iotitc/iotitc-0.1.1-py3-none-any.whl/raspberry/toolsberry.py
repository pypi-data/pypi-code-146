"""
Modulo orientado a la creacion de funciones para ser ejecutadas en Raspberry
"""

from typing import Tuple, Optional, Union
from math import modf
from datetime import datetime
import pandas as pd
import psutil  # type: ignore


def difference_between_times(
    last_time: datetime, time_now: Optional[datetime] = None
) -> str:
    """Funcion que calcula el tiempo transcurrido entre
    un periodo de tiempo determinado

    :param time: segundos totales
    :type time: datetime
    :return: cadena de caracteres en horas, minutos y segundos
    :rtype: str

    >>> from iotitc.raspberry.toolsberry import difference_between_times
    >>> from  datetime import datetime
    >>> last_datetime = datetime(2023,1,10,8,20,50)
    >>> now = datetime(2023,1,10,8,23,40)
    >>> difference_between_times(last_datetime, now)
    '00:02:50'
    """
    if time_now is None:
        time_now = datetime.now()

    # calculo la diferencia entre dos horas
    dif = time_now - last_time
    # saco los segundos
    sec = dif.seconds

    # los segundos los paso a horas y calculo los minutos restantes
    mins, hours = modf(sec / 60 / 60)
    mins = mins * 60

    # con los minutos, saco los segundos restantes y asi ya tengo
    # horas, minutos y segundos
    sec, _ = modf(mins)  # type: ignore
    sec = sec * 60

    # quito los decimales
    hours = int(hours)
    mins = int(mins)
    sec = int(sec)

    # los paso a string y si son menores de 10
    # les añado un 0 por delante a modo de estetica
    if hours < 10:
        hours_str = f"0{hours}"
    if mins < 10:
        mins_str = f"0{mins}"
    if sec < 10:
        sec_str = f"0{sec}"

    return f"{hours_str}:{mins_str}:{sec_str}"


def status_raspberry() -> Tuple:
    """
    :return: cpu, ram, disk
    - cpu: representa el % de uso de CPU
    - ram: diccionario que contiene la memoria libre, total y porcentaje ocupada de RAM en MB.
      La estrcutura del diccionario correspondiente a la memoria RAM es la siguiente:
      {avaliable_ram, total_ram, percentage_busy_ram}
    - disk: diccionario que contiene la memoria libre, total y porcentaje ocupada
      en el disco duro en GB. La estrcutura del diccionario correspondiente a la memoria
      del disco duro es la siguiente:
      {avaliable_disk, total_disk, percentage_busy_disk}
    :rtype: float, dict, dict

    >>> from iotitc.raspberry.toolsberry import status_raspberry
    >>> cpu, ram, disk, temp = status_raspberry()
    >>> temp["temp_cpu"] > 0
    True
    """
    # Datetime
    now = datetime.now()

    # porcentaje de uso de cpu
    cpu_percentage = psutil.cpu_percent()

    memory = psutil.virtual_memory()
    # memoria ram disponible
    avaliable_ram = round(memory.available / 1024.0 / 1024.0, 1)
    # memoria ram total
    total_ram = round(memory.total / 1024.0 / 1024.0, 1)
    # memoria ram ocupada
    busy_ram = round(total_ram - avaliable_ram, 1)
    #  % ocupado
    mem_info = round((total_ram - avaliable_ram) / total_ram, 1) * 100

    local_disk = psutil.disk_usage("/")
    # espacio libre en el disco
    avaliable_disk = round(local_disk.free / 1024.0 / 1024.0 / 1024.0, 1)
    # espacio total del disco
    total_disk = round(local_disk.total / 1024.0 / 1024.0 / 1024.0, 1)
    # espacio ocupado
    busy_disk = round(total_disk - avaliable_disk, 1)
    # % ocupado
    disk_info = round((total_disk - avaliable_disk) / total_disk, 1) * 100

    try:
        temp_cpu = psutil.sensors_temperatures()['cpu_thermal'][0][1]
    except KeyError:
        temp_cpu = -1

    return  (
        {
            "time"                  : now,
            "percentage_cpu"        : cpu_percentage,
        },
        {
            "time"                  : now,
            "busy_ram"              : busy_ram,
            "total_ram"             : total_ram,
            "percentage_busy_ram"   : round(mem_info, 2),
        },
        {
            "time"                  : now,
            "busy_disk"             : busy_disk,
            "total_disk"            : total_disk,
            "percentage_bussy_disk" : round(disk_info, 2),
         },{
            "time"                  : now,
            "temp_cpu"              : temp_cpu,
        },
    )

if __name__ == "__main__":
    cpu, ram, disk, temp = status_raspberry()
    print(cpu)