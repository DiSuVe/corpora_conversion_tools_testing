import os
import shutil

import docx2txt
import glob
import json
import aspose.words as aw
import re
from pdfminer.high_level import extract_text
import xml.etree.ElementTree as ET
from metadata import json_to_sgml


class Converter2vertical:
    def __init__(self, inpath, outpath):
        """
        Initializes an instance of the class with the specified input and output paths.

        Args:
            inpath (str): The path to the input directory.
            outpath (str): The path to the output directory.

        Returns:
            None
        """
        self.inpath = inpath
        self.outpath = outpath
        self.extensions = ['.docx', '.doc', '.xml', '.pdf', '.txt']
        self.extensions_dict = {'.docx': self.docx_2txt,
                                '.doc': self.doc2txt,
                                '.xml': self.xml2txt,
                                '.pdf': self.pdf2txt, '.txt': lambda x: x.read()}

        def ignore_files(directory, files):
            return [f for f in files if os.path.isfile(os.path.join(directory, f))]

        # calling the shutil.copytree() method and passing the src,dst,and ignore parameter
        if os.path.exists(self.outpath):
            shutil.rmtree(self.outpath)
        shutil.copytree(self.inpath, self.outpath, ignore=ignore_files)

    def iterate_through_corpus(self):
        """
        Iterates through the corpus by iterating over each directory in the "reviewed_articles" folder.
        If a directory has a "sub-articles" subdirectory, it calls the "all2txt" method with the
        path to the "sub-articles" subdirectory.
        Parameters:
        self (object): The instance of the class.
        Returns:
        None
        """
        for directory in os.listdir(self.inpath + 'reviewed_articles/'):
            if os.path.isdir(self.inpath + 'reviewed_articles/' + directory + '/sub-articles'):
                self.all2txt('reviewed_articles/' + directory + '/sub-articles')

    def all2txt(self, directory_path):
        """
        Convert all files in a specified directory to a text format.

        Args:
            directory_path (str): The path to the directory containing the files to be converted.

        Returns:
            None
        """
        for extension in self.extensions:
            directory = glob.glob(self.inpath + directory_path + '/*' + extension)
            for file_name in directory:
                with open(self.outpath + file_name[len(self.inpath):-len(extension)] + '.txt', 'w',
                          encoding='utf-8') as outfile:
                    # Extract the file name without extension
                    review_name, _ = os.path.splitext(file_name)

                    # Check if the file name contains "s" followed by an integer
                    parts = review_name.split(".")
                    if parts[-1].startswith("s") and parts[-1][1:].isdigit():
                        # Replace "s" with "r" and append the metadata extension
                        metadata_name = ".".join(parts[:-1]) + ".r" + parts[-1][1:] + '.json'
                    else:
                        # If there is no "s" in the file name, just append the metadata extension
                        metadata_name = review_name + '.json'
                    doc_tag = self.add_metadata(metadata_name)

                    # PROBLEM WITH SUPPLEMENTARY MATERIALS
                    if doc_tag is not None:
                        outfile.write(doc_tag)
                    with open(file_name, 'rb') as infile:
                        # print('Converting '+file_name)
                        doc = self.extensions_dict[extension](infile)
                        if doc is not None:
                            doc = self.txt2vertical(doc)
                            outfile.write(doc)

    def doc2txt(self, file):
        """
        Converts a doc file to a txt file.

        Parameters:
            file (str): The path of the doc file to convert.

        Returns:
            str: The text content of the converted txt file.
        """
        doc_text = aw.Document(file)
        text = doc_text.get_text().splitlines()
        clean_text = '\n'.join(text[1:-4])
        return clean_text

    def pdf2txt(self, file):
        """
        Converts a PDF file to a text file.

        Args:
            file (str): The path of the PDF file to be converted.

        Returns:
            str or None: The extracted text from the PDF file if conversion is successful,
            None if there is an error while converting.
        """
        try:
            return extract_text(file)
        except Exception as e:
            print(f'Error while converting: {str(e)}')
            return None

    def xml2txt(self, file):
        """
        Converts an XML file to a text file.

        Parameters:
            file (str): The path to the XML file.

        Returns:
            str: The text content extracted from the XML file.
        """
        tree = ET.parse(file)
        root = ET.tostring(tree.getroot(), encoding='utf-8', method='text')
        return root.decode('utf-8')

    def docx_2txt(self, file):
        """
        Converts a docx file to a txt file.

        Args:
            file (str): The path to the docx file.

        Returns:
            str: The content of the converted txt file.
        """
        return docx2txt.process(file)

    def txt2vertical(self, text):
        """
        Converts a text file to a vertical file.

        Parameters:
            text (str): The text file to be converted.

        Returns:
            str: The converted vertical file.
        """
        if type(text) != str:
            text = str(text)
        splited = re.findall(r'\w+|[^\s\w]+', text)
        return '\n'.join(splited) + '\n </doc>'

    def add_metadata(self, json_filename):
        """
        Adds metadata from a JSON file to an XML document.

        Parameters:
            json_filename (str): The path to the JSON file.

        Returns:
            str: The XML document as a string.

        Raises:
            FileNotFoundError: If the JSON file is not found.
            json.JSONDecodeError: If there is an error parsing the JSON.
        """
        try:
            # Load JSON data from the provided file
            with open(json_filename, 'r') as json_file:
                print('Adding metadata from ' + json_filename)
                json_data = json.load(json_file)

            # Create the root "doc" element
            root = ET.Element("doc")

            # Convert JSON to SGML/XML
            json_to_sgml(json_data, root)

            # Create an ElementTree object
            tree = ET.ElementTree(root)

            # Print or save the XML as needed
            xml_str = ET.tostring(root, encoding="unicode")
            # Do not close the doc element: we will add sentences after it.
            return xml_str

        except FileNotFoundError:
            print(f"File not found: {json_filename}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
