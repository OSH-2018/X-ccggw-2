import shutil
import os
import time


class Recover(object):
    """a class tracks the change of file and is capable of recovering it"""

    def __init__(self, path, ec_path):
        self.path = path
        self.recover_path = self.origin_path = ec_path + "/erasurecoding"
        self.diff_path = path + "/.DIFF_Track"
        self.list = ""
        self.clean()

    def clean(self):
        if os.path.exists(self.diff_path):
            shutil.rmtree(self.diff_path)

        if os.path.exists(self.origin_path):
            shutil.rmtree(self.origin_path)

        if os.path.exists(self.recover_path):
            shutil.rmtree(self.recover_path)

    def copy(self):
        # copies of the original file
        self.list = os.listdir(self.path)
        if ".DS_Store" in self.list:
            self.list.remove('.DS_Store')
        shutil.copytree(self.path, self.origin_path)

    def track_diff(self):
        os.system("mkdir " + self.diff_path)  # directory stores diff file
        for file in self.list:
            file = "/" + file
            command = "diff -u {} {} > {}".format( self.origin_path + file, self.path + file, self.diff_path + file)
            result = os.system(command)
        shutil.rmtree(self.origin_path)

    def pitch(self):
        # recover file
        os.mkdir(self.recover_path)

        for file in self.list:  # origin file's list
            file = "/" + file
            is_changed = len(open(self.diff_path + file).read())
            shutil.copyfile(self.path + file, self.recover_path + file)
            if is_changed == 0:
                continue
            command = "patch -R {} < {}".format(self.recover_path + file, self.diff_path + file)
            os.system(command)

    def install(self):
        self.copy()
        for file in self.list:  # origin file's list
            file = "/" + file
            with open(self.path + file, 'a') as f:
                f.write('\n' + time.ctime())


class ErasureCode(object):
    """ zip the file and make erasure code """
    def __init__(self, name):
        self.zip = ".bz2"
        self.name = name
        self.tarname = ""

    def zip_dir(self):
        command = ""
        if self.zip == "tar":
            command = "tar cvf {}.tar {}".format(self.name, self.name)
            self.tarname = self.name + ".tar"
        elif self.zip == ".tgz":
            command = "tar zcvf {}.tar.gz {}".format(self.name, self.name)
            self.tarname = self.name + ".tar.gz"
        elif self.zip == ".bz2":
            command = "tar jcvf {}.tar.bz2 {}".format(self.name, self.name)
            self.tarname = self.name + ".tar.bz2"
        os.system(command)
        shutil.rmtree("erasurecoding")

    def erasure_encoding(self):
        command = "./encoder '{}' 4 2 'reed_sol_van' 8 8 1024".format(self.tarname)
        os.system(command)

    def erasure_decoding(self):
        if os.path.exists(self.tarname):
            os.system("rm " + self.tarname)
        command = "./decoder '{}'".format(self.tarname)
        os.system(command)
        # shutil.rmtree("erasure_code")
