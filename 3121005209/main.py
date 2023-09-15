import sys
import difflib
import re
import string

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        sys.exit(1)

def clean_text(text):
    # 去除标点符号和特殊字符
    text = re.sub(f"[{string.punctuation}]", '', text)
    # 将文本转换为小写字母
    text = text.lower()
    return text

def calculate_similarity(original_text, plagiarized_text):
    # 使用difflib库的SequenceMatcher来计算相似性
    original_text = clean_text(original_text)
    plagiarized_text = clean_text(plagiarized_text)

    similarity = difflib.SequenceMatcher(None, original_text, plagiarized_text).ratio()
    return round(similarity, 4)  # 保留四位小数

def main():
    if len(sys.argv) != 4:
        print("Usage: python plagiarism_checker.py <original_file_path> <plagiarized_file_path> <output_file_path>")
        sys.exit(1)

    original_file_path = sys.argv[1]
    plagiarized_file_path = sys.argv[2]
    output_file_path = sys.argv[3]

    original_text = read_file(original_file_path)
    plagiarized_text = read_file(plagiarized_file_path)

    similarity = calculate_similarity(original_text, plagiarized_text)

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(f"{similarity:.2f}\n")
        print("similarity is:"f"{similarity:.2f}\n")

if __name__ == "__main__":
    main()