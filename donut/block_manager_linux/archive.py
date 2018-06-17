import os
import posix
import shutil
import json
import time
import zipfile


class Archive(object):
    """set the files' modified time stamp to a uniform time stamp
    zip the folder into {gcc-8-base}_donut.zip
    unzip {gcc-8-base}_donut.zip to {} folder

    :param path: top/donut
    :param pkg_name: gcc-8-base
    :param pack_type: zip
    :param modified_time: "1 Jan 18"
    """
    def __init__(self, path, pkg_name, pack_type, modified_time):
        self.path = path
        self.pkg_name = pkg_name
        (self.top_path, self.name) = os.path.split(path)
        self.pack_type = pack_type
        self.m_time_stamp = time.mktime(time.strptime(modified_time, "%d %b %y"))
        self.a_time_stamp = self.m_time_stamp

        # TODO: discuss
        self.time_path = self.top_path + "/TIME_Record_{}.json".format(self.name)

    # TODO: discuss
    def read_cm_time(self):
        """Abandon!!!"""
        with open(self.time_path, 'r') as f:
            data = json.load(f)
            return data

    # TODO: discuss
    def set_original_time(self):
        # TODO: get the way to modify file's created time
        """set the file's access time and modified time to his original time"""
        data = self.read_cm_time()
        for current_path, sub_folders, file_names in os.walk(self.path):
            time_dic = data[current_path]
            for folder in sub_folders:
                time_temp = time_dic[folder]
                posix.utime("{}/{}".format(current_path, folder), (time_temp[0], time_temp[1]))
            for file in file_names:
                time_temp = time_dic[file]
                posix.utime("{}/{}".format(current_path, file), (time_temp[0], time_temp[1]))
        posix.utime(self.path, (data['top'][0], data['top'][1]))

    def set_default_time(self):
        # TODO: get the way to modify file's created time
        """set the file's access time and modified time to his default time"""
        for current_path, sub_folders, file_names in os.walk(self.path):
            for folder in sub_folders:
                posix.utime("{}/{}".format(current_path, folder), (self.a_time_stamp, self.m_time_stamp))
            for file in file_names:
                posix.utime("{}/{}".format(current_path, file), (self.a_time_stamp, self.m_time_stamp))
        posix.utime(self.path, (self.a_time_stamp, self.m_time_stamp))

    def pack_it(self):
        """the archive file is saved into the work_place, but this avoids naming conflict on the other hand"""
        shutil.make_archive("{}/{}_donut".format(os.getcwd(), self.pkg_name), "zip", r"{}".format(self.path))

    @staticmethod
    def un_zip(file_name, dst):
        """unzip zip file"""
        zip_file = zipfile.ZipFile(file_name)
        if os.path.isdir(dst):
            pass
        else:
            os.mkdir(dst)
        for names in zip_file.namelist():
            zip_file.extract(names, dst+'/')
        zip_file.close()

    def unpack_it(self):
        # TODO: rename the recovered archive file
        shutil.unpack_archive(r"{}/Coding/{}_donut_decoded.{}".format(os.getcwd(), self.pkg_name, self.pack_type))