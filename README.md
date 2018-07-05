# *Donut*

分布式的包分发加速工具

## *Introduce*

本项目基于linux包管理工具链dpkg和apt，在此之上建构了一个P2P的分布式网络，以获得更高速的下载和高度的可用性。每一个用户，都作为节点共享本机已经安装好的软件包，并也可以从其他用户处获得新软件包的下载和更新。

## *Members*

#### *Storage*

- 柴磊[@Charley](https://github.com/charleyustccs)
- 顾健鑫

#### *Architecture*

- 归舒睿[@Citrine](https://github.com/CM-BF)
- 吴豫章
- 陈俊羽[@starmode](https://github.com/starmode)

## *Research Report*

- [PDF](docs/ResearchReport/分布式包分发系统调研报告.pdf)
- [Word](docs/ResearchReport/分布式包分发系统调研报告.docx)

## *Feasibility Report*

- [PDF](docs/FeasibilityReport/可行性分析.pdf)
- [Word](docs/FeasibilityReport/可行性分析.docx)

## *Mid-term Report*

- [Keynote](docs/Mid-termReport/donut.key)
- [HTML](docs/Mid-termReport/donut)

## *Final Report*

- [Keynote](docs/FinalReport/Donut.key)[注：由于没有备份，keynote不完成，见谅]
- [Word](docs/FinalReport/结题报告.docx)

## *Progress*

- [x] Erasure code
- [x] Track changes
- [x] Regress packages
- [x] rebuild deb packages
- [x] P2P connection
- [x] Send/Recive packages
- [X] Index local software
- [X] rebuild uniform packages from different machines on different times
- [X] ID block's building and updating ...
- [X] IP <=> ID
- [X] DNS Server
- [X] Blocks sync
