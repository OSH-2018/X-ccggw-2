import archive
import block
import track


path = "/Users/chailei/Desktop/Workplace/test"


def init():
    """when the user first start the """
    t = track.Track(path)
    t.clean()
    t.copy()
    t.track_diff()
    t.recode_cm_time()
    t.read_cm_time()
    # then install


def recover():
    t = track.Track(path)
    t.patch()


def pack():
    a = archive.Archive(path, "zip")
    a.set_default_time()
    a.pack_it()


def send(index):
    b = block.Block(path, "test_archive.zip")
    b.clean()
    b.erasure_encode()
    print(b.get_block_path(index=index))
    b.processbar()
    b.erasure_decode()


# init()
# recover()
# pack()
send(6)
