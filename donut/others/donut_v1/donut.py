# 对外命令行接口
from argparse import ArgumentParser

from Operations.Operation import init_network, download

if __name__ == '__main__':
    parser = ArgumentParser(' An P2P project based on dpkg and apt to accelerate your download.')
    parser.add_argument("mode", type=str, choices=['init', 'install', 'id'])
    parser.add_argument("-n", "--package", type=str, help="downloaded package name")
    parser.add_argument("-v", "--version", type=str, help="downloaded package version")

    args = parser.parse_known_args()[0]

    if args.mode == 'init':
        print('Init Donut...')
        init_network()

    elif args.mode == 'install':
        name = args.name
        version = args.version
        if name is None:
            print('Should has a valid package name!')
            exit(-1)
