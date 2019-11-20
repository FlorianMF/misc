import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import pandas as pd
    
    
def plot_data(filepath='data.csv'):
    # read the csv file with the pandas lib and extract the values into lists
    data = pd.read_csv(filepath)
    x  = data['x']
    y1 = data['y1']
    y2 = data['y2']

    # clear the plot axes to avoid overlay of lines -> line color will stay the same
    plt.cla()

    # plot both lines
    plt.plot(x, y1, label='Info 1')
    plt.plot(x, y2, label='Info 2')

    # define the legend's position to avoid that matplotlib automatically adapts its position
    plt.legend(loc='upper right')
    plt.tight_layout()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="data plotting parameters")

    parser.add_argument("--interval", type=int, dest="interval", default=1000,
                        help="Time after which the plot is refreshed.") 
    parser.add_argument("--load_path", type=str, dest="load_path", default="data.csv",
                        help="Path to file from which the data shall be read.")                       
    args = parser.parse_args()

    # pass current figure via plt.gcf() and the data plotting function to FuncAnimation, 
    # define the reading interval (time in ms between reading in the data from the csv file)
    FuncAnimation(plt.gcf(), plot_data, interval=args.interval, fargs=args.filepath)
    
    plt.tight_layout()
    plt.show()
