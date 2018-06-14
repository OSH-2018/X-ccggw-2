# 对外命令行接口
from argparse import ArgumentParser


if __name__ == '__main__':
    parser = ArgumentParser(' An P2P project based on dpkg and apt to accelerate your download.')
    parser.add_argument("mode", type=str, choices=['init', 'install', 'id'])
    parser.add_argument("-n", "--package", type=str, help="download package name")
    parser.add_argument("-v", "--version", type=str, help="package version")

    args = parser.parse_known_args()
