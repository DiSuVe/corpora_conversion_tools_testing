import os
import shutil
import json


def get_dict(inpath, outpath):
    d = {}
    for directory in os.listdir(inpath):
        if os.path.isdir(inpath + directory + '/sub-articles'):
            for file in os.listdir(inpath + directory + '/sub-articles'):

                extension = file.split('.')[-1]
                if extension not in d.keys():
                    d[extension] = 1

                    shutil.copy(inpath + directory + '/sub-articles/' + file, outpath)

                else:
                    d[extension] += 1
        else:
            for file in os.listdir(inpath + directory):

                extension = file.split('.')[-1]
                if extension not in d.keys():
                    d[extension] = 1

                    shutil.copy(inpath + directory + '/' + file, outpath)

                else:
                    d[extension] += 1

                if extension == 'json' and file.split('.')[0] != 'metadata':
                    print(file.split('.')[0])
    print(d)


def flat_builder():
    inpath = './mdpi_review/reviewed_articles/'
    outpath = './flat/mdpi/'
    for directory in os.listdir(inpath):
        if os.path.isdir(inpath + directory + '/sub-articles'):
            for file in os.listdir(inpath + directory + '/sub-articles'):
                if file.split('.')[-1] != 'json':
                    shutil.copy(inpath + directory + '/sub-articles/' + file, outpath)


def json_explorer(inpath):
    journal_metadata = []
    file_metadata = []
    for directory in os.listdir(inpath):
        print(file_metadata)
        if os.path.isfile(inpath + directory + '/metadata.json'):
            metadata_keys = json.load(open(inpath + directory + '/metadata.json')).keys()
            for key in metadata_keys:
                if key not in journal_metadata:
                    journal_metadata.append(key)

            if os.path.isdir(inpath + directory + '/sub-articles'):
                for file_path in os.listdir(inpath + directory + '/sub-articles'):
                    if file_path.split('.')[-1] == 'json':
                        with open(inpath + directory + '/sub-articles/' + file_path) as file:
                            metadata_keys = json.load(file).keys()
                            for key in metadata_keys:
                                if key not in file_metadata:
                                    file_metadata.append(key)
    print(journal_metadata)
    print(file_metadata)


if __name__ == "__main__":
    json_explorer('./mdpi_review/reviewed_articles/')

    # get_dict('./reviewed_articles/', './test_set/elife')
    # get_dict('./mdpi_review/reviewed_articles/', './test_set/')

    # get_dict('./plos_review/reviewed_articles/', './test_set/')
