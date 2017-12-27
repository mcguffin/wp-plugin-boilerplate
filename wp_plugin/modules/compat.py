import wp_plugin.modules.plugin_module as m

class compat(m.plugin_module):

	def pre_process(self):
		super().pre_process()
		self.add_template('include/{{plugin_namespace}}/Compat/WPMU.php')
