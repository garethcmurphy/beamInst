#!/usr/bin/env python3
"""get files info"""
import datetime
import glob
import hashlib
import os
import json

import pytz


class FilesInfo:
    """get files info"""

    def __init__(self):
        self.files = []
        self.file_number = 22
        self.experiment_date_time = "2017"
        self.total_file_size = 12345654
        self.source_folder = 'source_folder'
        self.base_name = 'base_name'
        self.file_names = []
        self.file_list = []

    @staticmethod
    def get_files(my_dir):
        """get files """
        files = glob.glob(my_dir + '/**/**.*', recursive=True)
        #files = os.listdir(my_dir)
        return files

    def extract_file_list(self, source_folder):
        """extract file list"""
        file_number = 0
        total_file_size = 0
        self.file_names = self.get_files(source_folder)
        # print(self.file_names[0])
        print('Fetching info on all files, n=', len(self.file_names))
        if not self.file_names:
            print("filename empty")
        for file in self.file_names:
            file_number += 1
            longname = file

            stat_info = os.stat(longname)
            rel_path = longname
            rel_path = longname.replace(
                '/Users/garethmurphy/Downloads/Mar25930/', '')
            rel_path = os.path.basename(longname)
            file_size = stat_info.st_size
            experiment_date_time = stat_info.st_ctime
            timestamp = int(experiment_date_time)

            permissions = oct(stat_info.st_mode & 0o777)

            experiment_date_time = str(
                datetime.datetime.fromtimestamp(timestamp, tz=pytz.UTC).isoformat())
            total_file_size += file_size
            checksum = "string"

            if file_size < 34000000:
                hash_object = hashlib.sha256(open(longname, 'rb').read())
                checksum = hash_object.hexdigest()

            file_entry = {
                "path": rel_path,
                "size": file_size,
                "time": experiment_date_time,
                "chk": checksum,
                "uid": stat_info.st_uid,
                "gid": stat_info.st_gid,
                "perm": permissions
            }
            if file_number < 1000:
                self.file_list.append(file_entry)
            self.experiment_date_time = experiment_date_time
            self.file_number = file_number
            self.total_file_size = total_file_size
            self.source_folder = source_folder
            if file_number > 250:
                break
        # print(self.file_number)


def main():
    file = FilesInfo()
    directory = "./demo"
    directory = "/users/detector/experiments/beamMonitors/CDT-IBM-V20-July2019"
    directory = "/Users/garethmurphy/Downloads/Mar25930"
    directory = "/nfs/groups/beamlines/ldpc/data"
    datasetId = "20.500.12269/4f8c991e-a879-4e00-9095-5bb13fb02ac4"

    file.get_files(directory)
    file.extract_file_list(directory)
    orig_dict = {
        "ownerGroup": "ess",
        "accessGroups": ["ess"],
        "size": file.total_file_size,
        "dataFileList": file.file_list,
        "datasetId": datasetId
    }
    print(json.dumps(orig_dict))


if __name__ == "__main__":
    main()