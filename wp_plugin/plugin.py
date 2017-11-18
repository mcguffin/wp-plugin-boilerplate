# -*- coding: utf-8 -*-

import sys, pprint, codecs, json
#from wp_plugin.modules import plugin_module
import wp_plugin.modules.plugin_module as m
import wp_plugin.modules.factory as factory

class plugin( m.plugin_module ):

	_modules = {}

	_config = {
		'plugin_name' 		: '',
		'plugin_slug' 		: '',
		'wp_plugin_slug'	: '',
		'plugin_namespace'	: '',
		'plugin_author'		: '',
		'plugin_author_uri'	: '',
	}

	def __init__( self ):
		m.plugin_module.__init__(self)

		self.add_template('readme.txt')
		self.add_template('index.php')
		self.add_template('languages/{{wp_plugin_slug}}.pot')
		self.add_template('include/autoload.php')
		self.add_template('include/{{plugin_namespace}}/Core/Singleton.php')
		self.add_template('include/{{plugin_namespace}}/Core/Core.php')
		self.add_template('include/{{plugin_namespace}}/Core/Plugin.php')
		self.add_template('include/{{plugin_namespace}}/Core/PluginComponent.php')

	def config(self, config, target_dir, plugin=False ):
		m.plugin_module.config( self, config, target_dir, plugin )

		if not 'modules' in self._config:
			self._config['modules'] = {} # cli arg module config

		for m,mconf in self._config['modules'].items():
			self.add_module( m, mconf )


		self.template_vars['modules'] = {} # generated module config

	def add_module( self, mod, module_config):

		self._modules[mod] = factory.factory.get( mod )
		self._modules[mod].config( module_config, self.target_dir, plugin=self )
		self._config['modules'][mod] = module_config

		if bool(self._modules[mod].template_vars):
			mod_vars = self._modules[mod].template_vars
		else:
			mod_vars = True
		self.template_vars['modules'][mod] = mod_vars
#		self.template_vars['_modules'][mod] = self._modules[mod]._config


	def pre_process(self):
		for mod,module in self._modules.items():
			module.pre_process()

		m.plugin_module.pre_process(self)

	def process(self):

		for mod,module in self._modules.items():
			module.process()

		m.plugin_module.process(self)

	def post_process(self):
		for mod,module in self._modules.items():
			module.post_process()

		m.plugin_module.post_process(self)
		pprint.pprint( self.template_vars )
#		pprint.pprint( self._config )
		f = codecs.open( self.target_dir + '/wp-plugin-boilerplate.json', 'w' )
		f.write( json.dumps(self._config, indent=2, sort_keys=True) )
		f.close()
