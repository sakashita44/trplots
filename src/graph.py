import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd


class graph:
    def __init__(self, ax):
        """
        Args:
            ax: matplotlib.pyplot.Axes
        """
        self._ax = ax
        self._graphs_in_ax = []

    def add_box_mean_plot(
        self,
        data,
        x,
        y,
        hue=None,
        flierprops={},
        jitter_setting={},
        mean_setting={},
        **kwargs,
    ):
        """seaborn.boxplotに処理を追加した関数
        箱ひげ図を作成し, 各箱ひげ図に平均値をプロットする

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
            flierprops: dict
                * seaborn.boxplotに渡す引数
                * 外れ値のマーカーの設定
            jitter_setting: dict
                * seaborn.swarmplotに渡す引数
                * 省略可能
            mean_setting: dict

            **kwargs:
                seaborn.boxplotに渡す引数

        Returns:
            ax: matplotlib.pyplot.Axes (作成したグラフが入ったax)
        """
        # line_mean_sd_plot, line_group_coloring_plotとの併用を禁止
        if (
            "line_mean_sd_plot" in self._graphs_in_ax
            or "line_group_coloring_plot" in self._graphs_in_ax
        ):
            raise ValueError(
                "line_mean_sd_plot and line_group_coloring_plot cannot be used together"
            )
        self._ax = box_mean_plot(
            data, x, y, hue, flierprops, jitter_setting, mean_setting, **kwargs
        )
        self._graphs_in_ax.append("box_mean_plot")
        return self._ax

    def add_brackets(
        self, brackets, bracket_base_y=None, h_ratio=0.02, hspace_ratio=0.1, fs=10
    ):
        """
        箱ひげ図が追加された状態のaxに[([int, int], [int, int], str), ([int, int], [int, int], str), ...]で指定される有意差を表示する
        箱ひげ図の存在しないaxが与えられた場合の動作は保証しない

        Args:
            brackets: list of tuple([int, int], [int, int], str)
                * listの要素の数だけブラケットを表示
                * 1つのブラケットはtuple([int, int], [int, int], str)で指定
                    * タプルの要素1: 1つめの箱ひげ図の位置を指定するためのインデックス([int, int])
                        * 1つ目のint: x軸のインデックス(int)
                        * 2つ目のint: hueのインデックス(int)
                    * タプルの要素2: 2つめの箱ひげ図の位置を指定するためのインデックス([int, int])
                        * 1つ目のint: x軸のインデックス(int)
                        * 2つ目のint: hueのインデックス(int)
                    * タプルの要素3: p値を示す文字列(str)
                * すべてのインデックスは1始まり
                * hueが存在しない場合はhueのインデックスは1を指定
            bracket_base_y: float
                有意差を表示するy軸の基準位置
            h_ratio: float
                有意差を表示するブラケットの高さの(グラフエリア高さに対する)比率
            hspace_ratio: float
                有意差を表示するブラケットの高さ間隔の(グラフエリア高さに対する)比率
            fs: int
                有意差マークのフォントサイズ
        """
        # box_mean_plotが存在しない場合はエラーを出力
        if not self._graphs_in_ax:
            raise ValueError("box_mean_plot must be executed before add_brackets")
        self._ax = add_brackets_for_boxplot(
            self._ax, brackets, bracket_base_y, h_ratio, hspace_ratio, fs
        )
        self._graphs_in_ax.append("add_brackets")
        return self._ax

    def add_line_mean_sd_plot(self, data, order=None, marks=[], **kwargs):
        # box_mean_plot, line_group_coloring_plotとの併用を禁止
        if (
            "box_mean_plot" in self._graphs_in_ax
            or "line_group_coloring_plot" in self._graphs_in_ax
        ):
            raise ValueError(
                "box_mean_plot and line_group_coloring_plot cannot be used together"
            )
        self._ax = line_mean_sd_plot(data, order, marks, **kwargs)
        self._graphs_in_ax.append("line_mean_sd_plot")
        return self._ax

    def add_line_group_coloring_plot(
        self, data, order=[], marks=[], color_palette=sns.color_palette(), **kwargs
    ):
        # box_mean_plot, line_mean_sd_plotとの併用を禁止
        if (
            "box_mean_plot" in self._graphs_in_ax
            or "line_mean_sd_plot" in self._graphs_in_ax
        ):
            raise ValueError(
                "box_mean_plot and line_mean_sd_plot cannot be used together"
            )
        self._ax = line_group_coloring_plot(data, order, marks, color_palette, **kwargs)
        self._graphs_in_ax.append("line_group_coloring_plot")

    def set_ax(
        self,
        ax,
        xlabel,
        ylabel,
        xlim=None,
        ylim=None,
        graph_type="box",
        legend_correspondence_dict={},
        label_font_size=None,
        tick_font_size=None,
        legend_font_size=None,
        graph_limit_left=None,
        graph_limit_right=None,
        graph_limit_bottom=None,
        graph_limit_top=None,
        xlabel_loc_x=None,
        xlabel_loc_y=None,
        ylabel_loc_x=None,
        ylabel_loc_y=None,
    ):
        """
        Args:
            ax: matplotlib.pyplot.Axes
            xlabel: str
            ylabel: str
            xlim: tuple
            ylim: tuple
            graph_type: str
            legend_correspondence_dict: dict
            label_font_size: int
            tick_font_size: int
            legend_font_size: int
            graph_limit_left: float
            graph_limit_right: float
            graph_limit_bottom: float
            graph_limit_top: float
            xlabel_loc_x: float
            xlabel_loc_y: float
            ylabel_loc_x: float
            ylabel_loc_y: float
        """
        self._ax = set_ax(
            ax,
            xlabel,
            ylabel,
            xlim,
            ylim,
            graph_type,
            legend_correspondence_dict,
            label_font_size,
            tick_font_size,
            legend_font_size,
            graph_limit_left,
            graph_limit_right,
            graph_limit_bottom,
            graph_limit_top,
            xlabel_loc_x,
            xlabel_loc_y,
            ylabel_loc_x,
            ylabel_loc_y,
        )
        return self._ax

    @property
    def graphs_in_ax(self):
        return self._graphs_in_ax

    @property
    def ax(self):
        return self._ax


def box_mean_plot(
    data: pd.DataFrame,
    x,
    y,
    hue=None,
    flierprops={"marker": "x", "markersize": 10},
    jitter_setting={},
    mean_setting={},
    **kwargs,
):
    """seaborn.boxplotに処理を追加した関数
    箱ひげ図を作成し, 各箱ひげ図に平均値をプロットする

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
        flierprops: dict
            * seaborn.boxplotに渡す引数
            * 外れ値のマーカーの設定
        jitter_setting: dict
            * seaborn.swarmplotに渡す引数
            * 省略可能
        mean_setting: dict

        **kwargs:
            seaborn.boxplotに渡す引数

    Returns:
        ax: matplotlib.pyplot.Axes (作成したグラフが入ったax)
    """

    # dfのxとhueのタイプをstrに変換
    data[x] = data[x].astype(str)
    if hue is not None:
        data[hue] = data[hue].astype(str)

    # sns.boxplotに渡す引数を抽出
    boxplot_args = {
        key: kwargs[key] for key in kwargs if key in sns.boxplot.__code__.co_varnames
    }

    # 箱ひげ図を作成
    ax = sns.boxplot(
        x=x,
        y=y,
        hue=hue,
        data=data,
        flierprops=flierprops,
        **boxplot_args,
    )

    # jitterを追加
    if any(jitter_setting):
        ax = add_jitter_plot(ax, data, x, y, hue, jitter_setting)

    # 箱ひげ図に外れ値を除いた平均値をプロット
    ax = add_mean_plot(ax, data, x, y, hue, mean_setting)

    # 空の凡例を削除
    if hue is None:
        if ax.get_legend() is not None:
            ax.get_legend().remove()

    return ax


def add_jitter_plot(ax, data, x, y, hue=None, jitter_setting={}):
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
        jitter_setting: dict
            * jitterをプロットする際の引数
            * 省略可能

    Returns:
        ax: matplotlib.pyplot.Axes
    """

    # 現在のlegendを保存
    handles, labels = ax.get_legend_handles_labels()

    # swarmplotの引数を設定
    swarmplot_args = {
        key: jitter_setting[key]
        for key in jitter_setting
        if key in sns.swarmplot.__code__.co_varnames
    }
    if "marker" not in jitter_setting:
        swarmplot_args["marker"] = "o"
    else:
        swarmplot_args["marker"] = jitter_setting["marker"]
    if "alpha" not in jitter_setting:
        swarmplot_args["alpha"] = 0.7
    else:
        swarmplot_args["alpha"] = jitter_setting["alpha"]

    ax = sns.swarmplot(
        x=x,
        y=y,
        hue=hue,
        data=data,
        dodge=True,
        **swarmplot_args,
    )
    # swarmplotで追加したlegendのみを削除
    if hue is not None:
        ax.get_legend().remove()
    ax.legend(handles, labels)

    return ax


def add_mean_plot(ax, data, x, y, hue=None, mean_setting={}):
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
        mean_setting: dict
            * 平均値をプロットする際の引数
            * 省略可能

    Returns:
        ax: matplotlib.pyplot.Axes
    """

    # plotの引数を設定
    mean_plot_args = {
        key: mean_setting[key]
        for key in mean_setting
        if key in ax.plot.__code__.co_varnames
    }
    if "color" not in mean_setting:
        mean_plot_args["color"] = "black"
    else:
        mean_plot_args["color"] = mean_setting["color"]
    if "marker" not in mean_setting:
        mean_plot_args["marker"] = "+"
    else:
        mean_plot_args["marker"] = mean_setting["marker"]
    if "markersize" not in mean_setting:
        mean_plot_args["markersize"] = 10
    else:
        mean_plot_args["markersize"] = mean_setting["markersize"]
    if "markeredgewidth" not in mean_setting:
        mean_plot_args["markeredgewidth"] = 1
    else:
        mean_plot_args["markeredgewidth"] = mean_setting["markeredgewidth"]

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
                **mean_plot_args,
            )

    return ax


def get_boxwidth(ax):
    # 各箱ひげ図のx座標の位置を取得 (ax.patches を使用)
    xlists = []
    for i, patch in enumerate(ax.patches):
        # パスの頂点（vertices）を取得してx座標を計算
        # PathPatch以外の場合はスキップ
        if type(patch) == matplotlib.patches.Rectangle:
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
        # hue_idが半分より前の場合 (例えばhue_len=4の場合，0, 1)
        if hue_id < hue_len // 2:
            k = -1
            # 例えばhue_len=4の場合，nは-2か-1になる
            n = abs(hue_id - hue_len // 2)
        # hue_idが半分より後の場合 (例えばhue_len=4の場合，2, 3)
        else:
            k = 1
            # 例えばhue_len=4の場合，nは1か2になる
            n = hue_id - hue_len // 2 + 1
        # 中心から1つずれるときはboxwidth/2を加算，2つずれるときは3*boxwidth/2を加算，3つずれるときは5*boxwidth/2を加算...となるのでnがずれの数として
        x_cood = x_center + ((boxwidth * (n - 1)) + (boxwidth / 2)) * k

    # 奇数の場合
    else:
        # hue_idが真ん中の場合 (例えばhue_len=5の場合，2)
        if hue_id == hue_len // 2:
            n = 0
            k = 0
        # hue_idが半分より前の場合 (例えばhue_len=5の場合，0, 1)
        elif hue_id < hue_len // 2:
            k = -1
            n = abs(hue_id - hue_len // 2)
        # hue_idが半分より後の場合 (例えばhue_len=5の場合，3, 4)
        else:
            k = 1
            n = hue_id - hue_len // 2
        x_cood = x_center + (boxwidth * n) * k

    return x_cood


def add_brackets_for_boxplot(
    ax, brackets, bracket_base_y=None, h_ratio=0.02, hspace_ratio=0.1, fs=10
):
    """
    箱ひげ図が追加された状態のaxに[([int, int], [int, int], str), ([int, int], [int, int], str), ...]で指定される有意差を表示する
    箱ひげ図の存在しないaxが与えられた場合の動作は保証しない

    Args:
        ax: matplotlib.pyplot.Axes
            * box_mean_plotで作成した箱ひげ図
        brackets: list of tuple([int, int], [int, int], str)
            * listの要素の数だけブラケットを表示
            * 1つのブラケットはtuple([int, int], [int, int], str)で指定
                * タプルの要素1: 1つめの箱ひげ図の位置を指定するためのインデックス([int, int])
                    * 1つ目のint: x軸のインデックス(int)
                    * 2つ目のint: hueのインデックス(int)
                * タプルの要素2: 2つめの箱ひげ図の位置を指定するためのインデックス([int, int])
                    * 1つ目のint: x軸のインデックス(int)
                    * 2つ目のint: hueのインデックス(int)
                * タプルの要素3: p値を示す文字列(str)
            * すべてのインデックスは1始まり
            * hueが存在しない場合はhueのインデックスは1を指定
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

    xtick_labels = [x.get_text() for x in ax.get_xticklabels()]
    xtick_len = len(xtick_labels)

    legend_labels = (
        [lb.get_text() for lb in ax.get_legend().get_texts()]
        if ax.get_legend()
        else [None]
    )
    legend_len = len(legend_labels)

    for b in brackets:
        check_bracket(b, xtick_len, legend_len)

    bracket_height = h_ratio * get_graph_area(ax)[0]
    bracket_hspace = hspace_ratio * get_graph_area(ax)[0]
    ph = bracket_height

    if bracket_base_y is None:
        bracket_base_y = ax.get_ylim()[1]

    base_y = bracket_base_y

    brackets_pos_list = convert_brackets_to_positions(
        ax, brackets, legend_labels, base_y, bracket_height
    )
    brackets_pos_list = sorted(brackets_pos_list, key=lambda x: x["x2"] - x["x1"])

    brackets_confirmed = adjust_bracket_positions(
        brackets_pos_list, base_y, bracket_height, bracket_hspace
    )

    plot_brackets(ax, brackets_confirmed, ph, fs)

    return ax


def convert_brackets_to_positions(ax, brackets, legend_labels, y_base, bracket_height):
    brackets_pos_list = []
    for b in brackets:
        x1 = get_boxcenter_x(
            get_boxwidth(ax), b[0][0] - 1, b[0][1] - 1, len(legend_labels)
        )
        x2 = get_boxcenter_x(
            get_boxwidth(ax), b[1][0] - 1, b[1][1] - 1, len(legend_labels)
        )
        if x2 < x1:
            x1, x2 = x2, x1
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
    brackets_confirmed = []
    for i, b in enumerate(brackets_pos_list):
        if i == 0:
            b["y_bottom"] = base_y
            b["y_bar"] = base_y + bracket_height
        else:
            b["y_bottom"] = search_y_pos(
                brackets_confirmed, b, base_y, bracket_height, bracket_hspace
            )
            b["y_bar"] = b["y_bottom"] + bracket_height
        brackets_confirmed.append(b)
    return brackets_confirmed


def plot_brackets(ax, brackets_confirmed, ph, fs):
    for b in brackets_confirmed:
        ax.plot(
            [b["x1"], b["x1"], b["x2"], b["x2"]],
            [b["y_bottom"], b["y_bar"], b["y_bar"], b["y_bottom"]],
            lw=1,
            color="black",
        )
        ax.text(
            (b["x1"] + b["x2"]) / 2,
            ph + b["y_bar"],
            b["mark"],
            ha="center",
            va="center",
            fontsize=fs,
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


def check_bracket(bracket, xtick_len, legend_len):
    """
    bracketが正しい形式であるかをチェックする関数
    正しくない場合はValueErrorを出力

    Args:
        bracket: tuple
            * 有意差を示すブラケット
            * (group1, group2, pマーク)
                * group1, group2: 比較するグループのインデックス (1始まり), int
                * p値: 有意差を示すpのマーク, str
        xtick_len: int
            x軸のラベルの数
        legend_len: int
            凡例のラベルの数
    """

    if len(bracket) != 3:
        raise ValueError(
            "brackets must be a list of tuple([int, int], [int, int], str)"
        )
    if len(bracket[0]) != 2 or len(bracket[1]) != 2:
        raise ValueError(
            "brackets must be a list of tuple([int, int], [int, int], str)"
        )
    if (
        not isinstance(bracket[0][0], int)
        or not isinstance(bracket[0][1], int)
        or not isinstance(bracket[1][0], int)
        or not isinstance(bracket[1][1], int)
    ):
        raise ValueError(
            "brackets must be a list of tuple([int, int], [int, int], str)"
        )
    if not isinstance(bracket[2], str):
        raise ValueError(
            "brackets must be a list of tuple([int, int], [int, int], str)"
        )
    if (
        bracket[0][0] > xtick_len
        or bracket[0][1] > legend_len
        or bracket[1][0] > xtick_len
        or bracket[1][1] > legend_len
    ):
        raise ValueError("the index of brackets is out of range")


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

    # もしorderが指定されているにも関わらず，y_col_nameとorder内容が一致しない場合はエラーを出力
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
            data_mean_sd[col + "_mean"] = data_tmp.mean(axis=1)
            data_mean_sd[col + "_std"] = data_tmp.std(axis=1)

        # グラフを作成
        ax = sns.lineplot(
            x=data_mean_sd.index,
            y=col + "_mean",
            data=data_mean_sd,
            label=col,
            marker=marks[i],
            markerfacecolor="none",
            markeredgecolor=sns.color_palette()[i],
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

    """
    # 時系列グラフの元データを作成
    unique_cols = data.columns.unique()

    # markが指定されていない場合Noneを代入
    if len(marks) == 0:
        marks = [None] * len(unique_cols)

    # もしorderが指定されているにも関わらず，unique_colsとorder内容が一致しない場合はエラーを出力
    if order is not None and set(unique_cols) != set(order):
        raise ValueError(
            "order must be the same as the unique value of data column name"
        )

    # グラフを作成
    # colnameをあらかじめorderに追加しておくことで，colnameの順番を固定する
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
            **kwargs,
        )

    # 凡例に同じ文字列が複数表示されるのを防ぐ
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())

    return ax


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
            data_mean_sd[col + "_mean"] = data_tmp.mean(axis=1)
            data_mean_sd[col + "_std"] = data_tmp.std(axis=1)

        data_ms.append(data_mean_sd)
        if len(data_tmp.shape) == 1:
            cond_cnt[col] = 1
        else:
            cond_cnt[col] = data_tmp.shape[1]

    # データの概要を返す
    describe = pd.concat(data_ms, axis=1)
    describe = describe.describe()
    for cond, cnt in cond_cnt.items():
        # describeに新しくcond列を追加し，count行にcntを追加
        describe.loc["count", cond + "_trial"] = cnt

    return describe


def set_ax(
    ax,
    xlabel,
    ylabel,
    xlim=None,
    ylim=None,
    graph_type="box",
    legend_correspondence_dict={},
    label_font_size=None,
    tick_font_size=None,
    legend_font_size=None,
    graph_limit_left=None,
    graph_limit_right=None,
    graph_limit_bottom=None,
    graph_limit_top=None,
    xlabel_loc_x=None,
    xlabel_loc_y=None,
    ylabel_loc_x=None,
    ylabel_loc_y=None,
):
    """axに対してconfig.ymlで指定したデフォルトのフォントサイズを設定する
    同時にx軸，y軸のラベル名を設定し，グラフの大きさを設定する

    Args:
        ax: matplotlib.pyplot.Axes
        xlabel: str
            x軸のラベル名
        ylabel: str
            y軸のラベル名
        xlim: double
            x軸の範囲
        ylim: double
            y軸の範囲
        graph_type: str
            グラフの種類
            "box": 箱ひげ図, "line": 折れ線グラフ
        legend_correspondence_dict: dict
            凡例のラベルを変更するための辞書
        label_font_size: int
            ラベルのフォントサイズ
        tick_font_size: int
            目盛りのフォントサイズ
        legend_font_size: int
            凡例のフォントサイズ
        graph_limit_left: float
            グラフの左端の位置
        graph_limit_right: float
            グラフの右端の位置
        graph_limit_bottom: float
            グラフの下端の位置
        graph_limit_top: float
            グラフの上端の位置
        xlabel_loc_x: float
            x軸ラベルの位置(x位置)
        xlabel_loc_y: float
            x軸ラベルの位置(y位置)
        ylabel_loc_x: float
            y軸ラベルの位置(x位置)
        ylabel_loc_y: float
            y軸ラベルの位置(y位置)

    Returns:
        ax: matplotlib.pyplot.Axes
    """
    # フォントサイズを設定
    if label_font_size is not None:
        ax.set_xlabel(xlabel, fontsize=label_font_size)
        ax.set_ylabel(ylabel, fontsize=label_font_size)
    if tick_font_size is not None:
        ax.tick_params(labelsize=tick_font_size)

    # グラフの大きさを設定(画像サイズを1とした場合の比率)
    if (
        graph_limit_left is not None
        and graph_limit_right is not None
        and graph_limit_bottom is not None
        and graph_limit_top is not None
    ):
        plt.gcf().subplots_adjust(
            left=graph_limit_left,
            right=graph_limit_right,
            bottom=graph_limit_bottom,
            top=graph_limit_top,
        )

    # ラベル位置の調整
    if xlabel_loc_x is not None and xlabel_loc_y is not None:
        ax.xaxis.set_label_coords(xlabel_loc_x, xlabel_loc_y)
    if ylabel_loc_x is not None and ylabel_loc_y is not None:
        ax.yaxis.set_label_coords(ylabel_loc_x, ylabel_loc_y)

    # グリッドを点線で表示
    ax.grid(linestyle=":")

    # x軸、y軸の範囲を設定
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)

    # 現在のlegendを取得し，対応する新しいlegendを作成
    handles, labels = ax.get_legend_handles_labels()
    new_labels = []
    # 新しいlegendを作成
    if legend_correspondence_dict != {}:
        for lb in labels:
            new_labels.append(legend_correspondence_dict[lb])
        if len(new_labels) == 0:
            new_labels = labels
        elif len(new_labels) != len(labels):
            new_labels = labels
            print(
                "WARN: The number of legend correspondence input is not equal to the number of legend labels."
            )
            print("WARN: The legend labels are not changed.")
    else:
        new_labels = labels

    # legendの順番を設定
    if legend_correspondence_dict != {}:
        legend_order = list(legend_correspondence_dict.values())
    else:
        legend_order = None

    # legendをorderに従って並び替え
    if legend_order is not None:
        for o in reversed(legend_order):
            # new_labelsのうちoの最初のインデックスを取得
            idx = new_labels.index(o)
            # new_labelsとhandlesのidx番目をtmpに保存
            lb_tmp = new_labels[idx]
            hd_tmp = handles[idx]
            # new_labelsとhandlesのidx番目を削除
            new_labels.pop(idx)
            handles.pop(idx)
            # new_labelsとhandlesの最初にtmpを追加
            new_labels.insert(0, lb_tmp)
            handles.insert(0, hd_tmp)

    # legendを設定
    # 時系列データの場合は同じ文字列が複数表示されるのを防ぐ処理を追加
    if graph_type == "line":
        # 凡例に同じ文字列が複数表示されるのを防ぐ
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(new_labels, handles))
        ax.legend(by_label.values(), by_label.keys(), fontsize=legend_font_size)
    elif graph_type == "box":
        ax.legend(handles, new_labels, fontsize=legend_font_size)

    return ax


if __name__ == "__main__":
    pass
