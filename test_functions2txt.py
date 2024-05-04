import pytest
import os
import glob
from functions2txt import Converter2vertical


class TestConverter2vertical:
    def setup_method(self, method):
        test_name = method.__name__
        self.input_dir = 'input_dir'
        self.output_dir = os.path.join('output_dir', test_name)

        os.makedirs(self.output_dir, exist_ok=True)

        self.converter = Converter2vertical(self.input_dir, self.output_dir)

    def test_pdf2txt(self):
        for file_path in glob.glob(os.path.join(self.input_dir, '*.pdf')):
            output_file_path = os.path.join(self.output_dir,
                                            os.path.splitext(os.path.basename(file_path))[0] + '_converted.txt')
            result = self.converter.pdf2txt(file_path)
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(result)
            assert os.path.exists(output_file_path), 'Output file was not created'

    def test_doc2txt(self):
        for file_path in glob.glob(os.path.join(self.input_dir, '*.doc')):
            output_file_path = os.path.join(self.output_dir,
                                            os.path.splitext(os.path.basename(file_path))[0] + '_converted.txt')
            result = self.converter.doc2txt(file_path)
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(result)
            assert os.path.exists(output_file_path), 'Output file was not created'

    def test_docx_2txt(self):
        for file_path in glob.glob(os.path.join(self.input_dir, '*.docx')):
            output_file_path = os.path.join(self.output_dir,
                                            os.path.splitext(os.path.basename(file_path))[0] + '_converted.txt')
            result = self.converter.docx_2txt(file_path)
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(result)
            assert os.path.exists(output_file_path), 'Output file was not created'

    def test_xml2txt(self):
        for file_path in glob.glob(os.path.join(self.input_dir, '*.xml')):
            output_file_path = os.path.join(self.output_dir,
                                            os.path.splitext(os.path.basename(file_path))[0] + '_converted.txt')
            result = self.converter.xml2txt(file_path)
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(result)
            assert os.path.exists(output_file_path), 'Output file was not created'

    def test_txt2vertical(self):
        text = 'This is a test text.'
        expected = 'This\nis\na\ntest\ntext\n.\n </doc>'
        result_1 = self.converter.txt2vertical(text)
        assert result_1 == expected
