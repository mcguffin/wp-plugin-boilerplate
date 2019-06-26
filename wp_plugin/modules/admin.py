import wp_plugin.modules.plugin_module as m

class admin(m.plugin_module):

	templates = [
		'include/{{plugin_namespace}}/Admin/Admin.php'
	]


	def configure( self, config, target_dir, plugin=False ):

		super().configure( config, target_dir, plugin )

		if 'css' in config:
			self.add_template('src/scss/admin/main.scss')

		if 'js' in config:
			self.add_template('src/js/admin/main/index.js')
