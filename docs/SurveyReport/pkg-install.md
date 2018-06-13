### *the node for installing packages in Linux*
#### *tar or tgz:*
*steps:*
1. get package
2. uncompress
```
tar: tar -xvf {}.tar
tagz: tar -zxvf {}.tgz
```
3. read INSTALL, README file
4. prepare for build
```
./configure
```
5. build
```
make
```
6. install
```
make install
```
7. finish and clean
```
make clean
```
*setting*
@ /usr/local/bin
*file*
#### *deb*
*step:*
1. sudo dpkg -i {}.deb
2. sudo apt-get install {}
3. sudo apt-get -f install
*command:*
1. dpkg -c {}.deb // the file included before innstalling
2. dpkg -L {} // after installing
3. dpkg -r {} // remove
4. dpkg -S filepath
