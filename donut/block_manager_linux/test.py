import archive
import block
import track
import collector
import os


path = "/Users/chailei/Desktop/Workplace/test"


def init():
    """when the user first start the """
    t = track.Track(path)
    t.clean()
    t.copy()
    t.track_diff()
    t.recode_cm_time()
    t.read_cm_time()
    # then install

def recover():
    t = track.Track(path)
    t.patch()

def send(index):
    b = block.Block(path, "test_archive.zip")
    b.clean()
    b.erasure_encode()
    print(b.get_block_path(index=index))
    b.processbar()
    b.erasure_decode()

def collect():
    pkg_name = input("package name: \n>>>")
    collect_deb = collector.Collector(pkg_name)
    collect_deb.extract_installed_package()
    collect_deb.package_exist()
    collect_deb.collector_file()
    control_info = collect_deb.get_control()
    if control_info is not None:
        os.mkdir("test/DEBIAN")
        with open("test/DEBIAN/control", 'w') as file:
            file.write(control_info)
        collect_deb.fix_control("test/DEBIAN/control")
    collect_deb.extract_md5()
    # collect_deb.build()
    time_setter = archive.Archive("{}/test".format(os.getcwd()),
                                  pkg_name, "zip", "1 Jan 18")
    time_setter.set_default_time()
    time_setter.pack_it()
    collect_deb.clean()
    block_manager = block.Block(os.getcwd()+"/gcc-8-base_archive.zip", "{}_archive.zip".format(pkg_name))
    block_manager.clean()
    block_manager.erasure_encode()
    print(block_manager.get_block_path(index=3))
    block_manager.processbar()
    # block_manager.erasure_decode()


# init()
# recover()
# pack()
# send(6)
collect()