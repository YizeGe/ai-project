import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st



def make_hist(df, col):
    plt.figure(figsize=(14, 6))
    sns.histplot(df[col].dropna(), bins=20, kde=True)
    plt.xticks(rotation=60)
    plt.title(f"Histogram of {col}")
    plt.tight_layout()
    st.pyplot(plt)


def make_bar(df, col):
    results = df[col].value_counts()
    plt.figure(figsize=(14, 6))
    sns.barplot(x=results.index, y=results.values)
    plt.xticks(rotation=60)
    plt.title(f"Barplot of {col}")
    plt.tight_layout()
    st.pyplot(plt)


'''
Parameters:
    - df: pandas dataframe
    - col: dataframe column name
    - plot_type: type of plot supported: bar, hist
'''
def make_plot(df, col, plot_type):
    if plot_type == "hist":
        make_hist(df, col)
    elif plot_type == "bar":
        make_bar(df, col)
    else:
        print("不支持的图表类型")


def main():
    st.title("表格数据可视化工具")

    uploaded_file = st.file_uploader("请上传 CSV 文件", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
    #else:
    #   df=pd.read_csv("cars_2010_2020.csv")需要本地拥有此文件

        columns = df.columns.tolist()
        selected_col = st.selectbox("请选择要可视化的列", columns)
        plot_type = st.selectbox("请选择图表类型", ["hist", "bar"])
        make_plot(df, selected_col, plot_type)


if __name__ == "__main__":
    main()
