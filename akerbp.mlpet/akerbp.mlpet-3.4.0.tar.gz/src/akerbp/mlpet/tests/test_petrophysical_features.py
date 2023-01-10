import numpy as np
import pandas as pd

from akerbp.mlpet import feature_engineering, petrophysical_features
from akerbp.mlpet.dataloader import DataLoader
from akerbp.mlpet.tests.client import CLIENT, CLIENT_FUNCTIONS

WELL = "15/3-5"
ID_COLUMN = "well_name"
VSH_KWARGS = {
    "nan_numerical_value": -9999,
    "nan_textual_value": "MISSING",
    "VSH_curves": ["GR"],
}


def test_guess_bs_from_cali():
    input = pd.DataFrame({"CALI": [6.1, 5.9, 12.0, 12.02]})
    df = petrophysical_features.guess_BS_from_CALI(input)
    assert "BS" in df.columns.tolist()


def test_calculate_cali_bs():
    input = pd.DataFrame({"CALI": np.array([6.1, 5.9, 12.0, 12.02])})
    df = petrophysical_features.calculate_CALI_BS(input)
    assert "CALI-BS" in df.columns.tolist()


def test_calculate_VSH():
    dl = DataLoader()
    df = dl.load_from_cdf(
        client=CLIENT, metadata={"wellbore_name": WELL, "subtype": "BEST"}
    )
    df[ID_COLUMN] = WELL
    df = petrophysical_features.calculate_LFI(df)
    # BS is required but missing in this sequence to init to all nans
    df["BS"] = np.nan
    df = feature_engineering.add_formations_and_groups(
        df, id_column=ID_COLUMN, depth_column="DEPTH"
    )
    df = feature_engineering.add_vertical_depths(
        df, id_column=ID_COLUMN, md_column="DEPTH"
    )

    df_out = petrophysical_features.calculate_VSH(
        df,
        id_column=ID_COLUMN,
        env="prod",
        return_CI=True,
        client=CLIENT_FUNCTIONS,
        keyword_arguments=dict(
            calculate_denneu=True,
            VSH_curves=["GR", "LFI"],
            groups_column_name="GROUP",
            formations_column_name="FORMATION",
            return_only_vsh_aut=False,
            nan_numerical_value=-9999,
            nan_textual_value="MISSING",
        ),
    )
    assert "VSH" in df_out.columns.tolist()
