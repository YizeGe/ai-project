import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


df = pd.read_csv("C:\\Users\\bzheng\\source\\repos\\ai-project\\stats\\cars_2010_2020.csv", index_col = 0)
print(df.head())
# print(df.value_counts(df["Model"]))
col = "Year"
plot_type = "hist"


def make_hist(df, col):
    plt.figure(figsize = (14, 6))
    #TODO: specify bins
    sns.histplot(df[col])
    plt.xticks(rotation = 60)
    plt.title(f"Histogram of {col}")
    # plt.show()
    return plt


# hist = make_hist(df, col)
# hist.savefig("hist.png")

def make_bar(df, col):
    #TODO: set head()
    results = df[col].value_counts()
    plt.figure(figsize = (14, 6))
    sns.barplot(
        x = results.index,
        y = results,
        hue = results.index
    )
    plt.xticks(rotation = 60)
    plt.title(f"Barplot of {col}")
    return plt


# bar = make_bar(df, col)
# bar.savefig("bar.png")

'''
Parameters:
    - df: pandas dataframe
    - col: dataframe column name
    - plot_type: type of plot supported: bar, hist
'''
def make_plot(df, col, plot_type):
    if plot_type == "hist":
        hist = make_hist(df, col)
        hist.savefig("hist.png")
    elif plot_type == "bar":
        bar = make_bar(df, col)
        bar.savefig("bar.png")
    else:
        print("Plot type not supported!")


make_plot(df, col, plot_type)