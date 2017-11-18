
import sys, os, pystache, re, pwd, pprint, shutil,codecs,subprocess
import __main__

class file_template:

	filename = False
	config = False

	def __init__(self, filename, config={}, target_dir=False ):
		self.filename = filename
		self.config = config
		self.target_dir = target_dir
		self.source_dir = os.path.dirname( os.path.realpath(__main__.__file__) ) + '/templates/v2'

	def set_config( self, key, value ):
		self.config[key] = value

	def process( self, override = True ):
		template = self.read()
		content = pystache.render( template, self.config )
		filename = pystache.render( self.filename, self.config )
		file_path = self.target_dir + '/' + filename

		if override or not os.path.exists(file_path):
			print('Write file: %s' % (filename))
			self.write(content,file_path)
		else:
			print('File exists: %s' % (filename))
			pass

	def read(self):
		file_path = self.source_dir + '/' + self.filename
		if not os.path.exists(file_path):
			return ''

		f = codecs.open(file_path,'rb',encoding='utf-8')
		contents = f.read()
		f.close()

		return contents

	def write(self, content, file_path ):
#		print "Write File", file_path
		fdir = os.path.dirname(file_path)
		if not os.path.exists(fdir):
			os.makedirs(fdir)
		f = codecs.open(file_path,'wb',encoding='utf-8')
		f.write(content)
		f.close()
