import gradio as gr
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 生成直方图
def make_hist(df, col):
    plt.figure(figsize=(14, 6))
    sns.histplot(df[col].dropna(), bins=20, kde=True)
    plt.xticks(rotation=60)
    plt.title(f"Histogram of {col}")
    plt.tight_layout()
    return plt

# 生成条形图
def make_bar(df, col):
    results = df[col].value_counts()
    plt.figure(figsize=(14, 6))
    sns.barplot(x=results.index, y=results.values)
    plt.xticks(rotation=60)
    plt.title(f"Barplot of {col}")
    plt.tight_layout()
    return plt

# 根据上传的文件生成图表
def make_plot(file, col, plot_type):
    if file is None:
        return None
    df = pd.read_csv(file.name)

    if plot_type == "hist":
        return make_hist(df, col)
    elif plot_type == "bar":
        return make_bar(df, col)
    else:
        return None

# 获取列名并显示前几行数据，同时更新分组与排序下拉框
def update_dropdowns(file):
    if file is None:
        return (gr.update(choices=[]), gr.update(choices=[]), gr.update(choices=[]), None)
    df = pd.read_csv(file.name)
    column_choices = list(df.columns)
    default = column_choices[0] if column_choices else None
    return (
        gr.update(choices=column_choices, value=default),  # column_dropdown
        gr.update(choices=column_choices, value=default),  # group_col_dropdown
        gr.update(choices=column_choices, value=default),  # sort_col_dropdown
        df.head()
    )

# 分组排序函数
def group_by(file, group_col, sort_col, order):
    if file is None:
        return None
    df = pd.read_csv(file.name)
    ascending = True if order == "升序" else False

    df_sorted = df.sort_values(by=sort_col, ascending=ascending)
    grouped_df = df_sorted.groupby(group_col, group_keys=False).head(10)

    return grouped_df

# Gradio 界面
with gr.Blocks() as demo:
    gr.Markdown("表格数据可视化工具")

    file_input = gr.File(label="上传CSV", file_types=[".csv"])
    output_dataframe = gr.DataFrame()
    column_dropdown = gr.Dropdown(label="选择列", choices=[], interactive=True)
    group_col_dropdown = gr.Dropdown(label="选择分组列", choices=[], interactive=True)
    plot_type = gr.Radio(["hist", "bar"], label="图表类型", value="hist")
    plot_button = gr.Button("生成图表")
    output_plot = gr.Plot()

    gr.Markdown("数据分组与排序")
    sort_col_dropdown = gr.Dropdown(label="选择排序列", choices=[], interactive=True)
    file_input.change(
        fn=update_dropdowns,
        inputs=file_input,
        outputs=[column_dropdown, group_col_dropdown, sort_col_dropdown, output_dataframe]
    )
    plot_button.click(fn=make_plot, inputs=[file_input, column_dropdown, plot_type], outputs=output_plot)

    sort_order = gr.Radio(choices=["升序", "降序"], label="排序方式", value="升序")
    group_button = gr.Button("执行分组排序")
    grouped_output = gr.DataFrame()

    group_button.click(
        fn=group_by,
        inputs=[file_input, group_col_dropdown, sort_col_dropdown, sort_order],
        outputs=grouped_output
    )

demo.launch()