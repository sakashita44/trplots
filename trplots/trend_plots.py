import seaborn as sns
from .plot_utils import (
    box_mean_plot,
    add_brackets_for_boxplot,
    line_mean_sd_plot,
    line_group_coloring_plot,
)
from .plot_config import configure_ax


class TrendPlots:
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
            ax=self._ax,
            data=data,
            x=x,
            y=y,
            hue=hue,
            is_add_jitter=is_add_jitter,
            jitter_setting=jitter_setting,
            mean_setting=mean_setting,
            **kwargs,
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
        # box_mean_plot, line_group_coloring_plotとの併用を禁止
        if (
            "box_mean_plot" in self._graphs_in_ax
            or "line_group_coloring_plot" in self._graphs_in_ax
        ):
            raise ValueError(
                "box_mean_plot and line_group_coloring_plot cannot be used together"
            )
        self._ax = line_mean_sd_plot(data, order, marks, ax=self._ax, **kwargs)
        self._graphs_in_ax.append("line_mean_sd_plot")
        return self._ax

    def add_line_group_coloring_plot(
        self, data, order=[], marks=[], color_palette=sns.color_palette(), **kwargs
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
        # box_mean_plot, line_mean_sd_plotとの併用を禁止
        if (
            "box_mean_plot" in self._graphs_in_ax
            or "line_mean_sd_plot" in self._graphs_in_ax
        ):
            raise ValueError(
                "box_mean_plot and line_mean_sd_plot cannot be used together"
            )
        self._ax = line_group_coloring_plot(
            data, order, marks, color_palette, ax=self._ax, **kwargs
        )
        self._graphs_in_ax.append("line_group_coloring_plot")

    def configure_ax(
        self,
        ax,
        xlabel,
        ylabel,
        xlim=None,
        ylim=None,
        label_font_size=None,
        tick_font_size=None,
        graph_limit_left=None,
        graph_limit_right=None,
        graph_limit_bottom=None,
        graph_limit_top=None,
        xlabel_loc_x=None,
        xlabel_loc_y=None,
        ylabel_loc_x=None,
        ylabel_loc_y=None,
        legend_correspondence_dict={},
        legend_kwargs={},
        **kwargs,
    ):
        """axにラベル, 凡例, 軸の設定を追加する関数

        Args:
            ax: matplotlib.pyplot.Axes
            xlabel: str
                x軸のラベル
            ylabel: str
                y軸のラベル
            xlim: list
                x軸の表示範囲
            ylim: list
                y軸の表示範囲
            label_font_size: int
                ラベルのフォントサイズ
            tick_font_size: int
                軸の目盛りのフォントサイズ
            graph_limit_left: float
                グラフの左端の位置
            graph_limit_right: float
                グラフの右端の位置
            graph_limit_bottom: float
                グラフの下端の位置
            graph_limit_top: float
                グラフの上端の位置
            xlabel_loc_x: float
                x軸ラベルの位置(x座標)
            xlabel_loc_y: float
                x軸ラベルの位置(y座標)
            ylabel_loc_x: float
                y軸ラベルの位置(x座標)
            ylabel_loc_y: float
                y軸ラベルの位置(y座標)
            legend_correspondence_dict: dict
                凡例のラベルを置換するための辞書
            legend_kwargs: dict
                凡例の設定
            **kwargs:
                ax.set()に渡す引数
        """
        self._ax = configure_ax(
            ax,
            xlabel,
            ylabel,
            xlim,
            ylim,
            label_font_size,
            tick_font_size,
            graph_limit_left,
            graph_limit_right,
            graph_limit_bottom,
            graph_limit_top,
            xlabel_loc_x,
            xlabel_loc_y,
            ylabel_loc_x,
            ylabel_loc_y,
            legend_correspondence_dict,
            legend_kwargs,
            **kwargs,
        )

    @property
    def graphs_in_ax(self):
        return self._graphs_in_ax

    @property
    def ax(self):
        return self._ax
