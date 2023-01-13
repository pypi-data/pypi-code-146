import os
from pathlib import Path

import matplotlib
import pandas as pd

from .define import DEFAULT_FEEDBACK_FILEPATH, DEFAULT_PREFIX, GRADING_ITEMS

matplotlib.rcParams["font.sans-serif"] = "Noto Sans CJK SC"
matplotlib.rc(group="axes", unicode_minus=False)
matplotlib.use(backend="agg")

import matplotlib.pyplot as plt


def read_feedback(filepath: str | Path = DEFAULT_FEEDBACK_FILEPATH) -> pd.DataFrame:
    df = pd.read_excel(filepath)
    df = df[
        [
            "提交答卷时间",
            "您的姓名",
            "志愿者",
            "答疑科目",
            "服务时长/分钟",
            "评分—业务能力",
            "启发程度",
            "服务态度",
            "满意程度",
            "想说的话",
        ]
    ]
    df.rename(columns={"评分—业务能力": "业务能力"}, inplace=True)
    for item in GRADING_ITEMS:
        df[item] = pd.to_numeric(df[item], errors="coerce")
    df["想说的话"].replace(to_replace="(空)", value="", inplace=True)
    return df


def plot_time(
    df: pd.DataFrame, prefix: str | Path = DEFAULT_PREFIX, top_k: int = 9
) -> None:
    prefix = Path(prefix)
    subjects = df[["答疑科目", "服务时长/分钟"]].groupby(by="答疑科目").sum()
    subjects.sort_values(by="服务时长/分钟", ascending=False, inplace=True)
    data: pd.Series = subjects["服务时长/分钟"].head(n=top_k)
    if top_k < len(subjects):
        data["其他"] = subjects["服务时长/分钟"][top_k:].sum()

    plt.figure(dpi=300)
    plt.pie(data, labels=data.keys(), autopct="%.1f%%")
    plt.tight_layout()
    plt.savefig(prefix / "pie.png")
    plt.close()

    plt.figure(dpi=300)
    plt.barh(y=data.index, width=data / 60)
    plt.xlabel("服务时长/小时")
    plt.tight_layout()
    plt.savefig(prefix / "bar.png")
    plt.close()


def process_feedback(
    name: str,
    df: pd.DataFrame,
    readme: str,
    prefix: str | Path = DEFAULT_PREFIX,
) -> None:
    prefix = Path(prefix)
    os.makedirs(name=prefix, exist_ok=True)

    readme = readme.replace("[name]", name)

    count: int = len(df)
    readme = readme.replace("[count]", str(count))
    time: float = df["服务时长/分钟"].sum(skipna=True)
    readme = readme.replace("[hours]", str(round(number=time / 60, ndigits=2)))

    grading: list[str] = list()
    for item in GRADING_ITEMS:
        score: float = df[item].mean(skipna=True)
        grading.append(f"- {item}: {round(score, ndigits=2)} / 5.0")
    readme = readme.replace("[score]", "\n".join(grading))

    plot_time(df=df, prefix=prefix)

    readme_filepath: Path = prefix / "README.md"
    readme_filepath.write_text(data=readme)
