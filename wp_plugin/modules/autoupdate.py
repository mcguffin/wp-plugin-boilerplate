import wp_plugin.modules.plugin_module as m

class autoupdate(m.plugin_module):

	def pre_process(self):
		m.plugin_module.pre_process(self)
		self.add_template('include/{{plugin_namespace}}/AutoUpdate/AutoUpdate.php')
		self.add_template('include/{{plugin_namespace}}/AutoUpdate/AutoUpdateGithub.php')

	def config( self, config, target_dir, plugin=False ):
		m.plugin_module.config( self, config, target_dir, plugin )
