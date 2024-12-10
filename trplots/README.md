# trplotsの各モジュールについて

各モジュールで特に重要なクラスや関数についての説明 # TODO

## plot_defaults.py

* `FLIERPROPS_DEFAULTS`: boxplotの外れ値のマーカーの設定に使用するデフォルト引数
* `SWARMPLOT_DEFAULTS`: jitter追加時に使用するswarmplotのデフォルト引数
* `PLOT_DEFAULTS`: 平均値追加時に使用するplotのデフォルト引数

## plot_utils.py

* `box_mean_plot`: seaborn.boxplotに処理を追加した関数. 箱ひげ図を作成し, 各箱ひげ図に平均値をプロットする. さらに, jitterを追加することも可能.
    * `data`: pandas.DataFrame - x, y, hueで指定された列を持つデータフレーム
    * `x`: str - x軸の列名
    * `y`: str - y軸の列名
    * `hue`: str - hueの列名 (省略可能)
    * `is_add_jitter`: bool - jitterを追加するかどうか (デフォルト: False)
    * `jitter_setting`: dict - seaborn.swarmplotに渡す引数(seaborn.swarmplotに**kwargsとして渡される, 省略可能)
    * `mean_setting`: dict - 平均値をプロットする際の設定(matplotlib.plotに**kwargsとして渡される, 省略可能)
    * `**kwargs`: dict - seaborn.boxplotに渡す引数: 箱ひげ図の見た目等を設定する
* `get_boxwidth`: 各箱ひげ図のx座標の位置を取得する関数. 外部から呼び出した際の動作は未確認.
* `get_boxcenter_x`: 箱ひげ図の中心のx座標を取得する関数. 外部から呼び出した際の動作は未確認.
* `add_brackets_for_boxplot`: 箱ひげ図が追加された状態のaxに有意差を表示する関数. box_mean_plotで作成したax以外に使用した場合の動作は未確認.
    * `ax`: matplotlib.pyplot.Axes - box_mean_plotで作成した箱ひげ図
    * `brackets`: list of tuple([int, int], [int, int], str) - 有意差を表示するブラケットのリスト
    * `bracket_base_y`: float - 有意差を表示するy軸の基準位置
    * `h_ratio`: float - 有意差を表示するブラケットの高さの比率 (ブラケットの高さをグラフの縦幅に対する比率で指定)
    * `hspace_ratio`: float - 有意差を表示するブラケットの高さ間隔の比率 (ブラケットの高さ間隔をグラフの縦幅に対する比率で指定)
    * `fs`: int - 有意差マークのフォントサイズ
* `plot_bracket`: 指定した座標にブラケットを追加する関数
    * `ax`: matplotlib.pyplot.Axes - ブラケットを追加するax
    * `x1`: float - ブラケットの始点のx座標
    * `x2`: float - ブラケットの終点のx座標
    * `y_bottom`: float - ブラケットの下端のy座標
    * `y_top`: float - ブラケットの上端のy座標
* `line_mean_sd_plot`: seaborn.lineplotに処理を追加した関数. 列名毎に平均と標準偏差を線グラフにプロットする.
    * `data`: pandas.DataFrame - index: x軸の値, 各列: データ (列名が同じ列をまとめて平均と標準偏差をプロットする)
    * `order`: list - 凡例の順番を指定 (省略可能)
    * `marks`: list - 凡例のマーカーを指定 (省略可能)
    * `**kwargs`: dict - seaborn.lineplotに渡す引数
* `line_group_coloring_plot`: seaborn.lineplotに処理を追加した関数. 列名毎に色分けして個別に線グラフをプロットする.
    * `data`: pandas.DataFrame - index: x軸の値, 各列: データ (列名が同じ列をまとめて色分けしてプロットする)
    * `order`: list - 凡例の順番を指定 (省略可能)
    * `marks`: list - 凡例のマーカーを指定 (省略可能)
    * `color_palette`: list - 色のリスト (省略可能)
    * `**kwargs`: dict - seaborn.lineplotに渡す引数

## plot_describe.py

* `single_describe`: box_mean_plotで使用したのと同じデータを与えるとその概要を返す関数.
    * `data`: pandas.DataFrame - x, y, hueで指定された列を持つデータフレーム
    * `x`: str - x軸の列名
    * `y`: str - y軸の列名
    * `hue`: str - hueの列名 (省略可能)
* `series_describe`: line_**_plotで使用したのと同じデータを与えるとその概要を返す関数.
    * `data`: pandas.DataFrame - index: x軸の値, 各列: データ

## plot_config.py

* `configure_ax`: axに対して設定を行う関数. ラベル, 凡例, 軸の設定を追加する.
    * `ax`: matplotlib.pyplot.Axes
    * `xlabel`: str - x軸のラベル名
    * `ylabel`: str - y軸のラベル名
    * `xlim`: double - x軸の範囲 (省略可能)
    * `ylim`: double - y軸の範囲 (省略可能)
    * `label_font_size`: int - ラベルのフォントサイズ (省略可能)
    * `tick_font_size`: int - 目盛りのフォントサイズ (省略可能)
    * `graph_limit_left`: float - グラフの左端の位置 (省略可能)
    * `graph_limit_right`: float - グラフの右端の位置 (省略可能)
    * `graph_limit_bottom`: float - グラフの下端の位置 (省略可能)
    * `graph_limit_top`: float - グラフの上端の位置 (省略可能)
    * `xlabel_loc_x`: float - x軸ラベルの位置(x位置) (省略可能)
    * `xlabel_loc_y`: float - x軸ラベルの位置(y位置) (省略可能)
    * `ylabel_loc_x`: float - y軸ラベルの位置(x位置) (省略可能)
    * `ylabel_loc_y`: float - y軸ラベルの位置(y位置) (省略可能)
    * `legend_correspondence_dict`: dict - 凡例のラベルを変更するための辞書 (set_legendで使用, 省略可能)
    * `legend_kwargs`: dict - ax.legendに渡す引数 (set_legendで使用, 省略可能)
* `set_legend`: axに対して凡例を設定する関数. legend_correspondence_dictを用いて凡例のラベルを変更する. また, 凡例で同じ文字列が複数表示されないようにする.
    * `ax`: matplotlib.pyplot.Axes
    * `legend_correspondence_dict`: dict - 凡例のラベルを変更するための辞書. key: 元のラベル, value: 新しいラベル (省略可能)
    * `**kwargs`: dict - ax.legendに渡す引数

## trend_plots.py

* `TrendPlots`: グラフを作成するためのクラス. 箱ひげ図や線グラフを追加するメソッドを持つ.
    * plot_utils.py, plot_config.pyの関数を使用しているため, それらの関数の引数をそのままメソッドに渡すことができる.
    * 共存不可能なグラフを同じaxに同時に追加することを防ぐことを目的としている.
    * ルートディレクトリのREADME.mdを参照
