import os
import csv
import functools
import shutil
import re


class Collector(object):
    """a class make a deb package from local

    :param package_name: gcc-8-base
    """
    def __init__(self, package_name):
        self.package_name = package_name  # gcc-8-base
        self.top_path = os.getcwd()  # the temp file all exist in current path
        self.installed_file = "{}/installed.csv".format(self.top_path)  # stay in top_path
        self.location_file = "{}/location".format(self.top_path)  # temp file
        self.temp_package_folder = "{}/donut".format(self.top_path)

    def extract_installed_package(self):
        """get the list of package installed, and store the list into a json file
        this json file will store forever, and update after every package install or uninstall"""
        temp_installed_file = "{}/installed".format(self.top_path)
        command = "dpkg -l > {}".format(temp_installed_file)
        os.system(command)
        with open(temp_installed_file, 'r') as f:
            list = f.readlines()
            for index, content in enumerate(list):
                if "+++-===" in content:
                    csv_data = list[index + 1:]
                    self.save_installed(csv_data)
                    break

    def save_installed(self, csv_data):
        """save the install list

        :type csv_data: list
        """
        header = ["Name", "Version", "Architecture", "Description"]
        data_0 = [content.split()[1:] for content in csv_data]
        data_1 = [functools.reduce(lambda x, y: x + ' ' + y, content[3:]) for content in data_0]
        data_2 = [content[:3] for content in data_0]
        data = [x + [y] for x, y in list(zip(data_2, data_1))]
        with open(self.installed_file, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(header)
            csv_writer.writerows(data)

    def package_exist(self):
        with open(self.installed_file, 'r') as file:
            csv_reader = csv.DictReader(file.readlines())
            for package in csv_reader:
                if package['Name'] == self.package_name:
                    return True
            return False

    def collector_file(self):
        """get the information from system, and collect them"""
        command = "dpkg-query -L {} > {}".format(self.package_name, self.location_file)
        os.system(command)
        file_list = []
        folder_list = []
        with open(self.location_file, 'r') as file:
            path = file.readlines()
            for p in path[1:]:
                file_list.append(p.strip())
        length = len(file_list)
        for i in range(length):
            for p in file_list[1 + i:]:
                if file_list[i] in p and p.count('/') > file_list[i].count('/'):
                    folder_list.append(file_list[i])
                    file_list[i] = ''
                    break
        for i in range(len(folder_list)):
            file_list.remove('')
        self.copy_file(set(file_list), set(folder_list))

    def copy_file(self, file_list, folder_list):
        """mkdir and copy

        :param folder_list:
        :param file_list:
        :type file_list: set
        :type folder_list: set
        """
        folder_list = sorted(folder_list, key=lambda x: len(x))
        if os.path.exists(self.temp_package_folder):
            shutil.rmtree(self.temp_package_folder)
        # TODO: add error handle for asking new temp_package_folder name
        os.mkdir(self.temp_package_folder)
        for folder in folder_list:
            os.mkdir("{}{}".format(self.temp_package_folder,folder))
        for file in file_list:
            if os.path.isfile(file):
                shutil.copy(src=file, dst="{}{}".format(self.temp_package_folder, file))
            else:
                shutil.copytree(src=file, dst="{}{}".format(self.temp_package_folder, file))

    # TODO: fix the bug
    def extract_control(self, version=None):
        """get a package's control information"""
        info_path = "/var/lib/dpkg/status"
        result = []
        with open(info_path, "r", encoding='utf-8') as f:
            items = f.read()
        mode = re.compile("\n\n(.+?)\n\n", re.S)
        mode_e = re.compile(".*\n\n(.+?)\n$", re.S)
        packages = mode.findall(items)
        packages.extend(mode_e.findall(items))
        mode_name = re.compile("Package: (.+?)\n")
        mode_ver = re.compile("Version: (.+?)\n")
        for package in packages:
            name = mode_name.search(package).group(1)
            version = mode_ver.search(package).group(1)
            if name == self.package_name:
                result.append([package, version, package])
        if len(result) > 1:
            result = [item for item in result if item[1] == version]
        if len(result) == 1:
            return result[0][2]
        elif len(result) == 0:
            return None

    def get_control(self):
        command = 'apt-cache show {} > control_temp'.format(self.package_name)
        os.system(command)
        with open('control_temp', 'r') as f:
            control_info = f.read()
        return control_info

    def extract_md5(self):
        """get the md5 of usr/lib/share/doc/*"""
        command = "dpkg-query -c {} > where_md5".format(self.package_name)
        os.system(command)
        with open("where_md5", 'r') as md5:
            md5 = md5.read().strip()
            if os.path.exists(md5):
                command = "cat {} > {}".format(md5, "donut/DEBIAN/md5sums")
                os.system(command)
            else:
                print("Error")
        os.remove("where_md5")

    @staticmethod
    def build(temp_folder, deb_name):
        """build deb package

        :param temp_folder: top_path/donut
        :param deb_name: {package_name}_donut.deb
        """
        # TODO: add file existence check
        command = "dpkg-deb -b {} {}".format(temp_folder, deb_name)
        os.system(command)
        print("Donut--> build successful!")

    @staticmethod
    def fix_control(file_name):
        with open(file_name, 'r+') as file:
            data = file.readlines()
        with open(file_name, 'w') as file:
            for line in data:
                if 'Status: ' in line:
                    continue
                file.write(line)
            file.write("\n")

    def clean(self):
        os.remove("installed")  # install temp
        os.remove(self.location_file)
        os.remove("control_temp")
        if os.path.exists(self.temp_package_folder):
            shutil.rmtree(self.temp_package_folder)