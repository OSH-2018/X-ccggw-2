import shutil
import os
import json
import pprint


class Track(object):
    """Track the differences caused by package install,
    save the difference information into a hidden folder
    and patch the file depend on the information

    :param path: path of the package

    A example:
        t = Track("/Users/chailei/Desktop/Donut/Erasure_code/fire_ice")
        t.copy()
        t.track_diff()
        t.install()
        t.pitch()
        t.recode_cm_time()
        t.read_cm_time()
    """
    def __init__(self, path):
        self.path = path
        (self.top_path, self.name) = os.path.split(path)
        self.work_path = self.top_path + "/{}_donut".format(self.name)
        self.diff_path = self.top_path + "/.DIFF_Track_{}".format(self.name)  # the hidden folder
        self.time_path = self.top_path + "/TIME_Record_{}.json".format(self.name)
        self.list = ""

    def clean(self):
        """handle the conflict in default file name"""
        if os.path.exists(self.diff_path):
            respond = input("the folder(to save diff) needed already exists, "
                            "do you want to overwrite it?(y/n)\n>>>")
            while True:
                if respond.lower() == 'y':
                    shutil.rmtree(self.diff_path)
                    break
                elif respond.lower() == 'n':
                    name = input("illegal name, input a new name\n>>>")
                    if len(name) == 0 or self.check_name(name, '.'):
                        continue
                    elif os.path.exists("{}/.{}".format(self.path, name)):
                        name = input("the new file you want named already exists, "
                                     "do you want to overwrite it?(y/n)\n>>>")
                    else:
                        self.diff_path = "{}/.{}".format(self.path, name)
                        break

        if os.path.exists(self.work_path):
            respond = input("the folder(origin file copy) needed already exists, "
                            "do you want to overwrite it?(y/n)\n>>>")
            while True:
                if respond.lower() == 'y':
                    shutil.rmtree(self.work_path)
                    break
                elif respond.lower() == 'n':
                    name = input("input a new name\n>>>")
                    if len(name) == 0 or self.check_name(name):
                        continue
                    elif os.path.exists("{}/{}".format(self.path, name)):
                        name = input("the new file you want named already exists, "
                                     "do you want to overwrite it?(y/n)\n>>>")
                    else:
                        self.work_path = "{}/{}".format(self.path, name)
                        break

        if os.path.exists(self.time_path):
            respond = input("the file(to save least modified time) needed already exists, "
                            "do you want to overwrite it?(y/n)\n>>>")
            while True:
                if respond.lower() == 'y':
                    os.remove(self.time_path)
                    break
                elif respond.lower() == 'n':
                    name = input("input a new name\n>>>")
                    if len(name) == 0 or self.check_name(name):
                        continue
                    elif os.path.exists("{}/{}".format(self.path, name)):
                        name = input("the new file you want named already exists, "
                                     "do you want to overwrite it?(y/n)\n>>>")
                    else:
                        self.time_path = "{}/{}".format(self.path, name)
                        break

    @staticmethod
    def check_name(name, not_in=None):
        """check name for illegal use"""
        pool = "0123456789abcdefghijklmnopqrstuvwxyz_.-"
        if (not_in is not None) and (not_in in name):
            return False
        else:
            for one_word in name:
                if one_word not in pool:
                    return False
        return True

    def copy(self):
        shutil.copytree(self.path, self.work_path)
        shutil.copytree(self.path, self.diff_path)

    def track_diff(self):
        for installed, origin, diff in list(zip(os.walk(self.path), os.walk(self.work_path), os.walk(self.diff_path))):
            for file in installed[2]:
                command = "diff -u '{}/{}' '{}/{}' > '{}/{}'".format(origin[0], file, installed[0],
                                                               file, diff[0], file)
                os.system(command)
        shutil.rmtree(self.work_path)

    def patch(self):
        shutil.copytree(self.path, self.work_path)

        for installed, diff in list(zip(os.walk(self.work_path), os.walk(self.diff_path))):
            for file in installed[2]:
                command = "patch -R '{}/{}' < '{}/{}'".format(installed[0], file, diff[0],file)
                os.system(command)

    def recode_cm_time(self):
        """created time and least modified time"""
        top_dic = {}
        for current_path, sub_folders, file_list in os.walk(self.path):
            file_dic = {}
            for file in file_list:
                full_path = "{}/{}".format(current_path, file)
                file_dic[file] = (os.path.getctime(full_path), os.path.getmtime(full_path))
            for folder in sub_folders:
                full_path = "{}/{}".format(current_path, folder)
                file_dic[folder] = (os.path.getctime(full_path), os.path.getmtime(full_path))
            top_dic[current_path] = file_dic
        top_dic['top'] = (os.path.getctime(self.path), os.path.getmtime(self.path))
        with open(self.time_path, 'w') as f:
            json.dump(top_dic, f)

    def read_cm_time(self):
        with open(self.time_path, 'r') as f:
            data = json.load(f)
            pprint.pprint(data)

    @staticmethod
    def install():
        print("Hello world")