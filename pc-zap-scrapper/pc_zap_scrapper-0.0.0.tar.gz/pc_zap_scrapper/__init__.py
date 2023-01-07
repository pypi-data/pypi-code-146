import os
import pc_zap_scrapper
from pathlib import Path
from pc_zap_scrapper._version import __version__

ACTION = "venda"

LOCALIZATION = "mg+pocos-de-caldas"

TYPE = "imoveis"

PATH_DATA_RAW = f"datasets/raw/data_raw_{LOCALIZATION}_{ACTION}_{TYPE}.parquet"

PATH_DATA_INTERIM = (
    f"datasets/interim/data_interim_{LOCALIZATION}_{ACTION}_{TYPE}.parquet"
)

PATH_NEIGHBORHOOD_COORDS = "datasets/external/neighbor_latlong.parquet"

PATH_TEMP = os.path.join(Path(pc_zap_scrapper.__file__).parents[1], "temp")

PATH_TEMP_DOTENV = os.path.join(PATH_TEMP, ".env")