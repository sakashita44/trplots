import os
import matplotlib.pyplot as plt
import pandas as pd
import yaml

import graph

VIS_ROOT_DIR = os.path.join(os.path.dirname(__file__), "..\\")
INPUT_DIR = os.path.join(VIS_ROOT_DIR, "Inputs\\")
OUTPUT_DIR = os.path.join(VIS_ROOT_DIR, "Outputs\\")
CONFIG_YML = os.path.join(VIS_ROOT_DIR, "config.yml")
INST_CSV = os.path.join(INPUT_DIR, "instructions.csv")

def read_instructions():
    with open(INST_CSV, 'r') as f:
        lines = f.readlines()
        instructions = [line.strip() for line in lines]

    # Remove the header
    instructions_val = instructions[1:]
    instructions_head = instructions[0].split(",")
    instructions_head = [head.strip() for head in instructions_head]

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

        # Convert the string to bool
        inst_dict["is_time_series"] = inst_dict["is_time_series"] == "TRUE"

        # Convert the legend to a dictionary
        if inst_dict["legend"] != "":
            legend = inst_dict['legend']
            legend = legend.split(".")
            legend = [l.strip() for l in legend]
            legend = [l.split(":") for l in legend]
            legend = {l[0]: l[1] for l in legend}
            inst_dict['legend'] = legend
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
    data = pd.read_csv(full_path)

    # Read the header
    with open(full_path, 'r') as f:
        lines = f.readlines()
        header = lines[0]
        header = header.split(",")
        header = [h.strip() for h in header]

    # Set the collected header
    data.columns = header

    return data

def read_config():
    with open(CONFIG_YML, encoding = 'utf-8') as f:
        config = yaml.safe_load(f)

    return config

def gen_single_graph(data: pd.DataFrame, ax: plt.Axes, inst: dict, config: dict):
    ax = graph.concat_single_graph(data, ax)

    if config["add_brackets"]:
        if inst["brackets"] != []:
            graph.add_brackets_for_concat_single(ax, inst["brackets"], bracket_base_y = inst["bracket_base_y"], dh = config["brackets_dh"], fs=config["p_mark_font_size"])

    return ax

def gen_time_series_graph(data: pd.DataFrame, ax: plt.Axes):
    ax = graph.time_series_graph(data, ax)

    return ax

def gen_time_series_individual_graph(data: pd.DataFrame, ax: plt.Axes):
    ax = graph.time_series_indiv_graph(data, ax)

    return ax

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
    is_time_series = inst["is_time_series"]
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

    ax = graph.set_ax(ax=ax, xlabel=xlabel, ylabel=ylabel, xlim=xlim, ylim=ylim, is_time_series=is_time_series, legend_correspondence_dict=legend_correspondence_dict,\
                     label_font_size=label_font_size, tick_font_size=tick_font_size, legend_font_size=legend_font_size,\
                         graph_limit_left=graph_limit_left, graph_limit_right=graph_limit_right, graph_limit_top=graph_limit_top, graph_limit_bottom=graph_limit_bottom,\
                             xlabel_loc_x=xlabel_loc_x, xlabel_loc_y=xlabel_loc_y, ylabel_loc_x=ylabel_loc_x, ylabel_loc_y=ylabel_loc_y)

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

    if inst["is_time_series"]:
        # dataの1列目の名前をframeに変更
        data = data.rename(columns={data.columns[0]: "frame"})
        ax = gen_time_series_graph(data, ax)
    else:
        ax = gen_single_graph(data, ax, inst, config)

    ax = set_ax_wrap(ax, inst, config)
    save_graphs(fig, inst['output_name'], dpi)

    if config["show_graph"]:
        plt.show()

    if config["save_describe"]:
        save_describe(data, inst)

    plt.close()

    # 個別のデータをプロットしたグラフを保存
    if config["save_individual"] and inst["is_time_series"]:
        fig, ax = plt.subplots()
        fig.set_size_inches(figure_width, figure_height)
        ax = gen_time_series_individual_graph(data, ax)
        ax = set_ax_wrap(ax, inst, config)
        save_graphs(fig, inst['output_name'] + "_individual", dpi)
        plt.close()

def save_graphs(fig: plt.Figure, output_name: str, dpi: int):
    out_path = os.path.join(OUTPUT_DIR, output_name)
    test_path(os.path.dirname(out_path))

    fig.savefig(out_path, dpi=dpi)

def save_describe(data: pd.DataFrame, inst: dict):
    if inst["is_time_series"]:
        describe = graph.time_series_describe(data)
    else:
        describe = graph.single_describe(data)

    # floatの桁数を指定してcsvに保存
    describe.to_csv(os.path.join(OUTPUT_DIR, inst['output_name'] + "_describe.csv"), index = True, float_format = '%.3f')

def gen_graph():
    instructions = read_instructions()
    config = read_config()

    for inst in instructions:
        # グラフを確認しつつ保存
        print(f"Generating {inst['output_name']}")
        save_set_graph(inst, config)

if __name__ == "__main__":
    gen_graph()
