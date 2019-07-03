# -*- coding: utf-8 -*-

import sys, codecs, json, os
from pprint import pprint
#from wp_plugin.modules import plugin_module
import wp_plugin.modules.plugin_module as m
import wp_plugin.modules.factory as factory

class plugin( m.plugin_module ):

	override = False
	update = False

	_modules = {}

	_config = {
		'plugin_name' 		: '',
		'plugin_slug' 		: '',
		'plugin_slug_upper'	: '',
		'wp_plugin_slug'	: '',
		'plugin_namespace'	: '',
		'plugin_author'		: '',
		'plugin_author_uri'	: '',
		'this_year'			: '',
	}

	def configure(self, config, target_dir, plugin=False ):

		super().configure( config, target_dir, plugin )

		if 'modules' not in self._config:
			self._config['modules'] = {} # cli arg module config

		self._config['plugin_slug_upper'] = self._config['plugin_slug'].upper()
		self._base_config = self._config

		for m, mconf in self._config['modules'].items():
			self.add_module( m, mconf )

	def set_update(self,update):
		super().set_update(update)
		for mod,module in self._modules.items():
			module.set_update(update)

	def set_override(self,override):
		super().set_override(override)
		for mod,module in self._modules.items():
			module.set_override(override)


	def add_module( self, mod, module_config):
		module = factory.factory.get( mod )
		if not module:
			print('No module named %s' % (mod))
			return

		self._modules[mod] = module
		self._modules[mod].configure( module_config, self.target_dir, plugin=self )
		#self._config['modules'][mod] = module_config



	def pre_process(self):

		if not os.path.exists(self.target_dir):
			os.makedirs(self.target_dir)

		os.chdir( self.target_dir )

		for mod,module in self._modules.items():
			module.pre_process()

		super().pre_process()

	def process(self):

		for mod,module in self._modules.items():
			module.process()

		super().process()

	def post_process(self):
		for mod,module in self._modules.items():
			module.post_process()

		super().post_process()
#		pprint.pprint( self._config )
		f = codecs.open( self.target_dir + '/wp-plugin-boilerplate.json', 'w' )
		f.write( json.dumps( self._config, indent=2, sort_keys=True) )
		f.close()
