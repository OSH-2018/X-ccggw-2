import os
import time
import shutil
import process


class Block(object):
    """Receive the needed block and send  out it

    :param package_path: top/{}_donut.zip
    """

    def __init__(self, package_path):
        self.pkg_path = package_path
        (self.top_path, self.pkg_full_name) = os.path.split(package_path)
        self.pkg_name = self.pkg_full_name.split('.')[0]
        # self.time = "2018-06-10"
        # self.block_path = "{}/.{}_donut_{}".format(self.top_path, self.name, self.time)
        self.block_folder = "{}/Coding".format(self.top_path)  # TODO: improve later

    # TODO: improve later
    def clean(self):
        """handle the conflict in default file name"""
        if os.path.exists(self.block_folder):
            respond = input("the folder(to save erasure blocks) needed already exists, "
                            "do you want to overwrite it?(y/n)\n>>>")
            while True:
                if respond.lower() == 'y':
                    shutil.rmtree(self.block_folder)
                    break
                elif respond.lower() == 'n':
                    name = input("illegal name, input a new name\n>>>")
                    if len(name) == 0 or self.check_name(name, '.'):
                        continue
                    elif os.path.exists("{}/{}".format(self.top_path, name)):
                        name = input("the new file you want named already exists, "
                                     "do you want to overwrite it?(y/n)\n>>>")
                    else:
                        self.block_folder = "{}/{}".format(self.top_path, name)
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

    def get_block_path(self, index):
        """the name like '/Users/chailei/Desktop/Donut/.fire_ice_donut_2018-06-10
        /fire_ice_archive_m2.zip'"""
        return "{}/{}".format(self.block_folder, self.calc_name(index))

    # delete
    def get_archive_time(self):
        """for the sake of avoiding conflict of naming, give the ec_code folder name after
        the archive file's least modified time"""
        time_modify_archive = time.gmtime(os.path.getmtime(self.pkg_path))
        return time.strftime("%Y-%m-%d", time_modify_archive)

    def calc_name(self, block_index):
        """return the name of block that needed to be sent"""
        # print(self.meta_file)
        meta_file_path = "{}/{}_{}".format(self.block_folder, self.pkg_name, "meta.txt")
        with open(meta_file_path) as meta:
            meta = meta.readlines()
            # print(meta)
            km_value = (meta[2]).split()
            extend_name = (meta[0]).strip().split(".")
            (_, block_name) = os.path.split(extend_name[0])
            # print(extend_name)
            if block_index <= int(km_value[0]):  # default 3 key
                return "{}_k{}.{}".format(block_name, block_index, extend_name[1])
            elif block_index <= int(km_value[0]) + int(km_value[1]):
                return "{}_m{}.{}".format(block_name, block_index - int(km_value[0]), extend_name[1])

    def erasure_encode(self):
        # TODO: upgrade the encoder.c for a more efficient and faster erasure coding process
        """because of the encoder's limited ability, copy the archive to the work_place, sent back the
        erasure codes after calculating"""
        command = "./encoder '{}' 4 2 'reed_sol_van' 8 8 1024".format(self.pkg_full_name)
        print(command)
        os.system(command)
        os.remove(self.pkg_path)
        # shutil.copytree("{}/Coding".format(os.getcwd()), self.block_path)
        # os.remove(self.package_name)
        # shutil.rmtree("{}/Coding".format(os.getcwd()))
        print("save the erasure code into ", self.block_folder)

    def processbar(self):
        P = process.ProcessBar()
        P.show()

    def erasure_decode(self):
        # TODO: upgrade the code for many error management
        command = "./decoder '{}'".format(self.pkg_full_name)
        os.system(command)
