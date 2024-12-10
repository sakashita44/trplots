import pandas as pd


def single_describe(data: pd.DataFrame, x, y, hue=None):
    """box_mean_plotで使用したのと同じデータを与えるとその概要を返す関数

    Args:
        data: pandas.DataFrame
            * x, y, hueで指定された列を持つデータフレーム(ワイド形式)
                * hueは省略可能
        x: str
            x軸の列名 (dataの列名)
            大分類
        y: str
            y軸の列名 (dataの列名)
            データ
        hue: str
            hueの列名 (dataの列名) (省略可能)
            大分類の中での分類

    Returns:
        describe: pandas.DataFrame
    """

    # データの概要を返す
    if hue is None:
        describe = data.groupby(x)[y].describe()
    else:
        describe = data.groupby([x, hue])[y].describe()

    return describe


def series_describe(data: pd.DataFrame):
    """line_**_plotで使用したのと同じデータを与えるとその概要を返す関数

    Args:
        df: pandas.DataFrame
            * index: x軸の値
            * 各列: データ
    Returns:
        describe: pandas.DataFrame
    """

    unique_cols = data.columns.unique()

    data_ms = []
    cond_cnt = {}
    for i, col in enumerate(unique_cols):
        # colを含む列のみを抽出
        data_tmp = data[col]
        # col列の平均値と標準偏差を新しいdfとして作成
        data_mean_sd = pd.DataFrame(index=data.index)
        # df_tmpの平均値と標準偏差を計算
        if data_tmp.ndim == 1:
            data_mean_sd[col + "_mean"] = data_tmp
            data_mean_sd[col + "_std"] = 0
        else:
            data_mean_sd[col + "_mean"] = data_tmp.mean(axis=1)  # type: ignore
            data_mean_sd[col + "_std"] = data_tmp.std(axis=1)  # type: ignore

        data_ms.append(data_mean_sd)
        if len(data_tmp.shape) == 1:
            cond_cnt[col] = 1
        else:
            cond_cnt[col] = data_tmp.shape[1]

    # データの概要を返す
    describe = pd.concat(data_ms, axis=1)
    describe = describe.describe()
    for cond, cnt in cond_cnt.items():
        # describeに新しくcond列を追加し, count行にcntを追加
        describe.loc["count", cond + "_trial"] = cnt

    return describe
