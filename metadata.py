# Used to import individual corpus files to SketchEngine
# We assume, as per SketchEngine convention, that the main element is "doc"
# Usage:
# python json_to_xml.py <input_file> > output.xml
#

import sys
import json
import xml.etree.ElementTree as ET


def json_to_sgml(json_data, parent):
    if isinstance(json_data, dict):
        # Convert dictionary items to attributes of the parent element
        for key, value in json_data.items():
            if isinstance(value, list):
                # If it's a list, create a sub-element
                sub_element = ET.SubElement(parent, key)
                for item in value:
                    json_to_sgml(item, sub_element)
            else:
                parent.set(key, str(value))
    elif isinstance(json_data, list):
        # Create sub-elements for list items
        for item in json_data:
            json_to_sgml(item, parent)
    else:
        # Add text content for non-list values
        parent.text = str(json_data)


# Check if a JSON filename is provided as a command-line argument
class InvalidArgumentException(Exception):
    pass


try:
    if len(sys.argv) != 2:
        raise InvalidArgumentException("Usage: python test_using_real_files.py <filename>")

    # Get the JSON filename from the command line argument
    json_filename = sys.argv[1]

    # Load JSON data from the provided file
    with open(json_filename, 'r') as json_file:
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
    print(xml_str[:-6])

except InvalidArgumentException as e:
    print(e)
    sys.exit(1)
except FileNotFoundError:
    print(f"File not found: {json_filename}")
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")
