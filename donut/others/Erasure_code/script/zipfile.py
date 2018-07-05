import os


class Zip(object):
    def __init__(self, file_list, file_name, direct_path, modify_name):
        self.file_list = file_list
        self.file_name = file_name
        self.direct_path = direct_path
        self.modify_name = modify_name
        self.location = []

    def check(self):
        """check out if the file exit"""
        for c_file in self.file_list:
            if not os.path.exists(c_file):
                print("file {} doesn't exit".format(c_file))
                exit(1)

    def zip(self):
        """just zip file"""
        now_path = os.getcwd()
        os.chdir(self.direct_path)  # go into the path that store the file
        self.check()  # check out exit
        command = "zip -X {}.zip".format(self.file_name)
        for zip_file in self.file_list:
            command += " {}".format(zip_file)
        os.system(command)
        os.chdir(now_path)

    def modify_time(self):
        """the only one difference is caused by time, modify them to 00
        see the file ZipSurveyReport.pdf about the details"""
        os.chdir(self.direct_path)
        print(os.getcwd())  # debug
        binary_read_file = open("{}.zip".format(self.file_name), "rb")
        binary_data = binary_read_file.read()
        binary_read_file.close()
        binary_write_file = open("{}.zip".format(self.modify_name), "wb")
        self.find_position(binary_data)
        binary_new_data = binary_data[:self.location[0]] + b'\0' + b'\0' + b'\0' + b'\0'
        for index, _ in enumerate(self.location):
            if index == 0:
                continue
            binary_new_data += binary_data[self.location[index - 1] + 4:self.location[index]] + b'\0' + b'\0' + b'\0' + b'\0'
        binary_new_data += binary_data[self.location[-1] + 4:]
        binary_write_file.write(binary_new_data)
        binary_write_file.close()

    def find_position(self, binary_data):
        """1400 0000 0800"""
        length = len(binary_data)
        for i in range(length):
            if binary_data[i] == 20 and binary_data[i + 1] == 0:
                if binary_data[i + 2] == 0 and binary_data[i + 3] == 0:
                    if binary_data[i + 4] == 8 and binary_data[i + 5] == 0:
                        self.location.append(i + 6)


def test():
    file = ["meltdown.pdf", "spectre.pdf"]
    a = Zip(file, "self_test", "/Users/chailei/Desktop/OSH", "modified")
    a.zip()
    a.modify_time()
