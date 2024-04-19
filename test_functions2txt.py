import pytest
import os
import shutil
import glob

from functions2txt import Converter2vertical
from functions2txt import docx_2txt


class TestConverter2vertical:
    def setup_method(self):
        self.test_input_dir = 'input_dir/'
        self.test_output_dir = 'output_dir/'

        """This chunk checks the files in the input directory I created to test, 
        which also includes samples documents with the extensions we need.
        When applied to the mdpi_review folder, it lists every single document inside"""
        print('Input directory:', self.test_input_dir)
        print('Files in this directory:', os.listdir(self.test_input_dir))

        """List of extensions we're working with, however,
        I couldn't find any XML file in the corpus.
        I included a sample document in the input directory"""
        self.supported_extensions = ['.pdf', '.docx', '.xml', '.txt', '.doc']

        """Cleaning up and setting the test environment"""
        if os.path.exists(self.test_output_dir):
            shutil.rmtree(self.test_output_dir)
        os.makedirs(self.test_output_dir, exist_ok=True)

        self.converter = Converter2vertical(self.test_input_dir, self.test_output_dir)

    def test_initialization_directory(self):
        """Checking if the output directory was created correctly.
        This passes without issues, but it's just a temporary fix
        as a new ouput directory is created whenever a new test is run"""
        assert os.path.exists(self.test_output_dir)

    def test_all2txt(self):
        """Test the all2txt method for file conversion across all supported extensions
        Also, checking if there are supported files in the input directory.
        This testing requires more work. At the moment, it's not testing if the final output
        is what we need (.txt + vertical format)"""
        input_files = []
        for extension in self.supported_extensions:
            input_files.extend(glob.glob(os.path.join(self.test_input_dir, '*' + extension)))

        if not input_files:
            pytest.skip('Couldn\'t find any files in the directory')

        try:
            self.converter.all2txt(self.test_input_dir)
        except Exception as e:
            pytest.fail(f'Conversion failed: {e}')

    def test_txt2vertical(self):
        """This chunk tests the conversion of text into vertical format.
        This one passes perfectly all the time."""
        text_1 = 'This is a test text.'
        expected_1 = 'This\nis\na\ntest\ntext\n.\n </doc>'
        result_1 = self.converter.txt2vertical(text_1)
        assert result_1 == expected_1

        text_2 = 'This is a, test text with? punctuation!'
        expected_2 = 'This\nis\na\n,\ntest\ntext\nwith\n?\npunctuation\n!\n </doc>'
        result_2 = self.converter.txt2vertical(text_2)
        assert result_2 == expected_2

    def test_doc2txt(self):
        """Test conversion of .doc text to .txt"""
        for file_path in glob.glob(os.path.join(self.test_input_dir, '*.doc')):
            result = self.converter.doc2txt(file_path)
            output_file_path = os.path.join(self.test_output_dir,
                                            os.path.basename(file_path).replace('.doc', '_converted.txt'))
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(result)
            assert os.path.exists(output_file_path), f'Output file was not created for {file_path}.'

    def test_pdf2txt(self):
        """Test conversion of .pdf text to .txt"""
        for file_path in glob.glob(os.path.join(self.test_input_dir, '*.pdf')):
            result = self.converter.pdf2txt(file_path)
            output_file_path = os.path.join(self.test_output_dir,
                                            os.path.basename(file_path).replace('.pdf', '_converted.txt'))
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(result)
            assert os.path.exists(output_file_path), f'Output file was not created for {file_path}.'

    def test_xml2txt(self):
        """Test conversion of .xml text to .txt"""
        for file_path in glob.glob(os.path.join(self.test_input_dir, '*.xml')):
            result = self.converter.xml2txt(file_path)
            output_file_path = os.path.join(self.test_output_dir,
                                            os.path.basename(file_path).replace('.xml', '_converted.txt'))
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(result)
            assert os.path.exists(output_file_path)


class TestDocxConverter:
    def setup_method(self):
        """Set up the test environment"""
        self.test_input_dir = 'input_dir/'
        self.test_output_dir = 'output_dir'

        if not os.path.exists(self.test_output_dir):
            os.makedirs(self.test_output_dir, exist_ok=True)

    """The following chunk generated an error which I suspect was generated by naming
    the function after the library (same name)
    Changing the name of the function in the original script fixed this"""

    def test_docx_2txt(self):
        """Test conversion of .docx text to .txt"""
        for file_path in glob.glob(os.path.join(self.test_input_dir, '*.docx')):
            result = docx_2txt(file_path)
            output_file_path = os.path.join(self.test_output_dir,
                                            os.path.basename(file_path).replace('.docx', '_converted.txt'))
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                output_file.write(result)
            assert os.path.exists(output_file_path)
