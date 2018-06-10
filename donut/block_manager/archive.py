import os
import posix
import shutil
import json


class Archive(object):
    """set the files' modified time stamp to a uniform time stamp

    :param path: the direct file's path
    :param pack_type: zip, tar, bz2...
    """
    def __init__(self, path, pack_type):
        self.path = path
        (self.top_path, self.name) = os.path.split(path)
        self.pack_type = pack_type
        self.time_path = self.top_path + "/TIME_Record_{}.json".format(self.name)
        # self.m_time_stamp = time.mktime(time.strptime(modified_time, "%a %b %d %H:%M:%S %Y"))
        # self.a_time_stamp = self.m_time_stamp

    def read_cm_time(self):
        with open(self.time_path, 'r') as f:
            data = json.load(f)
            return data

    def set_default_time(self):
        # TODO: get the way to modify file's created time
        """set the file's access time and modified time to his default time"""
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

    def pack_it(self):
        # TODO: better to fix it
        """the archive file is saved into the work_place, but this avoids naming conflict on the other hand"""
        shutil.make_archive("{}/{}_archive".format(os.getcwd(), self.name), "zip", r"{}".format(self.path))

    def unpack_it(self):
        # TODO: a part of installing, or rename the recovered archive file
        shutil.unpack_archive(r"{}/{}_archive.{}".format(self.top_path, self.name, self.pack_type))


