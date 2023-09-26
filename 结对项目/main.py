import argparse
import random
from fractions import Fraction

# 定义运算符和运算符优先级
operators = ['+', '-', '*', '/']
operator_precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

# 解析命令行参数
parser = argparse.ArgumentParser(description='Generate primary school arithmetic problems.')
parser.add_argument('-n', type=int, required=True, help='Number of problems to generate.')
parser.add_argument('-r', type=int, required=True, help='Range of numbers (up to, exclusive).')
args = parser.parse_args()

# 检查参数是否有效
if args.n <= 0 or args.r <= 1:
    print("Invalid arguments. Please provide a positive number of problems and a range greater than 1.")
    exit(1)

# 生成随机数
def generate_random_number(range_limit):
    return random.randint(1, range_limit - 1)

# 生成随机真分数
def generate_fraction(range_limit):
    numerator = generate_random_number(range_limit)
    denominator = generate_random_number(range_limit)
    while numerator >= denominator:
        numerator = generate_random_number(range_limit)
        denominator = generate_random_number(range_limit)
    return Fraction(numerator, denominator)

# 生成随机算术表达式
def generate_expression(range_limit, depth=0):
    if depth == 0:
        num_operators = random.randint(1, 3)  # 随机生成1到3个运算符
        left = generate_random_number(range_limit)
        right = generate_random_number(range_limit)
        operator = random.choice(operators)
        expression = f'{left} {operator} {right}'
        for _ in range(num_operators - 1):
            operator = random.choice(operators)
            right = generate_random_number(range_limit)
            expression = f'{expression} {operator} {right}'
        return expression
    else:
        left = generate_expression(range_limit, depth - 1)
        right = generate_expression(range_limit, depth - 1)
        operator = random.choice(operators)
        if operator == '/':
            # 除法结果应该是真分数或整数，不会是负数
            while True:
                try:
                    result = eval(f'({left}) {operator} ({right})')
                    if isinstance(result, Fraction) and (result < 0 or result.denominator == 1):
                        left = generate_expression(range_limit, depth - 1)
                        right = generate_expression(range_limit, depth - 1)
                    else:
                        return f'({left}) {operator} ({right})'
                except ZeroDivisionError:
                    left = generate_expression(range_limit, depth - 1)
                    right = generate_expression(range_limit, depth - 1)
        else:
            return f'({left}) {operator} ({right})'

# 转化分数为混合数（mixed number）
def to_mixed_number(frac):
    if frac.numerator == 0:
        return '0'
    whole_part = frac.numerator // frac.denominator
    numerator = frac.numerator % frac.denominator
    if whole_part > 0:
        if numerator > 0:
            return f"{whole_part}'{numerator}/{frac.denominator}"
        else:
            return f"{whole_part}"
    else:
        return f"{frac.numerator}/{frac.denominator}"

# 生成题目和答案
exercises = []
answers = []
i = 0
while i < args.n:
    expression = generate_expression(args.r)
    try:
        result = eval(expression)
        # 确保结果不是负数
        if result >= 0:
            i += 1
            # 如果结果是整数或小数，则转化为混合数
            if result == int(result):
                result = Fraction(int(result))
            else:
                result = Fraction(result).limit_denominator()
            # 将单独的数字（整数或真分数）不加括号
            # expression = expression.replace('(', '').replace(')', '')
            # 替换带有空格的除法运算符为特殊字符，保留不带空格的 *
            expression = expression.replace(' / ', ' ÷ ').replace(' * ', ' × ')
            exercises.append(expression)
            answers.append(result)
    except ZeroDivisionError:
        continue

# 将题目和答案写入文件
with open('Exercises.txt', 'w') as exercise_file:
    exercise_file.write('\n'.join(exercises))

with open('Answers.txt', 'w') as answer_file:
    # 将分数转换为混合数并写入答案文件
    answers = [to_mixed_number(answer) for answer in answers]
    answer_file.write('\n'.join(answers))

print(f"{args.n} arithmetic problems have been generated and saved in Exercises.txt and Answers.txt.")


















































