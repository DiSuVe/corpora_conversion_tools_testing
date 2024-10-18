import re
import os
import json


class AddMetadata:
    def __init__(self, input_directory, output_directory):
        self.input_directory = input_directory.rstrip(os.sep)
        self.output_directory = output_directory.rstrip(os.sep)

    def process_articles(self):
        reviewed_articles_dir = os.path.join(self.input_directory, 'reviewed_articles')

        for root, dirs, files in os.walk(reviewed_articles_dir):
            for filename in files:
                # I'm only working with .txt files here
                if filename.endswith('.txt'):
                    base_name = os.path.splitext(filename)[0]
                    if self.is_supplement_file(base_name):
                        continue

                    txt_file_path = os.path.join(root, filename)
                    json_file_path = os.path.join(root, f'{base_name}.json')

                    relative_path = os.path.relpath(root, self.input_directory)
                    output_dir_path = os.path.join(self.output_directory, relative_path)
                    os.makedirs(output_dir_path, exist_ok=True)
                    output_file_path = os.path.join(output_dir_path, filename)

                    self.process_single_file(txt_file_path, json_file_path, output_file_path)

    def is_supplement_file(self, file_name):
        # Assuming all files with an 's' before the digit are supplementary files
        if re.search(r'\.s\d+', file_name, re.IGNORECASE):
            return True
        else:
            return False

    def process_single_file(self, txt_file_path, json_file_path, output_file_path):
        text_content = self.read_text_file(txt_file_path)
        if text_content is None:
            print(f'{txt_file_path} is empty. Skipping file.')
            return

        metadata = self.read_json_file(json_file_path)
        if metadata is None:
            print(f'{json_file_path} does not contain metadata.')
            attributes_str = ''
        else:
            attributes_str = self.metadata_to_attributes(metadata)

        doc_tags = f'<doc {attributes_str}>\n{text_content}\n</doc>'

        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(doc_tags)
        print(f'Metadata added: {output_file_path}')

    def read_text_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                print(f'Text file: {file_path} read successfully.')
                return content
        except UnicodeDecodeError:
            print(f'Couldn\'t read {file_path} with utf-8 encoding due to a UnicodeDecodeError.')
            return None
        except FileNotFoundError:
            print(f'Text file not found: {file_path}')
            return None

    def read_json_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                print(f'Read metadata from: {file_path}.')
                return data
        except FileNotFoundError:
            print(f'JSON file not found: {file_path}')
            return None
        except json.JSONDecodeError as e:
            print(f'Error decoding JSON file {file_path}: {e}')
            return None

    def metadata_to_attributes(self, metadata):
        attributes = []
        for key, value in metadata.items():
            attr_string = self.process_metadata_item(key, value)
            if attr_string:
                attributes.append(attr_string)
        return ' '.join(attributes)

    def process_metadata_item(self, key, value):
        if isinstance(value, dict):
            return self.process_dict_attribute(key, value)
        elif isinstance(value, list):
            return self.process_list_attribute(key, value)
        else:
            attr_value = str(value).replace('"', '&quot;')
            return f'{key}="{attr_value}"'

    def process_dict_attribute(self, parent_key, value_dict):
        attributes = []
        for sub_key, sub_value in value_dict.items():
            full_key = f"{parent_key}_{sub_key}"
            attr_value = str(sub_value).replace('"', '&quot;')
            attributes.append(f'{full_key}="{attr_value}"')
        return ' '.join(attributes)

    def process_list_attribute(self, key, value_list):
        if all(isinstance(item, dict) for item in value_list):
            # List of dictionaries
            flattened = self.flatten_dicts_list(value_list)
            attributes = []
            for sub_key, sub_value in flattened.items():
                full_key = f"{key}_{sub_key}"
                attr_value = sub_value.replace('"', '&quot;')
                attributes.append(f'{full_key}="{attr_value}"')
            return ' '.join(attributes)
        else:
            # List of simple values
            value_str = '; '.join(str(item) for item in value_list)
            attr_value = value_str.replace('"', '&quot;')
            return f'{key}="{attr_value}"'

    def flatten_dicts_list(self, dicts_list):
        flattened = {}
        for item in dicts_list:
            for sub_key, sub_value in item.items():
                sub_value_str = str(sub_value)
                if sub_key in flattened:
                    flattened[sub_key].append(sub_value_str)
                else:
                    flattened[sub_key] = [sub_value_str]
        # Join all values separated by ;
        return {key: '; '.join(values) for key, values in flattened.items()}


if __name__ == '__main__':
    input_dir = '/mdpi_review'
    output_dir = '/mdpi_review/metadata_articles'

    processor = AddMetadata(input_dir, output_dir)
    processor.process_articles()
