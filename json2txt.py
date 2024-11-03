import json

def json_to_txt(json_file, txt_file):
    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as jf:
        data = json.load(jf)

    # 打开TXT文件以写入
    with open(txt_file, 'w', encoding='utf-8') as tf:
        # 递归函数用于格式化输出
        def write_item(item, indent=0):
            if isinstance(item, dict):
                for key, value in item.items():
                    tf.write(' ' * indent + f"{key}:\n")  # 写入键并缩进
                    write_item(value, indent + 4)  # 递归写入值，增加缩进
            elif isinstance(item, list):
                for sub_item in item:
                    write_item(sub_item, indent)  # 对于列表，保持相同缩进
            else:
                tf.write(' ' * indent + f"{item}\n")  # 写入普通值

        write_item(data)

# 使用示例
json_to_txt('test.json', 'output.txt')