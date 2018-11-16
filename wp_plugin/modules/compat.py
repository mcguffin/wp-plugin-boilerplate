import wp_plugin.modules.plugin_module as m

class compat(m.plugin_module):

	def pre_process(self):
		super().pre_process()
		self.add_template('include/{{plugin_namespace}}/Compat/ACF.php')
		self.add_template('include/{{plugin_namespace}}/Compat/Polylang.php')
		self.add_template('include/{{plugin_namespace}}/Compat/RegenerateThumbnails.php')
		self.add_template('include/{{plugin_namespace}}/Compat/WPMU.php')
		self.add_template('include/acf-json/group_PREFIX_GROUPNAME.json.tpl')
