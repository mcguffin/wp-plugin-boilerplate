import pprint, sys, copy
import wp_plugin.file_template as f

class plugin_module:
	override = False
	update = False
	_templates = None
	_config = None

	templates = []

	def __init__( self ):
		self._config = {}

		self._templates = {}
		self.template_vars = {}

		pass

	def set_override(self,override):
		self.override = override

	def set_update(self,update):
		self.update = update


	def add_template(self, template_name, template_vars = {} ):

		template_vars.update(self._config)

		template = f.file_template( template_name, template_vars, self.target_dir )

		self._templates[template.target_filename] = template


	def configure(self, config, target_dir, plugin=False ):

		if not isinstance( config, dict ):
			config = {}

		self._config = config
		self.target_dir = target_dir
		self.plugin = plugin


	def pre_process(self):
		for template in self.templates:
			template_config = copy.deepcopy(self._config)
			if self.plugin:
				template_config.update(self.plugin._config)
			self.add_template( template, template_config )
		pass


	def process(self):

		if self.plugin != False:
			config = self.plugin._config
		else:
			config = self._config

		for k,template in self._templates.items():
			template.process( self.override )

	def post_process(self):
		pass
