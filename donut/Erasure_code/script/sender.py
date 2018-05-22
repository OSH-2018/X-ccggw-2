import recover


class Sender(object):
	"""send out blocks"""
	def __init__(self, package, blocks, zip_way, ip):
		self.package = package
		self.blocks_index = blocks_index
		self.zip_way = zip_way
		self.ip = ip

	def split(self):
		# erasure code get the need block
		pass

	def send(self):
		# send to ip address
		pass

	def verify_msg(self):
		# paste block's verify message 
		# index, slice_hash, slice_id, block_id, package_hash
		pass

