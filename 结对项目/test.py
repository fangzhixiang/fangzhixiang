import argparse
import fractions
import re
from fractions import Fraction

# 解析命令行参数
parser = argparse.ArgumentParser(description='Check arithmetic problems against answers.')
parser.add_argument('-e', type=str, required=True, help='Exercise file path.')
parser.add_argument('-a', type=str, required=True, help='Answer file path.')
args = parser.parse_args()

# 读取题目和答案文件
with open(args.e, 'r') as exercise_file:
    exercises = exercise_file.read().splitlines()

with open(args.a, 'r') as answer_file:
    answers = answer_file.read().splitlines()

# 检查题目数量与答案数量是否一致
if len(exercises) != len(answers):
    print("Error: The number of exercises and answers does not match.")
    exit(1)

# 辅助函数：将混合数字符串转换为浮点数
def mixed_number_to_float(mixed_number_str):
    # 使用正则表达式来匹配混合数的格式
    match = re.match(r'(\d+)\'(\d+)/(\d+)', mixed_number_str)
    if match:
        whole_part = int(match.group(1))
        numerator = int(match.group(2))
        denominator = int(match.group(3))
        return "{:.6f}".format(whole_part + numerator / denominator)  # 将答案表示为浮点数
    else:
        match = re.match(r'(\d+)/(\d+)',mixed_number_str)
        if match:
            whole_part = int(match.group(1))
            numerator = int(match.group(2))
            return "{:.6f}".format(whole_part / numerator)
        else:
            return Fraction(mixed_number_str)

# 检查答案是否正确，并统计结果
correct_count = 0
correct_indices = []
wrong_count = 0
wrong_indices = []

for i in range(len(exercises)):
    expression = exercises[i]
    expected_answer_str = answers[i]
    try:
        # 替换特殊字符 '×' 为标准的 '*'
        expression = expression.replace(' × ', ' * ').replace(' ÷ ', ' / ')
        result = eval(expression)
        if result - (result // 1) != 0:
            result = "{:.6f}".format(result)
        expected_answer = mixed_number_to_float(expected_answer_str)
        # 如果结果与答案相匹配，则认为答案正确
        if result == expected_answer:
            correct_count += 1
            correct_indices.append(i + 1)
        else:
            wrong_count += 1
            wrong_indices.append(i + 1)
    except ZeroDivisionError:
        wrong_count += 1
        wrong_indices.append(i + 1)

# 将结果写入Grade.txt文件
with open('Grade.txt', 'w') as grade_file:
    grade_file.write(f"Correct: {correct_count} ({', '.join(map(str, correct_indices))})\n")
    grade_file.write(f"Wrong: {wrong_count} ({', '.join(map(str, wrong_indices))})\n")

print(f"Correct: {correct_count} problems")
print(f"Wrong: {wrong_count} problems")





