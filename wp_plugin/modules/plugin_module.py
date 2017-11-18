import pprint, sys
import wp_plugin.file_template as f

class plugin_module:
	templates = None
	_config = None
	template_vars = None

	def __init__( self ):
		self._config = {}

		self.templates = {}
		self.template_vars = {}

		pass

	def add_template(self, template, template_vars = False, override = True ):
		key = template
		if not override:
			i = 1
			while key in self.templates:
				key = '%s-%d' % ( template ,i )
				i = i+1
		self.templates[key] = {
			'file'	: template,
			'vars'	: template_vars
		}

	def config(self, config, target_dir, plugin=False ):

		if not isinstance( config, dict ):
			config = {}

		self._config = config
		self.target_dir = target_dir
		self.plugin = plugin
		self.template_vars.update( self._config )


	def pre_process(self):
		pass


	def process(self):

		if self.plugin != False:
			config = self.plugin._config
		else:
			config = self._config
		default_template_vars = {}
		for key,template in self.templates.items():
			template_vars = {}
			if template['vars'] == False:
				template_vars.update( self.template_vars )
			else:
				template_vars.update( template['vars'] )

			if self.plugin != False:
				template_vars.update(self.plugin.template_vars)

			f.file_template( template['file'], template_vars, self.target_dir ).process()

	def post_process(self):
		pass
