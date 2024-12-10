import unittest
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# srcディレクトリをパスに追加
sys.path.append(os.path.join(os.path.dirname(__file__), "../trplots"))

from trplots import (
    box_mean_plot,
    add_brackets_for_boxplot,
    line_mean_sd_plot,
    line_group_coloring_plot,
    series_describe,
    configure_ax,
)


class TestGraphFunctions(unittest.TestCase):
    def setUp(self):
        # テスト用のデータフレームを作成
        self.df_wide = pd.DataFrame(
            {
                "uid": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
                "main_id": [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2],
                "sub_id": [
                    "A",
                    "B",
                    "C",
                    "D",
                    "E",
                    "F",
                    "G",
                    "H",
                    "A",
                    "B",
                    "C",
                    "D",
                    "E",
                    "F",
                    "G",
                    "H",
                ],
                "group": [
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
                "value1": [1, 3, 3, 10, 5, 6, 7, 8, 9, 10, 11, 12, 18, 20, 15, 16],
                "value2": [
                    11,
                    12,
                    13,
                    20,
                    15,
                    16,
                    17,
                    18,
                    19,
                    20,
                    21,
                    22,
                    23,
                    30,
                    25,
                    26,
                ],
            }
        )
        self.df_long = pd.DataFrame(
            columns=["A", "A", "A", "A", "A", "B", "B", "B", "B", "C"]
        )
        # value行を追加
        self.df_long.loc["1"] = [1, 2, 3, 10, 5, 6, 7, 8, 9, 10]
        self.df_long.loc["2"] = [11, 12, 13, 20, 15, 16, 17, 18, 19, 20]
        self.df_long.loc["3"] = [21, 22, 23, 30, 25, 26, 27, 28, 29, 30]
        self.df_long.loc["4"] = [31, 32, 33, 40, 35, 36, 37, 38, 39, 40]
        self.df_long.loc["5"] = [41, 42, 43, 50, 45, 46, 47, 48, 49, 50]
        self.df_long.loc["6"] = [51, 52, 53, 60, 55, 56, 57, 58, 59, 60]
        # indexの型をintに変更
        self.df_long.index = self.df_long.index.astype(int)

        self.brackets_instruction_hue = [
            ([1, 1], [1, 2], "*"),
            ([1, 2], [2, 2], "**"),
            ([2, 1], [2, 2], "*"),
            ([1, 2], [2, 1], "**"),
        ]
        self.brackets_instruction_without_hue = [([1, 1], [2, 1], "*")]

    # def test_box_mean_plot(self):
    #     fig, ax = plt.subplots()
    #     hue_order = ["B", "A"]
    #     self.ax = box_mean_plot(
    #         data=self.df_wide,
    #         ax=ax,
    #         x="main_id",
    #         y="value1",
    #         hue="group",
    #         hue_order=hue_order,
    #         add_jitter=False,
    #     )
    #     self.assertIsNotNone(self.ax)
    #     plt.show()
    #     plt.close()

    def test_add_brackets_for_boxplot_with_hue(self):
        fig = plt.figure()
        ax = box_mean_plot(
            data=self.df_wide,
            x="main_id",
            y="value1",
            hue="group",
            hue_order=["B", "A", "C"],
            is_add_jitter=True,
            jitter_setting={
                "marker": "o",
                "linewidth": 1,
                "alpha": 0.7,
            },
            mean_setting={"markeredgewidth": 1.5},
            flierprops={"marker": "x", "markersize": 10},
        )
        ax = add_brackets_for_boxplot(
            ax, self.brackets_instruction_hue, h_ratio=0.02, hspace_ratio=0.1, fs=10
        )
        self.assertIsNotNone(ax)
        fig.add_axes(ax)
        plt.show()
        plt.close()

    def test_add_brackets_for_boxplot_without_hue(self):
        fig = plt.figure()
        ax = box_mean_plot(
            data=self.df_wide,
            x="main_id",
            y="value1",
            is_add_jitter=True,
            jitter_setting={"alpha": 0.7},
            mean_setting={"markeredgewidth": 1.5},
            flierprops={"marker": "x", "markersize": 10},
        )
        ax = add_brackets_for_boxplot(
            ax,
            self.brackets_instruction_without_hue,
            h_ratio=0.02,
            hspace_ratio=0.1,
            fs=10,
        )
        self.assertIsNotNone(ax)
        fig.add_axes(ax)
        plt.show()
        plt.close()

    # def test_line_mean_sd_plot(self):
    #     fig, ax = plt.subplots()
    #     ax = line_mean_sd_plot(
    #         data=self.df_long, ax=ax, order=["A", "C", "B"], marks=["o", "s", "D"]
    #     )
    #     self.assertIsNotNone(ax)
    #     plt.show()
    #     plt.close()

    # def test_line_group_coloring_plot(self):
    #     fig, ax = plt.subplots()
    #     ax = line_group_coloring_plot(
    #         data=self.df_long,
    #         ax=ax,
    #         order=["A", "C", "B"],
    #         marks=["o", "s", "D"],
    #     )
    #     self.assertIsNotNone(ax)
    #     plt.show()
    #     plt.close()

    # def test_series_describe(self):
    #     result = series_describe(self.df_long)
    #     self.assertIsNotNone(result)


if __name__ == "__main__":
    unittest.main()
