
import sys, os, pystache, re, pwd, pprint, shutil,codecs,subprocess
import __main__

class file_template:

	#source_filename = False
	#target_filename = False
	#source_dir = False
	#target_dir = False

	config = {}

	def __init__(self, template_name, config={}, target_dir=False ):
		self.config = config
		self.source_filename = template_name
		self.target_filename = pystache.render( self.source_filename + '', self.config )
		self.target_dir = target_dir
		self.source_dir = os.path.dirname( os.path.realpath(__main__.__file__) ) + '/templates/v2'


	def process( self, override = True ):

		template = self.read()
		content = pystache.render( template, self.config )
		file_path = self.target_dir + '/' + self.target_filename

		if override or not os.path.exists(file_path):
			print('Write file: %s' % (self.target_filename))
			self.write( content )
		else:
			print('File exists: %s' % (self.target_filename))
			pass

	def read(self):
		file_path = self.source_dir + '/' + self.source_filename

		f = codecs.open(file_path,'rb',encoding='utf-8')
		contents = f.read()
		f.close()

		return contents

	def write( self, content ):
		file_path = self.target_dir + '/' + self.target_filename

		fdir = os.path.dirname(file_path)
		if not os.path.exists(fdir):
			os.makedirs(fdir)
		f = codecs.open(file_path,'wb',encoding='utf-8')
		f.write(content)
		f.close()
