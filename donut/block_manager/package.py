# 从dpkg索引中读取所有安装好的软件
def extract_installed_list():
    with open('/var/lib/dpkg/status', 'r') as f:
        lines = f.readlines()
    mode = re.compile('^Package: (.+)')
    names = [mode.match(line).group(1) for line in lines if mode.match(line)]
    print(len(names))
    mode = re.compile('^Version: (.+)')
    versions = [mode.match(line).group(1) for line in lines if mode.match(line)]
    print(len(versions))
    all = [name + '___' + version + '\n' for name, version in zip(names, versions)]
    # 从config读取meta文件位置
    config = configparser.ConfigParser()
    config.read(config_file_name)
    path = config['general']['path']
    with open(os.path.join(path, 'installed'), 'w') as f:
        f.writelines(all)