import wp_plugin.modules.plugin_module as m

class ajax(m.plugin_module):

	def pre_process(self):
		super().pre_process()
		self.plugin.add_template('include/{{plugin_namespace}}/Ajax/AjaxHandler.php')
