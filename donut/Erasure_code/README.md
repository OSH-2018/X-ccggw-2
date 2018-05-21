### *Brief Introduction of ec-0.0.1*

##### *Doing What*

- track changs in a directory and recode them
- regress the changed directory
- simulate making changes(caused by installing) by adding Timestamps to the end of files
- zip files
- do erasure coding for this zip file: encode and decode

##### *How To Do*

1. copy the directory
2. change(install)
3. track the differences and delete the copy
4. recode them into the hidden driectory named ".DIFF_Track" located in this directory
5. regress the directory deponding on ".DIFF_Track"
6. zip/delete the regressed directory
7. do erasure coding

##### *New In Next Version*

- support more zip command
- fit parameters into real need
- ...
