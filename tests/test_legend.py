import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import trplots as trp


def test_configure_ax_with_hue_and_legend_kwargs():
    data = pd.DataFrame({
        "x": ["a", "a", "b", "b"],
        "y": [1, 2, 3, 4],
        "hue": ["A", "A", "B", "B"],
    })

    fig, ax = plt.subplots()
    tp = trp.TrendPlots(ax)
    tp.add_box_mean_plot(data=data, x="x", y="y", hue="hue")

    # Should not raise
    tp.configure_ax(xlabel="X", ylabel="Y", legend_kwargs={"title": "Group"})

    # Ensure legend exists
    assert ax.get_legend() is not None
