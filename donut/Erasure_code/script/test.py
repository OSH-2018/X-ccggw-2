import os
import recover

def test():
    os.chdir("..")  # /Users/chailei/Desktop/Donut/tests
    print(os.getcwd())
    R = recover.Recover(os.getcwd() + "/test", os.getcwd())
    R.install()
    R.track_diff()
    R.pitch()
    E = recover.ErasureCode("erasurecoding")
    E.zip_dir()
    E.erasure_encoding()
    E.erasure_decoding()

test()