import pandas as pd


def normalize_from_tokens(
    token_column: pd.Series,
    list_token: pd.Series,
    list_column: pd.Series,
    position: int = 0,
) -> pd.Series:
    """Find all tokens from token column in list_token,
    then use list_column to get the first appareance of given token.

    Args:s
        token_column (pd.Series): Tokens to find.
        list_token (pd.Series): Bag of tokens.
        list_column (pd.Series): Values to index from bag of tokens.

    Returns:
        pd.Series: New column.
    """

    def clean(sdx: str) -> str:
        return list_column[list_token == sdx].values[position]

    return token_column.map(clean)
