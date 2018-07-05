import os
import shutil
import hashlib


class Sender(object):
    """send out blocks"""

    def __init__(self, package, blocks_index, path, ip):
        self.package = package  # name
        self.file_locate = path + "/erasure_code/"
        self.blocks_index = blocks_index
        self.meta_file = "{}/{}_meta.txt".format(self.file_locate, package)
        self.sent_name = self.which_block()
        self.ip = ip

    def which_block(self):
        # return the name of block that needed to be sent
        print(self.meta_file)
        with open(self.meta_file) as meta:
            meta = meta.readlines()
            print(meta)
            km_value = (meta[2]).split()
            extend_name = (meta[0]).strip().split(".")
            print(extend_name)
            if self.blocks_index <= int(km_value[0]): # default 3 key
                return "{}_k{}.{}.{}".format(extend_name[0], self.blocks_index,
                                             extend_name[1], extend_name[2])
            elif self.blocks_index <= int(km_value[0]) + int(km_value[1]):
                return "{}_m{}.{}.{}".format(extend_name[0], self.blocks_index - int(km_value[0]),
                                             extend_name[1], extend_name[2])

    def generate_hash(self):
        hash_new = hashlib.sha1() # which one
        with open(self.file_locate + self.sent_name, 'rb') as file:
            all = ""
            while True:
                data = file.read()  # read the all the data
                if file.read() == b'':
                    break
                all += data
        hash_new.update(data)  # generate hash value
        hash_value = hash_new.hexdigest()
        print(hash_value)

    def send(self):
        # send to ip address
        name = self.file_locate + self.sent_name
        shutil.copyfile(name, "sent_to_{}".format(self.ip))

    def verify_msg(self):
        # paste block's verify message
        # index, slice_hash, slice_id, block_id, package_hash
        pass


os.chdir("..")
S = Sender("erasurecoding", 6, os.getcwd(), "8888.8888.8888")
S.send()
S.generate_hash()