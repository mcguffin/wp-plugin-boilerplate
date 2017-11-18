import wp_plugin.modules.plugin_module as m

class ajax(m.plugin_module):

	def pre_process(self):
		m.plugin_module.pre_process(self)
		self.add_template('include/{{plugin_namespace}}/Ajax/AjaxHandler.php')
