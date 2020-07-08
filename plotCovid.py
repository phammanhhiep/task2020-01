import logging, argparse

import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt


logging.basicConfig(filename="plotCovid.log", level=logging.DEBUG)


def plotCaseCountByStates(df, states=None):
    if not isinstance(df, DataFrame):
        raise TypeError("DataFrame is requied")

    if df.empty:
        logging.warning("Empty DataFrame is provided")
        return

    if states is None:
        logging.warning("States are not provided. The graph will be plotted for all states")
    else:
        df = df[df["state"].isin(states)]

    data = df["positive"].groupby(df["state"]).sum()

    if len(data) < len(states):
        logging.warning("{} are either not all (or not) the name of states, or some (or all) \
            of them do not have data".format(",".join(states)))

    ax = data.plot.bar(title="Number of Covid-19 Cases by States")
    ax.set_ylabel("Positive Cases")
    ax.set_xlabel("States")
    rects = ax.patches
    labels = ["{:,}".format(i) for i in data.values]
    for rect, label in zip(rects, labels):
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2, height + 5, label,
                ha='center', va='bottom')    
    plt.show()


if __name__ == "__main__":
    default_graph = "positive_count_by_states"
    default_states = ["NY", "OH", "CA"]
    default_input = "us_states_covid19_daily.csv" 

    parser = argparse.ArgumentParser("Plot Covid")
    parser.add_argument("--graphName", default=default_graph, help="The name \
        of one of the graphs being requested to plot. At this moment, there is only one graph, i.e. {}.".format(default_graph))
    parser.add_argument("--states", default=None, help="A list of state names separated by commas.")
    parser.add_argument("--input", help="The path of data file.")

    args = parser.parse_args()
    graph_name = args.graphName

    if graph_name == default_graph:
        states = args.states; states = states.split(",") if states else default_states
        file_name = args.input; file_name = file_name if file_name else default_input
        df = pd.read_csv(file_name)
        plotCaseCountByStates(df, states)
    else:
        logging.error("{} is not valid graph name".format(graph_name))


