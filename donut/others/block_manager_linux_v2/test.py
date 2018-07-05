import archive
import block
import collector
import os


def collect(pkg_name):
    """collect the needed package file from system
    create a zip file of these files

    :param pkg_name: the name of needed package
    """
    collect_deb = collector.Collector(pkg_name)
    collect_deb.extract_installed_package()
    collect_deb.package_exist()
    collect_deb.collector_file()  # /usr/...

    # /DEBIAN/...
    control_info = collect_deb.get_control()
    if control_info is not None:
        os.mkdir("donut/DEBIAN")
        with open("donut/DEBIAN/control", 'w') as file:
            file.write(control_info)
        collect_deb.fix_control("donut/DEBIAN/control")
    collect_deb.extract_md5()

    time_setter = archive.Archive("{}/donut".format(os.getcwd()), pkg_name, "zip", "1 Jan 18")
    time_setter.set_default_time()  # time-sync
    time_setter.pack_it()  # zip them, this file is asserted to be same in any machine
    collect_deb.clean()


def erasure_encoder(pkg_name, block_index):
    """cut the zip file and return the needed block's address
    """
    block_manager = block.Block(os.getcwd() + "/{}_donut.zip".format(pkg_name))
    block_manager.clean()
    block_manager.erasure_encode()
    print(block_manager.get_block_path(index=block_index))


def erasure_decoder(pkg_name):
    """when there is enough block for decoding
    """
    block_manager = block.Block("{}/{}_donut.zip".format(os.getcwd(), pkg_name))
    block_manager.erasure_decode()
    print("donut--> decode done!!!")


def build_deb(pkg_name):
    """unzip the packed file and build deb package
    """
    zip_mag = archive.Archive("{}/donut".format(os.getcwd()), pkg_name, "zip", "1 Jan 18")
    zip_mag.un_zip("{}/Coding/gcc-8-base_donut_decoded.zip".format(os.getcwd()),
                   "{}/donut".format(os.getcwd()))
    collect_deb = collector.Collector(pkg_name)
    collect_deb.build("{}/donut".format(os.getcwd()), "{}/{}_donut.deb".format(os.getcwd(), pkg_name))


def main1():
    temp = input("the package and index\n>>>")
    pkg_name, index = temp.split()
    collect(pkg_name)
    erasure_encoder(pkg_name, int(index))


def main2():
    temp = input("the package and index\n>>>")
    pkg_name, index = temp.split()
    erasure_decoder(pkg_name)


def main3():
    temp = input("the package and index\n>>>")
    pkg_name, index = temp.split()
    build_deb(pkg_name)


if __name__ == "__main__":
    main1()

