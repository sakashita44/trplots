import matplotlib.pyplot as plt


def configure_ax(
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
    """axに対して設定を行う関数

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
        label_font_size: int
            ラベルのフォントサイズ
        tick_font_size: int
            目盛りのフォントサイズ
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
        legend_correspondence_dict: dict
            凡例のラベルを変更するための辞書
        legend_kwargs: dict
            ax.legendに渡す引数
        **kwargs:
            ax.setに渡す引数

    Returns:
        ax: matplotlib.pyplot.Axes
    """

    for key, value in kwargs.items():
        ax.set(**{key: value})

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

    # 凡例の設定
    set_legend(ax, legend_correspondence_dict, **legend_kwargs)

    return ax


def set_legend(ax, legend_correspondence_dict, **kwargs):
    """axに対して凡例を設定する関数
    legend_correspondence_dictを用いて凡例のラベルを変更する
    また, 凡例で同じ文字列が複数表示されないようにする

    Args:
        ax: matplotlib.pyplot.Axes
        legend_correspondence_dict: dict
            凡例のラベルを変更するための辞書

    Returns:
        ax: matplotlib.pyplot.Axes
    """

    # 現在のlegendを取得し, 対応する新しいlegendを作成
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
    # 凡例に同じ文字列が複数表示されるのを防ぐ
    # reversedを使って逆順にすることで, dict化した際に最初に出現したものが優先され, あとから出現する同じラベルが削除される
    by_label = dict(zip(reversed(new_labels), reversed(handles)))
    # reversedしなおすことで, 元の順番に戻す
    hd = reversed(by_label.values())
    lb = reversed(by_label.keys())
    ax.legend(hd, lb, **kwargs)

    return ax
