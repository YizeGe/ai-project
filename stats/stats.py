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

# 获取列名并显示前几行数据
def update_dropdowns(file):
    if file is None:
        return gr.update(choices=[]), None
    df = pd.read_csv(file.name)
    column_choices = list(df.columns)
    return gr.update(choices=column_choices, value=column_choices[0] if column_choices else None), df.head()

# Gradio 界面
with gr.Blocks() as demo:
    gr.Markdown("## 📊 表格数据可视化工具（Gradio版）")

    file_input = gr.File(label="上传CSV", file_types=[".csv"])
    output_dataframe = gr.DataFrame()
    column_dropdown = gr.Dropdown(label="选择列", choices=[], interactive=True)
    plot_type = gr.Radio(["hist", "bar"], label="图表类型", value="hist")
    plot_button = gr.Button("生成图表")
    output_plot = gr.Plot()

    file_input.change(fn=update_dropdowns, inputs=file_input, outputs=[column_dropdown, output_dataframe])
    plot_button.click(fn=make_plot, inputs=[file_input, column_dropdown, plot_type], outputs=output_plot)

demo.launch()