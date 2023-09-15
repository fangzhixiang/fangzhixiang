import unittest
from main import read_file, clean_text, calculate_similarity

class MyTestCase(unittest.TestCase):

    #测试read_file函数
    def test_read_file(self):
        # 创建一个临时文本文件供测试使用
        with open('temp.txt', 'w', encoding='utf-8') as temp_file:
            temp_file.write('This is a test text.')

        # 测试文件存在的情况
        content = read_file('temp.txt')
        self.assertEqual(content, 'This is a test text.')

        # 测试文件不存在的情况
        with self.assertRaises(SystemExit):
            content = read_file('nonexistent_file.txt')

    #测试clean_text函数
    def test_clean_text(self):
        input_text = "Hello, World! This is a test text."
        expected_output = "hello world this is a test text"
        cleaned_text = clean_text(input_text)
        self.assertEqual(cleaned_text, expected_output)

    #测试caculate_similarity函数
    def test_calculate_similarity(self):
        original_text = "This is the original text."
        plagiarized_text = "This Is The Original Text."
        similarity = calculate_similarity(original_text, plagiarized_text)
        self.assertAlmostEqual(similarity, 1.0, places=2)


if __name__ == '__main__':
    unittest.main()
