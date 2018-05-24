import recover


class Collector(object):
    """ collect the block """

    def __init__(self, package, version, inf_file):
        self.package = package  # name
        self.version = version
        self.inf_file = inf_file
        self.blocks_demand = 0

    def count(self, ):
        # get the fastest N blocks
        pass

    def checkout(self, block_inf):
        # decide to recive one block
        pass

    def combine(self):
        # N --> 1
        pass
