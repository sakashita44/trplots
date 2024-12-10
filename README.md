# trplots

* `trplots`(trend plots)はデータ傾向把握に役立つグラフを生成するためのPythonパッケージ
* 以下のグラフを生成可能: 各グラフの詳細は[使用方法](#使用方法)を参照
    * 箱ひげ図 (外れ値を除いた平均値, 有意差を表すブラケット, データの分布を確かめるJitter plotを追加可能)
    * 系列グラフ (入力データの平均値と標準偏差の網掛けを表示するもの)
        * 個別系列グラフ (入力の個別のデータを表示するもの: 系列グラフの詳細確認用)

## インストール

事前にgitがインストールされている必要がある
以下はsshでのインストール方法

```bash
pip install git@github.com:sakashita44/trplots.git
```

## 依存パッケージ

* matplotlib
* seaborn
* pandas

## 使用方法

### 例: TrendPlotsクラスを使用してグラフを生成する

```python
import pandas as pd
import matplotlib.pyplot as plt
import trplots as trp

# サンプルデータの作成
data = pd.DataFrame({
    "group": [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2],
    "category": ["A","A","A","B","B","C","C","C","A","A","A","B","B","C","C","C",],
    "value": [1, 3, 3, 10, 5, 6, 7, 8, 9, 10, 11, 12, 18, 20, 15, 16]
})

line_data = pd.DataFrame(columns=["A", "A", "A", "A", "A", "B", "B", "B", "C", "C"])
line_data.loc["1"] = [1, 2, 3, 4, 5, 11, 12, 13, 31, 32]
line_data.loc["2"] = [2, 3, 4, 5, 6, 12, 13, 14, 32, 33]
line_data.loc["3"] = [3, 4, 5, 6, 7, 13, 14, 15, 33, 34]
line_data.loc["4"] = [4, 5, 6, 7, 8, 14, 15, 16, 34, 35]
line_data.loc["5"] = [5, 6, 7, 8, 9, 15, 16, 17, 35, 36]
line_data.loc["6"] = [6, 7, 8, 9, 10, 16, 17, 18, 36, 37]
line_data.index = line_data.index.astype(int)

brackets_instructions = [
    ([1, 1], [1, 2], "*"),
    ([1, 2], [2, 2], "**"),
    ([2, 1], [2, 2], "*"),
    ([1, 2], [2, 1], "**"),
]

markers = ["o", "x", "^"]

# matplotlibのfigure, axesを作成 (axを3つ横に並べる)
fig, ax = plt.subplots(1, 3, figsize=(15, 5))

# TrendPlotsクラスのインスタンスを作成
trp_box = trp.TrendPlots(ax[0])
trp_line_ms = trp.TrendPlots(ax[1])
trp_line_gc = trp.TrendPlots(ax[2])

# 箱ひげ図の作成と見た目の設定
trp_box.add_box_mean_plot(
    data=box_data,
    x="group",
    y="value",
    hue="category",
    hue_order=["B", "A", "C"],
    is_add_jitter=True,
    flierprops=trp.FLIERPROPS_DEFAULTS,
)
trp_box.add_brackets(
    brackets=brackets_instructions,
    h_ratio=0.02,
    hspace_ratio=0.1,
    fs=10,
)
trp_box.configure_ax(
    xlabel="Group",
    ylabel="Value",
    label_font_size=12,
    tick_font_size=10,
    legend_correspondence_dict={"A": "Alpha", "B": "Bravo", "C": "Charlie"},
)

# 線グラフの作成 (平均値と標準偏差を表示) と見た目の設定
trp_line_ms.add_line_mean_sd_plot(data=line_data, order=["C", "A", "B"], marks=markers)
trp_line_ms.configure_ax(
    xlabel="Time",
    ylabel="Value",
    label_font_size=12,
    tick_font_size=10,
)

# 線グラフの作成 (グループごとに色分け) と見た目の設定
trp_line_gc.add_line_group_coloring_plot(
    data=line_data, order=["C", "A", "B"], marks=markers
)
trp_line_gc.configure_ax(
    xlabel="Time",
    ylabel="Value",
    label_font_size=12,
    tick_font_size=10,
    legend_correspondence_dict={"A": "Alpha", "B": "Bravo", "C": "Charlie"},
    legend_kwargs={"loc": "upper left"},
)

# 各インスタンスに格納されているグラフの名前を表示
print(f"Graphs in trp_box: {trp_box.graphs_in_ax}")
# Output: "Graphs in trp_box: ['box_mean_plot', 'add_brackets']"

print(f"Graphs in trp_line_ms: {trp_line_ms.graphs_in_ax}")
# Output: "Graphs in trp_line_ms: ['line_mean_sd_plot']"

print(f"Graphs in trp_line_gc: {trp_line_gc.graphs_in_ax}")
# Output: "Graphs in trp_line_gc: ['line_group_coloring_plot']"

# 箱ひげ図が存在するaxesにline_mean_sd_plotを追加する等するとエラーが発生
# trp_box.add_line_group_coloring_plot(
#     data=line_data, order=["C", "A", "B"], marks=markers
# )

plt.show()
```

出力結果:
![example_graph](img/example.png)

### TrendPlotsクラスのメソッド

#### add_box_mean_plot

* 箱ひげ図を作成し，各箱の外れ値を除いた平均値を表示する
* データの分布を確認するためのJitter plotを追加可能

引数:

* data: pd.DataFrame
    * データフレーム
    * 必須カラム: x, y
