import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import yaml

def single_graph(df: pd.DataFrame, ax, **kwargs):
    """
    seaborn.boxplotに処理を追加した関数

    1. 引数
        1. pandas.DataFrame
            * 1列目: trial_id(試行番号)
            * 2列目: parameter※(パラメータ) ※ファイルにより異なる
            * 3列目: is_assist_continue(実験のアシスト条件(TRUE/FALSE) またはPGT(null))
        1. ax: matplotlib.pyplot.Axes
        1. plotのその他引数(x, y, axを除く)
    1. 返り値
        1. ax: matplotlib.pyplot.Axes
        1. describe: pandas.DataFrame
    1. 処理
        1. 3列目の値で分類して箱ひげ図をax内に作成
        1. この関数外部でx軸の範囲等を設定する
    """
    # 箱ひげ図を作成
    x_col_name, y_col_name = get_colname(df, False)
    ax = sns.boxplot(x=x_col_name, y=y_col_name, data=df, ax=ax, **kwargs)

    # 箱ひげ図に外れ値を除いた平均値をプロット
    for i, val in enumerate(df[x_col_name].unique()):
        # データの四分位範囲を取得
        q1 = df[df[x_col_name] == val][y_col_name].quantile(0.25)
        q3 = df[df[x_col_name] == val][y_col_name].quantile(0.75)
        iqr = q3 - q1
        # 外れ値の範囲を取得
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        # 外れ値を除いたデータの平均値をプロット
        df_tmp = df[(df[x_col_name] == val) & (df[y_col_name] >= lower_bound) & (df[y_col_name] <= upper_bound)]
        ax.plot([i], [df_tmp[y_col_name].mean()], marker='x', markersize=8, color='black')

    return ax

def add_brackets(ax, brackets, bracket_base_y = None, dh=1, fs=10):
    """boxplotの追加された状態のaxに[(int, int, str), (int, int, str), ...]で指定される有意差を表示する

    Args:
        ax: matplotlib.pyplot.Axes
        brackets: list of tuple(int, int, str)
            * (int, int, str): (group1, group2, p-value-mark)
            * group1, group2: 有意差を表示する箱ひげ図の位置(1始まり)

    Returns:
        ax: matplotlib.pyplot.Axes
    """
    # bracketsが空の場合は何もしない
    if len(brackets) == 0:
        return ax

    # ax内の箱ひげ図の位置を取得
    xticks = ax.get_xticks()

    # y軸の範囲を取得
    if bracket_base_y is None:
        ylim = ax.get_ylim()
        ylim = [float(ylim[0]), float(ylim[1])]
    else:
        ylim = [0, bracket_base_y]

    # 有意差を表示
    for b in brackets:
        # group1, group2の位置を取得
        x1 = xticks[b[0]-1]
        x2 = xticks[b[1]-1]

        # y軸の位置を取得
        y = ylim[1] - 1

        # group1, group2間にブラケットを表示
        ax.plot([x1, x1, x2, x2], [y, y+1, y+1, y], lw=1, c='black')

        # p-value-markを表示
        # fsにあわせて調整
        fh = fs /10
        ax.text((x1 + x2) / 2, y+1+fh, b[2], ha='center', va='center', color='black', fontsize=fs)

        # y軸の範囲を調整
        ylim[1] += dh

    ax.set_ylim(ylim)

    return ax

def single_describe(df: pd.DataFrame):
    """single_graphで使用したのと同じデータを与えるとその概要を返す関数

    Args:
        df: pandas.DataFrame
            * 1列目: trial_id(試行番号)
            * 2列目: parameter※(パラメータ) ※ファイルにより異なる
            * 3列目: is_assist_continue(実験のアシスト条件(TRUE/FALSE) またはPGT(null))

    Returns:
        describe: pandas.DataFrame
    """
    x_col_name, y_col_name = get_colname(df, False)

    # データの概要を返す
    describe = df.groupby(x_col_name)[y_col_name].describe()

    return describe

def get_colname(df: pd.DataFrame, is_time_seriese):
    """dfの列名を取得する関数

    Args:
        df: pandas.DataFrame
        is_time_seriese: bool
            True: 時系列データの場合
            False: 時系列データでない場合

    Returns:
        x_col_name: str
        y_col_name: str
    """
    if is_time_seriese:
        x_col_name = df.columns[0]
        y_col_name = df.columns[1:]
    else:
        x_col_name = df.columns[2]
        y_col_name = df.columns[1]

    return x_col_name, y_col_name

def time_series_graph(df: pd.DataFrame, ax, **kwargs):
    """
    seaborn.lineplotに処理を追加した関数

    1. 引数
        1. pandas.DataFrame
            * 1列目: frame(フレーム番号): indexに設定していないもの
            * 2列目以降: cond1, cond2, ... (条件1, 条件2, ...)
        1. ax: matplotlib.pyplot.Axes
        1. plotのその他引数(x, y, axを除く)
    1. 返り値
        1. ax: matplotlib.pyplot.Axes
        1. describe: pandas.DataFrame
    1. 処理
        1. 列名毎に時系列グラフをax内に作成
        1. 同一列名のデータは平均値と標準偏差(網掛け)をプロット
    """
    # 時系列グラフの元データを作成
    x_col_name, y_col_name = get_colname(df, True)
    y_col_name = y_col_name.unique()

    mark = ['o', 'x', '^', 'v', '<', '>', 'd', 'p', 'h']

    # condition毎に平均値と標準偏差のdfを作成
    for i, col in enumerate(y_col_name):
        # colを含む列のみを抽出
        df_tmp = df[col]
        # frame列を除いたcol列の平均値と標準偏差を新しいdfとして作成
        df_mean_sd = pd.DataFrame({'frame': df[x_col_name]})
        # df_tmpの平均値と標準偏差を計算
        df_mean_sd[col + '_mean'] = df_tmp.mean(axis=1)
        df_mean_sd[col + '_std'] = df_tmp.std(axis=1)

        # 時系列グラフを作成
        ax = sns.lineplot(x=x_col_name, y=col + '_mean', data=df_mean_sd, ax=ax, label=col, **kwargs)
        # マーカも表示する場合
        #sns.lineplot(x=x_col_name, y=col+'_mean', data=df_mean_sd, ax=ax, label=col, marker=mark[i], markerfacecolor='none', markeredgecolor=sns.color_palette()[i])
        # 平均値に標準偏差を網掛け
        ax.fill_between(df_mean_sd[x_col_name], df_mean_sd[col + '_mean'] - df_mean_sd[col + '_std'], df_mean_sd[col + '_mean'] + df_mean_sd[col +'_std'], alpha=0.2)

    return ax

def time_series_describe(df: pd.DataFrame):
    """time_series_graphで使用したのと同じデータを与えるとその概要を返す関数

    Args:
        df: pandas.DataFrame
            * 1列目: frame(フレーム番号): indexに設定していないもの
            * 2列目以降: cond1, cond2, ... (条件1, 条件2, ...)
    Returns:
        describe: pandas.DataFrame
    """

    x_col_name, y_col_name = get_colname(df, True)
    y_col_name = y_col_name.unique()

    df_ms = []
    cond_cnt = {}
    for i, col in enumerate(y_col_name):
        # colを含む列のみを抽出
        df_tmp = df[col]
        # frame列を除いたcol列の平均値と標準偏差を新しいdfとして作成
        df_mean_sd = pd.DataFrame({'frame': df[x_col_name]})
        # df_tmpの平均値と標準偏差を計算
        df_mean_sd[col + '_mean'] = df_tmp.mean(axis=1)
        df_mean_sd[col + '_std'] = df_tmp.std(axis=1)

        df_ms.append(df_mean_sd.drop(columns='frame'))
        cond_cnt[col] = df_tmp.shape[1]

    # データの概要を返す
    describe = pd.concat(df_ms, axis=1)
    describe = pd.concat([df[x_col_name], describe], axis=1)
    describe = describe.describe()
    for cond, cnt in cond_cnt.items():
        # describeに新しくcond列を追加し，count行にcntを追加
        describe.loc['count', cond+"_trial"] = cnt

    return describe

def set_ax(ax, xlabel, ylabel, config, xlim=None, ylim=None, is_time_series=False):
    """axに対してconfig.ymlで指定したデフォルトのフォントサイズを設定する
    同時にx軸、y軸のラベル名と

    Args:
        ax: matplotlib.pyplot.Axes
        xlabel: x軸のラベル名
        ylabel: y軸のラベル名
        xlim: x軸の範囲
        ylim: y軸の範囲

    Returns:
        ax: matplotlib.pyplot.Axes
    """
    # 凡例を表示
    # ただし実線のみ表示(今回の場合はcond1, cond2)
    # フォントサイズはconfig.ymlで指定し，set_ax関数で設定
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:2], labels[:2])

    # フォントサイズを設定
    ax.set_xlabel(xlabel, fontsize=config['label_font_size'])
    ax.set_ylabel(ylabel, fontsize=config['label_font_size'])
    ax.tick_params(labelsize=config['tick_font_size'])

    # グラフの大きさを設定(画像サイズを1とした場合の比率)
    plt.gcf().subplots_adjust(left=config['graph_limit_left'], right=config['graph_limit_right'], bottom=config['graph_limit_bottom'], top=config['graph_limit_top'])

    # ラベル位置の調整
    ax.xaxis.set_label_coords(config['xlabel_loc_x'], config['xlabel_loc_y'])
    ax.yaxis.set_label_coords(config['ylabel_loc_x'], config['ylabel_loc_y'])

    # グリッドを点線で表示
    ax.grid(linestyle=':')

    # x軸、y軸の範囲を設定
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)

    # is_time_seriesがTrueの場合，x軸のメモリを整数にし，凡例のフォントサイズを設定
    if is_time_series:
        ax.legend(fontsize=config['legend_font_size'])
        ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        # 凡例に同じ文字列が複数表示されるのを防ぐ
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys())
    # is_time_seriesがFalseの場合，凡例を非表示
    else:
        ax.legend().set_visible(False)  # FIXME UserWarningが出るが，凡例を非表示にしないと空の凡例が表示されるため現状このまま

    return ax

if __name__ == '__main__':
    # TEST
    # 試行ごとのパラメータの箱ひげ図
    # データの作成(実際はcsvファイル等から読み込む)
    df = pd.DataFrame({
        'trial_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        'parameter': [1, 2, 3, 10, 5, 6, 7, 8, 9, 10, 10, 11, 9, 14, 16, 17, 17, 15, -1],
        'is_assist_continue': [True, True, True, True, True, False, False, False, False, False, "PGT", "PGT", "PGT", "PGT", "PGT", "PGT", "PGT", "PGT", "PGT"],
        #'is_assist_continue': [False, True, True, True, True, False, False, False, False, False, False, False, True, True, False, False, False, False, False],
        'group': ["A", "A", "A", "B", "B", "A", "A", "A", "B", "B", "A", "A", "A", "A", "B", "B", "B", "B", "B"]
    })

    # グラフの作成(single_graph)
    # fig, ax = plt.subplots()でfig, axを作成
    fig, ax = plt.subplots()
    # 作成した関数を用いてテンプレートに基づくboxplotを作成
    ## 箱ひげ図をax内に作成する
    ax = single_graph(df, ax, hue='is_assist_continue')
    ## 使用したデータの概要を確認する
    describe = single_describe(df)
    ## axの見た目等を設定する
    ax = set_ax(ax, 'condition', 'value', ylim=[-5, 20])

    # 以降，必要に応じて処理を追加
    # x軸の値をcontinue, stop, PGTに変更
    ax.set_xticks(["True", "False", "PGT"], ['continue', 'stop', 'PGT'])

    ax = add_brackets(ax, [(1, 2, 'p<0.05'), (1, 3, 'p<0.01')], bracket_base_y=20, dh=2, fs=10)

    # グラフ等を表示
    print(describe)
    plt.show()

    # 時系列データのグラフ
    # データの作成(実際はcsvファイル等から読み込む)
    data = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            [1, 2, 3, 10, 5, 6, 7, 8, 9, 10, 10, 14, 9, 14, 16, 17, 17, 15, 14],
            [1, 2, 3, 11, 4, 6, 7, 5, 9, 10, 14, 11, 10, 14, 15, 18, 17, 14, 11],
            [1, 2, 3, 17, 6, 6, 7, 6, 9, 10, 12, 12, 9, 12, 14, 17, 18, 13, 14],
            [6, 5, 5, 12, 9, 6, 10, 8, 9, 10, 21, 21, 19, 17, 16, 18, 10, 22, 24],
            [6, 5, 7, 10, 9, 7, 11, 8, 11, 11, 18, 21, 19, 17, 16, 17, 21, 25, 20],
            [8, 4, 8, 15, 10, 8, 12, 8, 11, 15, 20, 21, 18, 11, 16, 11, 24, 29, 10]]
    data_label = ['frame', 'cond1', 'cond1', 'cond2', 'cond2', 'cond3', 'cond3']
    df = pd.DataFrame(data).T
    df = df.set_axis(data_label, axis=1)

    # グラフの作成(time_series_graph)
    # fig, ax = plt.subplots()でfig, axを作成
    fig, ax = plt.subplots()
    # 作成した関数を用いてテンプレートに基づくlineplotを作成
    ## 時系列グラフをax内に作成する
    ax= time_series_graph(df, ax)
    ## 使用したデータの概要を確認する
    describe = time_series_describe(df)
    ## axの見た目等を設定する
    ax = set_ax(ax, 'frame', 'value', ylim=[0, 30], is_time_series=True)

    # 以降，必要に応じて処理を追加

    # グラフ等を表示
    print(describe)
    plt.show()
