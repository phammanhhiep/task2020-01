import logging, argparse

import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt


logging.basicConfig(filename="plotCovid.log", level=logging.DEBUG)


def plotCasesByStates(df, states=None):
    if not isinstance(df, DataFrame):
        raise TypeError("DataFrame is requied")

    if df.empty:
        logging.warning("Empty DataFrame is provided")
        return

    if states is None:
        logging.warning("States are not provided. The graph will be plotted for all states.")
    else:
        df = df[df["state"].isin(states)]

    data = df["positive"].groupby(df["state"]).sum()
    ax = data.plot.bar(title="Number of Covid-19 Cases by States")
    ax.set_ylabel("Positive Cases")
    ax.set_xlabel("States")
    plt.show()


if __name__ == "__main__":
    default_graph = "positive_count_by_states"
    parser = argparse.ArgumentParser("Plot Covid")
    parser.add_argument("--graphName", default=default_graph, help="Provide one of the name \
        of the graphs, including, {}.".format(default_graph))
    parser.add_argument("--states", default=None, help="A list of state names separated by commas")
    parser.add_argument("--input", help="path to data file")

    args = parser.parse_args()
    graph_name = args.graphName

    if graph_name == default_graph:
        states = args.states; states = states.split(",") if states else ["NY", "OH", "CA"]
        file_name = args.input; file_name = file_name if file_name else "us_states_covid19_daily.csv" 
        df = pd.read_csv(file_name)
        plotCasesByStates(df, states)
    else:
        logging.debug("{} is not valid graph name".format(graph_name))


