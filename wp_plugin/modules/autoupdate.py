import wp_plugin.modules.plugin_module as m

class autoupdate(m.plugin_module):

	def pre_process(self):
		super().pre_process()
		self.plugin.add_template('include/{{plugin_namespace}}/AutoUpdate/AutoUpdate.php')
		self.plugin.add_template('include/{{plugin_namespace}}/AutoUpdate/AutoUpdateGithub.php')

	def config( self, config, target_dir, plugin=False ):
		super().config( config, target_dir, plugin )
