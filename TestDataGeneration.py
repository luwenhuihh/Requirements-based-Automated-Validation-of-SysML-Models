import os
import tkinter as tk
from tkinter import messagebox, filedialog
import re
import pandas as pd
import random


# 定义一个类处理需求
class RequirementProcessor:
    def __init__(self):
        # 初始化空的 DataFrame
        self.df = pd.DataFrame(columns=["输入", "期望输出", "模型输出"])

    # 处理 "SHOULD HAVE" 句型
    def process_should_have(self, sentence):
        pattern = r"(.*?)\s+SHOULD\s+HAVE\s+(.*)"
        match = re.match(pattern, sentence)

        if match:
            # 获取期望输出部分
            expected_output = match.group(2)

            # 用正则表达式匹配括号内的内容
            search_modes = re.findall(r'\[(.*?)\]', expected_output)

            # 存储新行数据
            new_rows = []
            if search_modes:
                # 如果有 [] 包裹的内容，给每个模式加上编号
                for idx, mode in enumerate(search_modes):
                    new_rows.append({"输入": idx, "期望输出": mode, "模型输出": ""})

            # 将结果存储为一个新的 DataFrame
            self.df = pd.DataFrame(new_rows, columns=["输入", "期望输出", "模型输出"])

            # 打印当前句子的表格
            print(f"\n表格输出（SHOULD HAVE）:")
            # print(self.df)
        return self.df

    # 处理 "SHOULD support transitions" 句型
    def process_should_support_transitions(self, sentence):
        pattern = r"(.*?)\s+SHOULD\s+support\s+transitions"
        match = re.match(pattern, sentence)

        if match:
            search_modes = re.findall(r'\[(.*?)\]', match.group(1))
            if search_modes:
                # 顺序按照 [0,1,2,0,2,1,0]
                transition_order = [0, 1, 2, 0, 2, 1, 0]
                input_modes = [search_modes[i] for i in transition_order]

                new_rows = []
                for i in range(len(input_modes)):
                    if i == 0:
                        A = input_modes[i]
                    else:
                        A = input_modes[i - 1]
                    B = input_modes[i]
                    C = transition_order[i]

                    # 去掉期望输出中的 []
                    new_rows.append({
                        "输入": C,  # 当前的 mode
                        "期望输出": f"{A} to {B}",  # 从前一个 mode 转到当前 mode，去掉 []
                        "模型输出": ""
                    })

                # 将结果存储为一个新的 DataFrame
                # self.df = pd.DataFrame(new_rows)
                self.df = pd.DataFrame(new_rows, columns=["输入", "期望输出", "模型输出"])

                # 打印当前句子的表格
                print(f"\n表格输出（SHOULD support transitions）:")
                # print(self.df)

        return self.df


    # 处理 "SHOULD BE" 句型
    def process_should_be(self, sentence):
        pattern = r"(.*?)\s+SHOULD\s+BE\s+(.*)"
        match = re.match(pattern, sentence)

        if match:
            # 只提取SHOULD BE 后的 [] 中的内容
            output_match = re.findall(r'\[(.*?)\]', match.group(2))

            # 确保提取到内容
            if output_match:
                new_rows = [{"输入": "null", "期望输出": output_match[0], "模型输出": ""}]
            else:
                # 如果没有找到 [] 内容，使用默认格式
                new_rows = [{"输入": "null", "期望输出": match.group(2), "模型输出": ""}]

            # 将结果存储为一个新的 DataFrame
            self.df = pd.DataFrame(new_rows, columns=["输入", "期望输出", "模型输出"])

            # 打印当前句子的表格
            print(f"\n表格输出（SHOULD BE）:")
            # print(self.df)
        return self.df

    def process_when_input_output(self, sentence):
        # 先将句子分割为多个部分
        parts = sentence.split("==>WHEN INPUT")
        parts = ["==>WHEN INPUT " + part.strip() for part in parts if part.strip()]  # 重新加上 "==>WHEN INPUT"

        # 临时存储所有部分处理后的 DataFrame
        all_dfs = []

        for part in parts:
            if "OUTPUT" in part:
                pattern = r"""==>WHEN\s+INPUT\s+([a-zA-Z\u4e00-\u9fa5]+)(?:\s*(\[[^\]]*\]))?(?:\s*；\s*([a-zA-Z\u4e00-\u9fa5]+)(?:\s*(\[[^\]]*\]))?)?\s*OUTPUT\s+([a-zA-Z\u4e00-\u9fa5]+)(?:\s*(\[[^\]]*\]))?"""
                #
                # matches = re.finditer(pattern, part)

                # pattern = r"""==>WHEN\s+INPUT\s+([a-zA-Z\u4e00-\u9fa5]+)(?:\s*(\[[^\]]*\]))?\s*OUTPUT\s+([a-zA-Z\u4e00-\u9fa5]+)?(?:\s*(\[[^\]]*\]))?"""
                matches = re.finditer(pattern, part)
                for match in matches:
                    input1_keyword = match.group(1)
                    input1_range = match.group(2)  # 取值范围，可能为空
                    output_keyword = match.group(5)
                    output_range = match.group(6)  # 输出的取值范围，可能为空

                    # 生成对应的输入和输出值
                    input1_values = self.generate_values(input1_range)
                    new_rows = []
                    if output_keyword != input1_keyword:
                        output_values = self.generate_values(output_range)
                        # 创建新行数据，纵向填充
                        for i in range(len(input1_values)):
                            row = {
                                "输入": f"{input1_values[i]}",
                                "期望输出": output_values[0],
                                "模型输出": ""
                            }
                            new_rows.append(row)
                    #                         all_dfs.append(pd.DataFrame(new_rows))
                    else:
                        output_values = input1_values
                        for i in range(len(input1_values)):
                            row = {
                                "输入": f"{input1_values[i]}",
                                "期望输出": output_values[i],
                                "模型输出": ""
                            }
                            new_rows.append(row)

                    all_dfs.append(pd.DataFrame(new_rows, columns=["输入", "期望输出", "模型输出"]))

        # 将所有部分的 DataFrame 纵向合并为最终的 DataFrame
        if all_dfs:
            self.df = pd.concat(all_dfs, ignore_index=True)
            # 打印当前句子的表格
            print(f"\n表格输出（多个 WHEN INPUT ... OUTPUT ...）:")
            print(self.df)
        else:
            print("输入句子格式不符合要求")
        return self.df



    def process_when_input_output_2(self, sentence):
        # 先将句子分割为多个部分
        parts = sentence.split("==>WHEN INPUT")
        parts = ["==>WHEN INPUT" + part.strip() for part in parts if part.strip()]  # 重新加上 "==>WHEN INPUT"

        # 临时存储所有部分处理后的 DataFrame
        all_dfs = []

        for part in parts:
            print(part)
            if "OUTPUT" in part:
                #                 print(part)
                # 匹配 ==>WHEN INPUT_1 <keyword1>[<range1>] INPUT_2 <keyword2>[<range2>] OUTPUT[<bool>]
                #                 pattern = r"""==>WHEN\s+INPUT_1\s+([a-zA-Z\u4e00-\u9fa5]+)\[([^\]]*)\]\s+INPUT_2\s+([a-zA-Z\u4e00-\u9fa5]+)\[([^\]]*)\]\s+OUTPUT\[(TRUE|FALSE)\]"""
                # pattern = r"""==>WHEN\s+INPUT_1\s+([a-zA-Z\u4e00-\u9fa5]+)\[([^\]]+)\]\s+INPUT_2\s+([a-zA-Z\u4e00-\u9fa5]+)\[([^\]]+)\]\s+OUTPUT\s*(?:([a-zA-Z\u4e00-\u9fa5]+))?\[([^\]]+)\]"""
                pattern = r"""==>WHEN\s+INPUT_1\s+([a-zA-Z\u4e00-\u9fa5]+)\s*\[([^\]]+)\]\s+INPUT_2\s+([a-zA-Z\u4e00-\u9fa5]+)\s*\[([^\]]+)\]\s+OUTPUT\s*\[([^\]]+)\]"""

                # 查找匹配
                match = re.search(pattern, part)
                if match:
                    # 提取各部分信息
                    input1_keyword = match.group(1)
                    input1_range = match.group(2)  # 输入1的范围
                    input2_keyword = match.group(3)
                    input2_range = match.group(4)  # 输入2的范围
                    output_value = match.group(5)  # 输出的布尔值

                    # 生成输入和输出值
                    input1_values = self.generate_values(input1_range)
                    input2_values = self.generate_values(input2_range)
                    output_values = [output_value] * len(input1_values)

                    # 创建行数据，并追加到 self.df 中
                    new_rows = []
                    for i in range(len(input2_values)):
                        row = {
                            "输入1": f"{input1_values[0]}",
                            "输入2": f"{input2_values[i]}",
                            "期望输出": output_values[0],
                            "模型输出": ""
                        }
                        new_rows.append(row)

                    # 将当前部分的 DataFrame 添加到 all_dfs 列表中
                    all_dfs.append(pd.DataFrame(new_rows, columns=["输入1", "输入2","期望输出", "模型输出"]))
                print(all_dfs)

        # 将所有部分的 DataFrame 纵向合并为最终的 DataFrame
        if all_dfs:
            self.df = pd.concat(all_dfs, ignore_index=True)
            # 打印当前句子的表格
            print(f"\n表格输出（多个 WHEN INPUT ... OUTPUT ...）:")
            # print(self.df)
        else:
            print("输入句子格式不符合要求")
        return self.df


    def process_given(self,sentence,xls_file_path):
        pattern = r'\[(.*?)\]'
        # all_dfs =
        matches = re.findall(pattern, sentence)
        first_bracket_content = matches[0]
        second_bracket_content = matches[1]

        df = pd.read_excel(xls_file_path)
        expected_output = []
        # concatenated_value=''
        if len(matches) < 2:
            # print(matches[2])
            for index, row in df.iterrows():
                print(row[2])
                # 获取第二列的内容
                column_value = row[1]
                column_value_2 = row[2]
                if str(column_value_2).lower() == "true":
                # 拼接第二列内容与第二个中括号内容
                    concatenated_value = f"{'目标距离为:'}{column_value}{','}{second_bracket_content}{','}{matches[2]}{':'}{'空气动力学目标'}"
                if str(column_value_2).lower() == "false":
                # 拼接第二列内容与第二个中括号内容
                    concatenated_value = f"{'目标距离为:'}{column_value}{','}{second_bracket_content}{','}{matches[2]}{':'}{'未知'}"

                # 将拼接后的结果添加到预期输出列表中
                expected_output.append(concatenated_value)
        else:
            for index, row in df.iterrows():
                # 获取第二列的内容
                column_value = row[1]

                # 拼接第二列内容与第二个中括号内容
                concatenated_value = f"{'目标距离为:'}{column_value}{','}{second_bracket_content}"

                # 将拼接后的结果添加到预期输出列表中
                expected_output.append(concatenated_value)

        self.df = pd.DataFrame({
            '输入': [first_bracket_content] * len(df),  # 第一列全部填写第一个中括号的内容
            '预期输出': expected_output,  # 第二列为拼接后的内容
            '模型输出': [''] * len(df)  # 第三列为空
        })

        return self.df




    # 辅助函数，用于根据范围生成值
    def generate_values(self, value_range):
        """生成值，支持范围、符号和布尔值"""
        if not value_range:
            return [""]  # 如果没有定义范围，则返回空值

        value_range = value_range.replace('[', '').replace(']', '').strip()

        if '-' in value_range:  # 处理范围类型，例如 "0-100"
            start, end = map(int, value_range.split('-'))
            return [random.randint(start, end) for _ in range(3)]  # 返回单行随机数
        elif ">=" in value_range:
            threshold = int(value_range.replace('>=', '').strip())
            return [random.randint(threshold, threshold + 10) for _ in range(3)]  # 返回单行大于等于的随机数
        elif ">" in value_range:
            threshold = int(value_range.replace('>', '').strip())
            return [random.randint(threshold + 1, threshold + 10) for _ in range(3)]  # 返回单行大于的随机数
        elif "<=" in value_range:
            threshold = int(value_range.replace('<=', '').strip())
            return [random.randint(0, threshold) for _ in range(3)]  # 返回单行小于等于的随机数
        elif "<" in value_range:
            threshold = int(value_range.replace('<', '').strip())
            return [random.randint(0, threshold - 1) for _ in range(3)]  # 返回单行小于的随机数
        elif value_range.lower() in ["true", "false"]:
            return [value_range]  # 返回布尔值
        else:
            return [str(value_range)]  # 如果是单一值，返回该值

    # 判断输入句子属于哪种句式并调用对应的处理函数
    def identify_and_process_sentence(self, sentence, related_file_path):
        if "SHOULD support transitions" in sentence:
            self.process_should_support_transitions(sentence)
        elif "SHOULD HAVE" in sentence:
            self.process_should_have(sentence)
        elif "SHOULD BE" in sentence:
            self.process_should_be(sentence)
        elif "==>GIVEN" in sentence:
            self.process_given(sentence, related_file_path)
        elif "==>WHEN" in sentence:
            if "INPUT_2" in sentence:
                self.process_when_input_output_2(sentence)
            else:
                self.process_when_input_output(sentence)
                print(sentence)
        else:
            print("无法识别的句型")
        return self.df



# 创建主应用程序窗口
root = tk.Tk()
root.title("需求处理工具")

# 设置窗口大小
root.geometry("600x600")

# 句子输入框和标签
tk.Label(root, text="请输入句子：").pack(pady=5)
sentence_entry = tk.Entry(root, width=80)
sentence_entry.pack(pady=5)

# 文件选择相关需求文件
def select_related_file():
    global related_file_path
    file_path = filedialog.askopenfilename(
        title="选择相关需求文件",
        filetypes=[("Excel Files", "*.xls;*.xlsx"), ("All Files", "*.*")]
    )
    if file_path:
        related_file_path = file_path
        related_file_label.config(text=f"已选择文件: {os.path.basename(file_path)}")
    else:
        related_file_path = None
        related_file_label.config(text="未选择文件")

related_file_path = None  # 初始化相关文件路径为 None

file_frame = tk.Frame(root)
file_frame.pack(pady=5)

select_file_button = tk.Button(file_frame, text="选择相关文件", command=select_related_file)
select_file_button.pack(side=tk.LEFT, padx=5)

related_file_label = tk.Label(file_frame, text="未选择文件")
related_file_label.pack(side=tk.LEFT, padx=5)

# 文件名输入框和标签
tk.Label(root, text="请输入保存的文件名：").pack(pady=5)
filename_entry = tk.Entry(root, width=80)
filename_entry.pack(pady=5)

# 显示 DataFrame 结果的文本框
output_text = tk.Text(root, height=20, width=80, state='disabled')
output_text.pack(pady=10)

# 生成 DataFrame 的函数，接受 related_file_path 作为参数
def generate_df(sentence, related_file):
    processor = RequirementProcessor()
    df = processor.identify_and_process_sentence(sentence, related_file)
    print(df)
    return df

def display_dataframe(df):
    """在输出框中显示 DataFrame 的内容"""
    output_text.configure(state='normal')
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, df.to_string())
    output_text.configure(state='disabled')

def process_sentence():
    """处理输入的句子并更新 DataFrame"""
    sentence = sentence_entry.get()
    if not sentence:
        messagebox.showwarning("输入错误", "请输入句子")
        return

    # 调用生成 DataFrame 的代码，传入相关文件路径
    df_result = generate_df(sentence, related_file_path)

    # 展示 DataFrame 结果
    display_dataframe(df_result)

def save_to_excel():
    """将当前 DataFrame 保存到 Excel 文件中"""
    filename = filename_entry.get().strip()
    if not filename:
        messagebox.showwarning("输入错误", "请输入文件名")
        return

    # 获取句子和相关文件路径
    sentence = sentence_entry.get().strip()
    if not sentence:
        messagebox.showwarning("输入错误", "请输入句子")
        return

    df_result = generate_df(sentence, related_file_path)

    # 检查并设置数据类型
    for col in df_result.columns:
        # 将包含数值的列转换为 int 或 float 类型
        if df_result[col].apply(lambda x: str(x).isdigit()).all():
            df_result[col] = pd.to_numeric(df_result[col], downcast='integer')
        elif df_result[col].apply(lambda x: str(x).replace('.', '', 1).isdigit()).all():
            df_result[col] = pd.to_numeric(df_result[col], downcast='float')
        else:
            # 非数值列设置为字符串类型
            df_result[col] = df_result[col].astype(str)

    # 保存到指定的 Excel 文件
    excel_filename = f"{filename}.xlsx"
    try:
        df_result.to_excel(excel_filename, index=False)
        messagebox.showinfo("保存成功", f"已保存为 {excel_filename}")
    except Exception as e:
        messagebox.showerror("保存失败", f"保存文件时出错: {e}")

# 处理句子的按钮
process_button = tk.Button(root, text="需求处理", command=process_sentence)
process_button.pack(pady=5)

# 保存到 Excel 的按钮
save_button = tk.Button(root, text="保存到Excel文件", command=save_to_excel)
save_button.pack(pady=5)

# 运行主循环
root.mainloop()

