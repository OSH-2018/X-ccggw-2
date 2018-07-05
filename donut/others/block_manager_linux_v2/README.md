### *Brief Intorduction of Working Process*

#### *1.Overview* 
##### Ⅰ. Input:
- package name(eg. gcc-8-base)
- erasur code block index
##### Ⅱ. Production:
- a zip file of needed erasur code block and meta_hash information
![](/pic/zip.png)
![](/pic/sent.png)

#### *2.Details*
**Ⅰ. Get users requests and collector relative file from local**
1. get the package's name ➠ <font color=green> *step 2*</font>
2. check out existence of this package, if not ➠ <font color=red> *step 1*</font>, else ➠ <font color=green> *step 3*</font>
3. get the construction of package file ➠ <font color=green> *step 4*</font>
4. collect [original files](www.google.com) of this package locally ➠ <font color=green> *step 5*</font>
5. get [md5](www.google.com) and [control](www.google.com) file locally ➠ <font color=green> *step 6*</font>
6. put original files, md5 and control into a defaul folder name after *donut* ➠ <font color=green> *step 7*</font>
7. set the least modified time to a default time in *donut* and zip them ✓ <font color=green>*finish!*</font>

**Ⅱ. Decode this zipped package and pack needed block and some information data**
1. encode the zipped file ➠ <font color=green> *step 2*</font>
2. get which erasure block the users want to get  ➠ <font color=green> *step 3*</font>
3. calculate the need bock's path ➠ <font color=green> *step 4*</font>
4. calculate hash of zipped fiel and needed block ➠ <font color=green> *step 5*</font>
5. save **hash** and encode meat information into a txt file ➠ <font color=green> *step 6*</font>
6. zip the txt file and needed bloc ✓ <font color=green>*finish!*</font>

**Ⅲ. Encode**
1. just encode 😂



