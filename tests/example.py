import pandas as pd
import matplotlib.pyplot as plt
import trplots as trp

# サンプルデータの作成
box_data = pd.DataFrame(
    {
        "group": [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2],
        "category": [
            "A",
            "A",
            "A",
            "B",
            "B",
            "C",
            "C",
            "C",
            "A",
            "A",
            "A",
            "B",
            "B",
            "C",
            "C",
            "C",
        ],
        "value": [1, 3, 3, 10, 5, 6, 7, 8, 9, 10, 11, 12, 18, 20, 15, 16],
    }
)

line_data = pd.DataFrame(columns=["A", "A", "A", "A", "A", "B", "B", "B", "C", "C"])
line_data.loc["1"] = [1, 2, 3, 10, 5, 6, 7, 8, 9, 10]
line_data.loc["2"] = [11, 12, 13, 20, 15, 16, 17, 18, 19, 20]
line_data.loc["3"] = [21, 22, 23, 30, 25, 26, 27, 28, 29, 30]
line_data.loc["4"] = [31, 32, 33, 40, 35, 36, 37, 38, 39, 40]
line_data.loc["5"] = [41, 42, 43, 50, 45, 46, 47, 48, 49, 50]
line_data.loc["6"] = [51, 52, 53, 60, 55, 56, 57, 58, 59, 60]
line_data.index = line_data.index.astype(int)

brackets_instructions = [
    ([1, 1], [1, 2], "*"),
    ([1, 2], [2, 2], "**"),
    ([2, 1], [2, 2], "*"),
    ([1, 2], [2, 1], "**"),
]

# matplotlibのfigure, axesを作成 (axを3つ横に並べる)
fig, ax = plt.subplots(1, 3, figsize=(15, 4))

# TrendPlotsクラスのインスタンスを作成
trp_box = trp.TrendPlots(ax[0])
trp_line_ms = trp.TrendPlots(ax[1])
trp_line_gc = trp.TrendPlots(ax[2])

# 箱ひげ図の作成
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

# 線グラフの作成 (平均値と標準偏差を表示)
trp_line_ms.add_line_mean_sd_plot(
    data=line_data, order=["C", "A", "B"], marks=["o", "x", "^"]
)

plt.show()
