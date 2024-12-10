import seaborn as sns
import pandas as pd
from matplotlib import patches
from .plot_defaults import SWARMPLOT_DEFAULTS, PLOT_DEFAULTS


def box_mean_plot(
    data: pd.DataFrame,
    x,
    y,
    hue=None,
    is_add_jitter=False,
    jitter_setting={},
    mean_setting={},
    **kwargs,
):
    """seaborn.boxplotに処理を追加した関数
    箱ひげ図を作成し, 各箱ひげ図に平均値をプロットする
    さらに, jitterを追加することも可能

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
        is_add_jitter: bool
            * jitterを追加するかどうか
        jitter_setting: dict
            * seaborn.swarmplotに渡す引数
            * 省略可能
        mean_setting: dict
            * ax.plotに渡す引数
            * 省略可能
        **kwargs:
            seaborn.boxplotに渡す引数

    Returns:
        ax: matplotlib.pyplot.Axes (作成したグラフが入ったax)
    """

    # dataとして入力されたdfのx列とhue列の型をstrに変換
    data[x] = data[x].astype(str)
    if hue is not None:
        data[hue] = data[hue].astype(str)

    # 箱ひげ図を作成
    ax = sns.boxplot(x=x, y=y, hue=hue, data=data, **kwargs)

    # jitterを追加
    if is_add_jitter:
        # **kwargs内にhue_orderがある場合かつjitter_setting内にhue_orderがない場合はhue_orderをjitter_settingに追加
        if "hue_order" in kwargs and "hue_order" not in jitter_setting:
            jitter_setting["hue_order"] = kwargs["hue_order"]
        ax = add_jitter_plot(ax=ax, data=data, x=x, y=y, hue=hue, **jitter_setting)

    # 箱ひげ図に外れ値を除いた平均値をプロット
    ax = add_mean_plot(ax=ax, data=data, x=x, y=y, hue=hue, **mean_setting)

    # 空の凡例を削除
    if hue is None:
        if ax.get_legend() is not None:
            ax.get_legend().remove()

    return ax


def add_jitter_plot(ax, data, x, y, hue=None, **kwargs):
    """box_mean_plotで作成した箱ひげ図にjitterをプロットする関数

    Args:
        ax: matplotlib.pyplot.Axes
            box_mean_plotで作成した箱ひげ図
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
        **kwargs:
            seaborn.swarmplotに渡す引数

    Returns:
        ax: matplotlib.pyplot.Axes
    """

    # 現在のlegendを保存
    handles, labels = ax.get_legend_handles_labels()

    # swarmplotのデフォルト引数
    swarmplot_args = SWARMPLOT_DEFAULTS.copy()

    # kwargsがある場合はswarmplot_argsに追加
    swarmplot_args.update(kwargs)

    ax = sns.swarmplot(
        ax=ax,
        x=x,
        y=y,
        hue=hue,
        data=data,
        dodge=True,
        **swarmplot_args,
    )
    # swarmplotで追加したlegendのみを削除
    # 別の場所で改めてax.legendを実行した場合, 削除したlegendが復活するので注意
    if hue is not None:
        ax.get_legend().remove()
    ax.legend(handles, labels)

    return ax


def add_mean_plot(ax, data, x, y, hue=None, **kwargs):
    """box_mean_plotで作成した箱ひげ図に, 外れ値を除いた平均値をプロットする関数

    Args:
        ax: matplotlib.pyplot.Axes
            box_mean_plotで作成した箱ひげ図
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
        **kwargs:
            ax.plotに渡す引数

    Returns:
        ax: matplotlib.pyplot.Axes
    """

    # plotのデフォルト引数
    plot_args = PLOT_DEFAULTS.copy()

    # kwargsがある場合はplot_argsに追加
    plot_args.update(kwargs)

    # 箱ひげ図の幅を取得
    boxwidth = get_boxwidth(ax)

    # legendのラベルを取得
    if hue is None:
        leg_labels = [None]
    else:
        labels = ax.get_legend().get_texts()
        leg_labels = [lb.get_text() for lb in labels]

    # xticksのラベルを取得
    xticks_labels = ax.get_xticklabels()
    xticks_labels = [x.get_text() for x in xticks_labels]

    # 箱ひげ図に外れ値を除いた平均値をプロット
    for i, xt_label in enumerate(xticks_labels):
        for j, leg_label in enumerate(leg_labels):
            # データの四分位範囲を取得
            condition = data[x] == xt_label
            if hue is not None:
                condition = condition & (data[hue] == leg_label)
            q1 = data[condition][y].quantile(0.25)
            q3 = data[condition][y].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            # 四分位範囲内のデータのみを抽出
            on_bound_condition = (
                (data[x] == xt_label)
                & (data[y] >= lower_bound)
                & (data[y] <= upper_bound)
            )
            if hue is not None:
                on_bound_condition = on_bound_condition & (data[hue] == leg_label)
            df_tmp = data[on_bound_condition]
            x_cood = get_boxcenter_x(boxwidth, i, j, len(leg_labels))

            # 平均値のプロット
            ax.plot(
                x_cood,
                [df_tmp[y].mean()],
                **plot_args,
            )

    return ax


def get_boxwidth(ax):
    # 各箱ひげ図のx座標の位置を取得 (ax.patches を使用)
    xlists = []
    for i, patch in enumerate(ax.patches):
        # パスの頂点（vertices）を取得してx座標を計算
        if isinstance(patch, patches.Rectangle):
            continue
        path = patch.get_path()
        vertices = path.vertices

        # verticesの各要素の1列目の最小値と最大値を取得
        x_min = vertices[:, 0].min()
        x_max = vertices[:, 0].max()

        xlists.append([x_min, x_max])

    # xlistsをx_minが小さい順にソート
    xlists = sorted(xlists, key=lambda x: x[0])
    xlists = [(x[1] - x[0]) for x in xlists]
    xwidth = sum(xlists) / len(xlists)
    return xwidth


def get_boxcenter_x(boxwidth, xtick_id, hue_id, hue_len):
    """箱ひげ図の中心のx座標を取得する関数

    Args:
        boxwidth: float
            箱ひげ図の幅(get_boxwidthで取得)
        xtick_id: int
            左から数えて何番目のx軸か(0始まり)
        hue_id: int
            同じxtick_idの中で左から数えて何番目のhueか(0始まり)
        hue_len: int
            同じxtick_idの中でのhueの数
    """

    x_center = xtick_id

    # 偶数の場合
    if hue_len % 2 == 0:
        # hue_idが半分より前の場合 (例えばhue_len=4の��合, 0, 1)
        if hue_id < hue_len // 2:
            k = -1
            # 例えばhue_len=4の場合, nは-2か-1になる
            n = abs(hue_id - hue_len // 2)
        # hue_idが半分より後の場合 (例えばhue_len=4の場合, 2, 3)
        else:
            k = 1
            # 例えばhue_len=4の場合, nは1か2になる
            n = hue_id - hue_len // 2 + 1
        # 中心から1つずれるときはboxwidth/2を加算, 2つずれるときは3*boxwidth/2を加算, 3つずれるときは5*boxwidth/2を加算...となるのでnがずれの数として
        x_cood = x_center + ((boxwidth * (n - 1)) + (boxwidth / 2)) * k

    # 奇数の場合
    else:
        # hue_idが真ん中の場合 (例えばhue_len=5の場合, 2)
        if hue_id == hue_len // 2:
            n = 0
            k = 0
        # hue_idが半分より前の場合 (例えばhue_len=5の場合, 0, 1)
        elif hue_id < hue_len // 2:
            k = -1
            n = abs(hue_id - hue_len // 2)
        # hue_idが半分より後の場合 (例えばhue_len=5の場合, 3, 4)
        else:
            k = 1
            n = hue_id - hue_len // 2
        x_cood = x_center + (boxwidth * n) * k

    return x_cood


def add_brackets_for_boxplot(
    ax, brackets, bracket_base_y=None, h_ratio=0.02, hspace_ratio=0.1, fs=10
):
    """
    箱ひげ図が追加された状態のaxに[([str, str], [str, str], str), ([str, str], [str, str], str), ...]で指定される有意差を表示する
    箱ひげ図の存在しないaxが与えられた場合の動作は保証しない

    Args:
        ax: matplotlib.pyplot.Axes
            * box_mean_plotで作成した箱ひげ図
        brackets: list of tuple([str, str], [str, str], str)
            * listの要素の数だけブラケットを表示
            * 1つのブラケットはtuple([str, str], [str, str], str)で指定
                * タプルの要素1: 1つめの箱ひげ図の位置を指定するための名前([str, str])
                    * 1つ目のstr: x軸のラベル名
                    * 2つ目のstr: hueのラベル名
                * タプルの要素2: 2つめの箱ひげ図の位置を指定するための名前([str, str])
                    * 1つ目のstr: x軸のラベル名
                    * 2つ目のstr: hueのラベル名
                * タプルの要素3: p値を示す文字列(str)
            * hueが存在しない場合はhueのラベル名は空白
        bracket_base_y: float
            有意差を表示するy軸の基準位置
        h_ratio: float
            有意差を表示するブラケットの高さの(グラフエリア高さに対する)比率
        hspace_ratio: float
            有意差を表示するブラケットの高さ間隔の(グラフエリア高さに対する)比率
        fs: int
            有意差マークのフォントサイズ

    Returns:
        ax: matplotlib.pyplot.Axes
    """
    if not brackets:
        return ax

    # x軸のラベルを取得
    xtick_labels = [x.get_text() for x in ax.get_xticklabels()]

    # 凡例のラベルを取得
    legend_labels = (
        [lb.get_text() for lb in ax.get_legend().get_texts()]
        if ax.get_legend()
        else [None]
    )

    # 箱ひげ図の幅を取得
    box_width = get_boxwidth(ax)

    # 各ブラケットの形式をチェック
    for b in brackets:
        check_bracket(b, xtick_labels, legend_labels)

    # ブラケットの高さと間隔を計算
    bracket_height = h_ratio * get_graph_area(ax)[0]
    bracket_hspace = hspace_ratio * get_graph_area(ax)[0]
    ph = bracket_height

    # 基準となるy座標を設定
    if bracket_base_y is None:
        bracket_base_y = ax.get_ylim()[1]

    base_y = bracket_base_y

    # ブラケットの位置を計算
    brackets_pos_list = convert_brackets_to_positions(
        brackets, xtick_labels, legend_labels, base_y, bracket_height, box_width
    )
    brackets_pos_list = sorted(brackets_pos_list, key=lambda x: x["x2"] - x["x1"])

    # ブラケットの位置を調整
    brackets_confirmed = adjust_bracket_positions(
        brackets_pos_list, base_y, bracket_height, bracket_hspace
    )

    # ブラケットをプロット
    plot_brackets(ax, brackets_confirmed, ph, fs)

    return ax


def convert_brackets_to_positions(
    brackets, xtick_labels, legend_labels, y_base, bracket_height, box_width
):
    """
    ブラケットの位置情報を計算する関数

    Args:
        brackets: list of tuple([str, str], [str, str], str)
            * 1つのブラケットはtuple([str, str], [str, str], str)で指定
                * タプルの要素1: 1つめの箱ひげ図の位置を指定するための名前([str, str])
                    * 1つ目のstr: x軸のラベル名
                    * 2つ目のstr: hueのラベル名
                * タプルの要素2: 2つめの箱ひげ図の位置を指定するための名前([str, str])
                    * 1つ目のstr: x軸のラベル名
                    * 2つ目のstr: hueのラベル名
                * タプルの要素3: p値を示す文字列(str)
            * hueが存在しない場合はhueのラベル名は空白
        legend_labels: list
            * 凡例のラベル
        y_base: float
            * ブラケットの基準位置
        bracket_height: float
            * ブラケットの高さ
        box_width: float
            * 箱ひげ図の幅

    Returns:
        brackets_pos_list: list of dict
            * ブラケットの位置情報 (引数bracketsに対応)
            * dictのkey
                * x1: float
                    * ブラケットの左端のx座標
                * x2: float
                    * ブラケットの右端のx座標
                * mark: str
                    * ブラケットの中に表示する文字列
                * y_bottom: float
                    * ブラケットの下端のy座標
                * y_bar: float
                    * ブラケットの上端のy座標
    """
    brackets_pos_list = []
    for b in brackets:
        # ブラケットのx座標を計算

        x1 = get_boxcenter_x(
            box_width,
            xtick_labels.index(b[0][0]),
            legend_labels.index(b[0][1]),
            len(legend_labels),
        )
        x2 = get_boxcenter_x(
            box_width,
            xtick_labels.index(b[1][0]),
            legend_labels.index(b[1][1]),
            len(legend_labels),
        )
        if x2 < x1:
            x1, x2 = x1, x2
        # ブラケットの位置情報を追加
        brackets_pos_list.append(
            {
                "x1": x1,
                "x2": x2,
                "mark": b[2],
                "y_bottom": y_base,
                "y_bar": y_base + bracket_height,
            }
        )
    return brackets_pos_list


def adjust_bracket_positions(brackets_pos_list, base_y, bracket_height, bracket_hspace):
    """
    ブラケットの高さを調整して, ブラケット同士が重ならないように座標を調整する関数

    Args:
        brackets_pos_list: list of dict
            * ブラケットの位置情報
            * dictのkey
                * x1: float
                    * ブラケットの左端のx座標
                * x2: float
                    * ブラケットの右端のx座標
                * mark: str
                    * ブラケットの中に表示する文字列
                * y_bottom: float
                    * ブラケットの下端のy座標
                * y_bar: float
                    * ブラケットの上端のy座標
        base_y: float
            * ブラケットの基準位置
        bracket_height: float
            * ブラケットの高さ
        bracket_hspace: float
            * ブラケットの高さ間隔

    Returns:
        brackets_confirmed: list of dict
            * ブラケットの位置情報 (引数bracketsに対応)
            * dictのkey
                * x1: float
                    * ブラケットの左端のx座標
                * x2: float
                    * ブラケットの右端のx座標
                * mark: str
                    * ブラケットの中に表示する文字列
                * y_bottom: float
                    * ブラケットの下端のy座標
                * y_bar: float
    """
    brackets_confirmed = []
    for i, b in enumerate(brackets_pos_list):
        if i == 0:
            # 最初のブラケットの位置を設定
            b["y_bottom"] = base_y
            b["y_bar"] = base_y + bracket_height
        else:
            # 他のブラケットの位置を調整
            b["y_bottom"] = search_y_pos(
                brackets_confirmed, b, base_y, bracket_height, bracket_hspace
            )
            b["y_bar"] = b["y_bottom"] + bracket_height
        brackets_confirmed.append(b)
    return brackets_confirmed


def plot_brackets(ax, brackets, ph, fs):
    """
    複数のブラケットをプロットし, 各ブラケットにp値を表すマークをプロットする関数

    Args:
        ax: matplotlib.pyplot.Axes
            * ブラケットをプロットする対象のax
        brackets: list of dict
            * ブラケットの位置情報
            * dictのkey
                * x1: float
                    * ブラケットの左端のx座標
                * x2: float
                    * ブラケットの右端のx座標
                * mark: str
                    * ブラケットの中に表示する文字列
                * y_bottom: float
                    * ブラケットの下端のy座標
                * y_bar: float
                    * ブラケットの上端のy座標
        ph: float
            * マークをプロットするy座標 (ブラケットの上端からの相対位置)
        fs: int
            * 有意差マークのフォントサイズ
    """
    for b in brackets:
        # ブラケットをプロット
        plot_bracket(ax, b["x1"], b["x2"], b["y_bottom"], b["y_bar"])
        # p値を表す文字列をプロット
        ax.text(
            (b["x1"] + b["x2"]) / 2,
            ph + b["y_bar"],
            b["mark"],
            ha="center",
            va="center",
            fontsize=fs,
        )


def plot_bracket(ax, x1, x2, y_bottom, y_top):
    """
    ブラケットをプロットする関数

    Args:
        ax: matplotlib.pyplot.Axes
            * ブラケットをプロットする対象のax
        x1: float
            * ブラケットの左端のx座標
        x2: float
            * ブラケットの右端のx座標
        y_bottom: float
            * ブラケットの下端のy座標
        y_top: float
            * ブラケットの上端のy座標
    """
    # ブラケットをプロット
    ax.plot(
        [x1, x1, x2, x2],
        [y_bottom, y_top, y_top, y_bottom],
        lw=1,
        color="black",
    )


def search_y_pos(brackets_confirmed, b, base_y, bracket_height, bracket_hspace):
    """brackets_confirmedに追加されるbのy座標を再帰的に探索する関数
    bracketの占有範囲は[x1, y_bottom]から[x2, y_bar]で表現される四角形
    base_yの高さに配置できる場合はbase_yがy_bottomとなる
    base_yに配置すると重なる場合はy_bottomにbracket_hspaceを加算し,

    Args:
        brackets_confirmed: list
            * すでに設定されたブラケットのリスト
        b: dict
            * 追加するブラケット (x1, x2)が既知
        base_y: float
            * ブラケットの最小y座標
        bracket_height: float
            * ブラケットの高さ
        bracket_hspace: float
            * ブラケットの高さ間隔

    Returns:
        y_bottom: float
            * ブラケットの下端のy座標
    """

    # bとすでに設定されたブラケットが重なっているかを判定
    is_overlapped = False
    for b_confirmed in brackets_confirmed:
        # bとb_confirmedが重なっている場合
        if (
            b["x1"] <= b_confirmed["x2"]
            and b["x2"] >= b_confirmed["x1"]
            and b["y_bottom"] <= b_confirmed["y_bar"]
            and b["y_bar"] >= b_confirmed["y_bottom"]
        ):
            is_overlapped = True
            break

    # 重なっていない場合はbase_yを返す
    if not is_overlapped:
        return base_y

    # 重なっている場合は再帰的にy座標を探索
    else:
        # 重ならない高さを探索
        new_base_y = base_y + bracket_hspace
        for b_confirmed in brackets_confirmed:
            if (
                b["x1"] < b_confirmed["x2"]
                and b["x2"] > b_confirmed["x1"]
                and new_base_y < b_confirmed["y_bar"]
                and new_base_y + bracket_height > b_confirmed["y_bottom"]
            ):
                return search_y_pos(
                    brackets_confirmed,
                    b,
                    new_base_y,
                    bracket_height,
                    bracket_hspace,
                )
        return new_base_y


def get_graph_area(ax):
    """グラフエリアの高さを取得する関数

    Args:
        ax: matplotlib.pyplot.Axes
            グラフエリアの高さを取得する対象のax

    Returns:
        graph_area_height, graph_area_width: (float, float)
            グラフエリアの高さ, グラフエリアの幅 ()
    """
    # グラフエリアの高さを取得
    ylim = ax.get_ylim()
    graph_area_height = ylim[1] - ylim[0]

    # グラフエリアの幅を取得
    xlim = ax.get_xlim()
    graph_area_width = xlim[1] - xlim[0]

    return graph_area_height, graph_area_width


def check_bracket(bracket, xtick_labels, legend_labels):
    """
    bracketが正しい形式であるかをチェックする関数
    正しくない場合はValueErrorを出力

    Args:
        bracket: tuple
            * 有意差を示すブラケット
            * (group1, group2, pマーク)
                * group1, group2: 比較するグループの名前 (str)
                * p値: 有意差を示すpのマーク, str
        xtick_labels: list
            x軸のラベルのリスト
        legend_labels: list
            凡例のラベルのリスト
    """

    if len(bracket) != 3:
        raise ValueError(
            "brackets must be a list of tuple([str, str], [str, str], str)"
        )
    if len(bracket[0]) != 2 or len(bracket[1]) != 2:
        raise ValueError(
            "brackets must be a list of tuple([str, str], [str, str], str)"
        )
    if (
        not isinstance(bracket[0][0], str)
        or not isinstance(bracket[0][1], str)
        or not isinstance(bracket[1][0], str)
        or not isinstance(bracket[1][1], str)
    ):
        raise ValueError(
            "brackets must be a list of tuple([str, str], [str, str], str)"
        )
    if not isinstance(bracket[2], str):
        raise ValueError(
            "brackets must be a list of tuple([str, str], [str, str], str)"
        )
    if (
        bracket[0][0] not in xtick_labels
        or bracket[0][1] not in legend_labels
        or bracket[1][0] not in xtick_labels
        or bracket[1][1] not in legend_labels
    ):
        raise ValueError("the label of brackets is out of range")


def line_mean_sd_plot(data: pd.DataFrame, order=None, marks=[], **kwargs):
    """
    seaborn.lineplotに処理を追加した関数
    列名毎に平均と標準偏差を線グラフにプロットする

    Args:
        data: pandas.DataFrame
            * index: x軸の値
            * 各列: データ
                * 列名が同じ列をまとめて平均と標準偏差をプロットする
        order: list
            * 凡例の順番を指定
            * 省略可能
        marks: list
            * 凡例のマーカーを指定(系列数より多い必要がある)
            * 省略した場合はマーカーなし
        **kwargs:
            seaborn.lineplotに渡す引数
    """
    # 時系列グラフの元データを作成
    unique_cols = data.columns.unique()

    # markが指定されていない場合Noneを代入
    if len(marks) == 0:
        marks = [None] * len(unique_cols)

    # **kwargsにmarkeredgecolorが指定されていない場合はデフォルトの色を指定
    if "markeredgecolor" not in kwargs:
        markeredgecolor = sns.color_palette()
    else:
        markeredgecolor = kwargs["markeredgecolor"]
        del kwargs["markeredgecolor"]

    # もしorderが指定されているにも関わらず, y_col_nameとorder内容が一致しない場合はエラーを出力
    if order is not None and set(unique_cols) != set(order):
        raise ValueError(
            "order must be the same as the unique value of data column name"
        )

    # orderが指定されている場合はその順番でグラフを作成
    if order is not None:
        unique_cols = order

    # 同じ名前の列毎に平均値と標準偏差のdfを作成
    for i, col in enumerate(unique_cols):
        # col列のみを抽出
        data_tmp = data[col]
        # col列の平均値と標準偏差を新しいdfとして作成
        data_mean_sd = pd.DataFrame(index=data.index)

        # data_tmpの平均値と標準偏差を計算
        if data_tmp.ndim == 1:
            data_mean_sd[col + "_mean"] = data_tmp[0]
            data_mean_sd[col + "_std"] = 0
        else:
            data_mean_sd[col + "_mean"] = data_tmp.mean(axis=1)  # type: ignore
            data_mean_sd[col + "_std"] = data_tmp.std(axis=1)  # type: ignore

        # グラフを作成
        ax = sns.lineplot(
            x=data_mean_sd.index,
            y=col + "_mean",
            data=data_mean_sd,
            label=col,
            marker=marks[i],
            markeredgecolor=markeredgecolor[i],
            **kwargs,
        )
        # 平均値に標準偏差を網掛け
        ax.fill_between(
            data_mean_sd.index,
            data_mean_sd[col + "_mean"] - data_mean_sd[col + "_std"],
            data_mean_sd[col + "_mean"] + data_mean_sd[col + "_std"],
            alpha=0.2,
        )

    return ax


def line_group_coloring_plot(
    data: pd.DataFrame, order=[], marks=[], color_palette=sns.color_palette(), **kwargs
):
    """
    seaborn.lineplotに処理を追加した関数
    列名毎に色分けして個別に線グラフをプロットする

    Args:
        data: pandas.DataFrame
            * index: x軸の値
            * 各列: データ
                * 列名が同じ列をまとめて色分けしてプロットする
        order: list
            * 凡例の順番を指定
            * 省略可能
        marks: list
            * 凡例のマーカーを指定(系列数より多い必要がある)
            * 省略した場合はマーカーなし
        color_palette: list
            * 色のリスト
            * 省略した場合はseabornのデフォルトカラーパレット
        **kwargs:
            seaborn.lineplotに渡す引数

    Returns:
        ax: matplotlib.pyplot.Axes
    """
    # 時系列グラフの元データを作成
    unique_cols = data.columns.unique()

    # markが指定されていない場合Noneを代入
    if len(marks) == 0:
        marks = [None] * len(unique_cols)

    # **kwargsにmarkeredgecolorが指定されていない場合はデフォルトの色を指定
    if "markeredgecolor" not in kwargs:
        markeredgecolor = color_palette
    else:
        markeredgecolor = kwargs["markeredgecolor"]
        del kwargs["markeredgecolor"]

    # もしorderが指定されているにも関わらず, unique_colsとorder内容が一致しない場合はエラーを出力
    if order is not None and set(unique_cols) != set(order):
        raise ValueError(
            "order must be the same as the unique value of data column name"
        )

    # グラフを作成
    # colnameをあらかじめorderに追加しておくことで, colnameの順番を固定する
    colname = order

    # dataの列毎に時系列グラフを作成
    for i, col in enumerate(data.columns):
        # s.name毎に色を変えてlineplotを作成
        series = data.iloc[:, i]
        if series.name not in colname:
            colname.append(series.name)
        # 名前毎に色を変えてlineplotを作成
        ax = sns.lineplot(
            x=series.index,
            y=series.values,
            label=series.name,
            color=color_palette[colname.index(series.name)],
            marker=marks[colname.index(series.name)],
            markeredgecolor=markeredgecolor[colname.index(series.name)],
            **kwargs,
        )

    # 凡例に同じ文字列が複数表示されるのを防ぐ
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())

    return ax
