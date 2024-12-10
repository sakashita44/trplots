import os
import matplotlib.pyplot as plt
import pandas as pd
import yaml
import schemeta_splitter.io as ss

import graph

VIS_ROOT_DIR = os.path.join(os.path.dirname(__file__), "..\\")
INPUT_DIR = os.path.join(VIS_ROOT_DIR, "Inputs\\")
OUTPUT_DIR = os.path.join(VIS_ROOT_DIR, "Outputs\\")
CONFIG_YML = os.path.join(VIS_ROOT_DIR, "config.yml")
INST_CSV = os.path.join(INPUT_DIR, "instructions.csv")


def read_instructions():
    with open(INST_CSV, "r") as f:
        lines = f.readlines()
        instructions = [line.strip() for line in lines]

    # Remove the header
    instructions_val = instructions[1:]
    instructions_head = instructions[0].split(",")
    instructions_head = [head.strip() for head in instructions_head]

    # check the header
    if instructions_head != [
        "output_name",
        "filename",
        "dtype",
        "graph_type",
        "xlim_min",
        "xlim_max",
        "ylim_min",
        "ylim_max",
        "xlabel",
        "ylabel",
        "legend",
        "brackets",
        "bracket_base_y",
    ]:
        raise ValueError("The header of instructions.csv is invalid")

    # Convert the instructions to a list of dictionary
    instructions_ret = []
    for inst in instructions_val:
        inst = inst.split(",")
        inst = [i.strip() for i in inst]
        inst_dict = dict(zip(instructions_head, inst))

        # Convert the string to int
        if inst_dict["xlim_min"] != "":
            inst_dict["xlim_min"] = float(inst_dict["xlim_min"])
        if inst_dict["xlim_max"] != "":
            inst_dict["xlim_max"] = float(inst_dict["xlim_max"])
        if inst_dict["ylim_min"] != "":
            inst_dict["ylim_min"] = float(inst_dict["ylim_min"])
        if inst_dict["ylim_max"] != "":
            inst_dict["ylim_max"] = float(inst_dict["ylim_max"])
        if inst_dict["bracket_base_y"] != "":
            inst_dict["bracket_base_y"] = float(inst_dict["bracket_base_y"])

        # Convert the legend to a dictionary
        if inst_dict["legend"] != "":
            legend = inst_dict["legend"]
            legend = legend.split(".")
            legend = [l.strip() for l in legend]
            legend = [l.split(":") for l in legend]
            legend = {l[0]: l[1] for l in legend}
            inst_dict["legend"] = legend
        else:
            inst_dict["legend"] = {}

        # Convert the brackets to a list of taple([int, int], [int, int], str)
        # ex [1:1][1:2]*.[1:3][2:3]** -> [([1, 1], [1, 2], "*"), ([1, 3], [2, 3], "**")]
        if inst_dict["brackets"] != "":
            brackets = inst_dict["brackets"]
            brackets = brackets.split(".")
            b_ret = []
            for b in brackets:
                b = b.split("]")
                b = [item.replace("[", "") for item in b if item]
                b = [item.split(":") for item in b]
                b[0] = int(b[0][0]), int(b[0][1])
                b[1] = int(b[1][0]), int(b[1][1])
                b[2] = b[2][0]
                b_ret.append(b)
            inst_dict["brackets"] = b_ret
        else:
            inst_dict["brackets"] = []

        instructions_ret.append(inst_dict)

    return instructions_ret


def read_data(path: str) -> pd.DataFrame:
    full_path = os.path.join(INPUT_DIR, path)
    data = pd.read_csv(full_path, index_col=0)

    return data


def read_config():
    with open(CONFIG_YML, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config


def gen_box_graph(
    data: pd.DataFrame,
    ax: plt.Axes,
    inst: dict,
    config: dict,
    use_all=False,
    x_col_num=0,
    y_col_num=3,
    hue_col_num=2,
    x=None,
    y=None,
    hue=None,
):
    """
    instructionsやconfigに従って箱ひげ図を生成する


    Parameters
    ----------
    data : pd.DataFrame
        データ
    ax : plt.Axes
        グラフを描画するAxes
    inst : dict
        instructions
    config : dict
        config
    use_all : bool, optional
        xで分割せずにすべてのデータを使用するかどうか, by default False
    x_col_num : int, optional
        xの列番号, by default 0
        xで列名が指定されている場合, 両者が一致している必要がある
    y_col_num : int, optional
        yの列番号, by default 3
        yで列名が指定されている場合, 両者が一致している必要がある
    hue_col_num : int, optional
        hueの列番号, by default 2
        hueで列名が指定されている場合, 両者が一致している必要がある
    x : str, optional
        xの列名, by default None
    y : str, optional
        yの列名, by default None
    hue : str, optional
        hueの列名, by default None
    """
    # データ形式が転置の場合，wide形式に変換
    if inst["dtype"] == "tp":
        meta, data = ss.split_dataframe(df=data, is_wide_format=False)
        data = ss.concatenate_dataframes(meta, data, get_wide_format=True)

    hue_order = get_order(inst)

    # x, y, hueの指定がある場合はそれを使用
    if x is None:
        x = data.columns[x_col_num]
    elif x != data.columns[x_col_num]:
        raise ValueError("x and x_col_num do not match")

    if y is None:
        y = data.columns[y_col_num]
    elif y != data.columns[y_col_num]:
        raise ValueError("y and y_col_num do not match")

    if hue is None:
        if hue_col_num is not None:
            hue = data.columns[hue_col_num]
    elif hue != data.columns[hue_col_num]:
        raise ValueError("hue and hue_col_num do not match")

    if use_all:
        # data[x]の値をすべて空文字に変換することでxで分割しない
        data[x] = ""

    ax = graph.box_mean_plot(
        data=data,
        ax=ax,
        x=x,
        y=y,
        hue=hue,
        hue_order=hue_order,
        jitter_setting={
            "marker": "o",
            "hue_order": hue_order,
            "linewidth": 1,
            "alpha": 0.7,
        },
    )

    if config["show_significance_brackets"]:
        if inst["brackets"] != []:
            graph.add_brackets_for_boxplot(
                ax=ax,
                brackets=inst["brackets"],
                bracket_base_y=inst["bracket_base_y"],
                h_ratio=config["brackets_height_ratio"],
                hspace_ratio=config["brackets_spacing_ratio"],
                fs=config["p_mark_font_size"],
            )

    return ax, x, y, hue


def gen_line_graph(data: pd.DataFrame, ax: plt.Axes, inst: dict):
    data = get_long_data(data, inst)

    order = get_order(inst)
    ax = graph.line_mean_sd_plot(data=data, ax=ax, order=order)

    return ax


def gen_line_individual_graph(data: pd.DataFrame, ax: plt.Axes, inst: dict):
    data = get_long_data(data, inst)

    order = get_order(inst)
    ax = graph.line_group_coloring_plot(data=data, ax=ax, order=order)

    return ax


def get_long_data(data: pd.DataFrame, inst: dict):
    if inst["dtype"] == "wide":
        is_wide = True
    else:
        is_wide = False

    meta, data = ss.split_dataframe(df=data, is_wide_format=is_wide)
    # metaの3列目をgroupsに使用
    groups = meta.iloc[:, 2]
    # dataを転置
    data = data.T
    # 列名をgroupsを用いて変更
    data.columns = groups

    # indexを数値に変換
    data.index = data.index.astype(float)
    # すべての列の型をfloatに変換
    data = data.astype(float)

    return data


def get_order(inst: dict):
    # legendの指定がある場合はorderを指定
    if inst["legend"] != {}:
        order = list(inst["legend"].keys())
    else:
        order = None

    return order


def set_ax_wrap(ax, inst, config):
    xlabel = inst["xlabel"]
    ylabel = inst["ylabel"]
    xlim_min = inst["xlim_min"]
    xlim_max = inst["xlim_max"]
    if (xlim_min != "") and (xlim_max != ""):
        xlim = [xlim_min, xlim_max]
    else:
        xlim = None
    ylim_min = inst["ylim_min"]
    ylim_max = inst["ylim_max"]
    if (ylim_min != "") and (ylim_max != ""):
        ylim = [ylim_min, ylim_max]
    else:
        ylim = None
    graph_type = inst["graph_type"]
    legend_correspondence_dict = inst["legend"]
    label_font_size = config["label_font_size"]
    tick_font_size = config["tick_font_size"]
    legend_font_size = config["legend_font_size"]
    graph_limit_left = config["graph_limit_left"]
    graph_limit_right = config["graph_limit_right"]
    graph_limit_bottom = config["graph_limit_bottom"]
    graph_limit_top = config["graph_limit_top"]
    xlabel_loc_x = config["xlabel_loc_x"]
    xlabel_loc_y = config["xlabel_loc_y"]
    ylabel_loc_x = config["ylabel_loc_x"]
    ylabel_loc_y = config["ylabel_loc_y"]

    ax = graph.set_ax(
        ax=ax,
        xlabel=xlabel,
        ylabel=ylabel,
        xlim=xlim,
        ylim=ylim,
        graph_type=graph_type,
        legend_correspondence_dict=legend_correspondence_dict,
        label_font_size=label_font_size,
        tick_font_size=tick_font_size,
        legend_font_size=legend_font_size,
        graph_limit_left=graph_limit_left,
        graph_limit_right=graph_limit_right,
        graph_limit_top=graph_limit_top,
        graph_limit_bottom=graph_limit_bottom,
        xlabel_loc_x=xlabel_loc_x,
        xlabel_loc_y=xlabel_loc_y,
        ylabel_loc_x=ylabel_loc_x,
        ylabel_loc_y=ylabel_loc_y,
    )

    return ax


def test_path(dir_path: str):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def save_set_graph(inst: dict, config: dict):
    data = read_data(inst["filename"])
    dpi = config["figure_dpi"]
    figure_width = config["figure_width"]
    figure_height = config["figure_height"]
    fig, ax = plt.subplots()
    fig.set_size_inches(figure_width, figure_height)

    x = None
    y = None
    hue = None
    if inst["graph_type"] == "box":
        ax, x, y, hue = gen_box_graph(data, ax, inst, config)
    elif inst["graph_type"] == "line":
        ax = gen_line_graph(data, ax, inst)
    else:
        print(f"Invalid graph type. Skipping {inst['output_name']}")
        return

    ax = set_ax_wrap(ax, inst, config)
    save_graphs(fig, inst["output_name"], dpi)

    if config["show_graph"]:
        plt.show()

    if config["save_describe"]:
        save_describe(data, inst, x, y, hue)

    plt.close()

    # 個別のデータをプロットしたグラフを保存
    if config["save_individual"] and inst["graph_type"] == "line":
        fig, ax = plt.subplots()
        fig.set_size_inches(figure_width, figure_height)
        ax = gen_line_individual_graph(data, ax, inst)
        ax = set_ax_wrap(ax, inst, config)
        save_graphs(fig, inst["output_name"] + "_individual", dpi)
        plt.close()


def save_graphs(fig: plt.Figure, output_name: str, dpi: int):
    out_path = os.path.join(OUTPUT_DIR, output_name)
    test_path(os.path.dirname(out_path))

    fig.savefig(out_path, dpi=dpi)


def save_describe(data: pd.DataFrame, inst: dict, x=None, y=None, hue=None):
    if inst["graph_type"] == "line":
        describe = graph.series_describe(data)
    elif inst["graph_type"] == "box":
        if x is None:
            raise ValueError("x is required for box graph")
        if y is None:
            raise ValueError("y is required for box graph")
        describe = graph.single_describe(data, x, y, hue)
    else:
        print(f"Invalid graph type. Skipping {inst['output_name']}")
        return

    # floatの桁数を指定してcsvに保存
    describe.to_csv(
        os.path.join(OUTPUT_DIR, inst["output_name"] + "_describe.csv"),
        index=True,
        float_format="%.3f",
    )


def gen_graph():
    instructions = read_instructions()
    config = read_config()

    for inst in instructions:
        # グラフを確認しつつ保存
        print(f"Generating {inst['output_name']}")
        save_set_graph(inst, config)


if __name__ == "__main__":
    gen_graph()
