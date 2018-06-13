# 安装包格式
- 安装包有3个部分组成：数据包，包含实际安装的程序数据；
    - 在这个实例中data和installer都是数据包。其下一级目录中的usr是在重构软件包时的必要组成。
    - 从usr这一级开始目录名称不可以更改。
- 安装信息及控制脚本包，包含 deb 的安装说明，标识，脚本等；
    - 在这个实例中就是package目录下的DEBIAN目录
    - 从DEBIAN这一级开始也不可以更改目录名称
    - md5sums可以实时计算
    - control可以如下从系统文件恢复:

```python
import re
def extract_control(_name: str, _version=None):
    result = []
    with open('/var/lib/dpkg/status', 'r') as f:
        items = f.read()
    mode = re.compile('\n\n(.+?)\n\n', re.S)
    mode_e = re.compile('.*\n\n(.+?)\n$', re.S)
    packages = mode.findall(items)
    packages.extend(mode_e.findall(items))
    mode_name = re.compile('Package: (.+?)\n')
    mode_ver = re.compile('Version: (.+?)\n')
    for package in packages:
        name = mode_name.search(package).group(1)
        version = mode_ver.search(package).group(1)
        if name == _name:
            result.append([package, version, package])
    if len(result) > 1:
        result = [item for item in result if item[1] == version]
    if len(result) == 1:
        return result[0][2]
    elif len(result) == 0:
        return None


print(extract_control('gedit'))
```

- 最后一个是 deb 文件的一些二进制数据，包括文件头等信息，一般看不到，在某些软件中打开可以看到。
    - 重构时并不需要特殊操作
# 重构过程
1. 获得数据包usr(使用如下命令   {}为包名，如gcc：要具体到版本gcc-8-base)
    ```bash
    dpkg-query -L {}
    ```
2. 当场计算恢复出DEBIAN目录下的文件
    - 这里的md5sums有两种获得方式，一个可以用python现算，也可以用dpkg-query -c {}来调出来
    - 后者可靠性没有过多测试，但是试了几个都可以用
    - control除了用上述函数，也可用这条命令来获得apt-cache show {}
3. 将usr和DEBIAN放到同一个目录下，该目录名称可以自定义
4. 采用如下语句来生成deb安装包({}中为自定义的目录名，build为生成的deb包的名字)
```bash
dpkg-deb -b {} build
```