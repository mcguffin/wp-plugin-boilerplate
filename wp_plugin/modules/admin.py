import wp_plugin.modules.plugin_module as m

class admin(m.plugin_module):

	def pre_process(self):
		m.plugin_module.pre_process(self)
		self.add_template('include/{{plugin_namespace}}/Admin/Admin.php')



	def config( self, config, target_dir, plugin=False ):
		if 'css' in config:
			self.add_template('src/scss/admin/admin.scss')
			plugin.add_template('src/scss/mixins/_mixins.scss')
			plugin.add_template('src/scss/variables/_colors.scss')
			plugin.add_template('src/scss/variables/_dashicons.scss')
			plugin.add_template('src/scss/variables/_variables.scss')

		if 'js' in config:
			self.add_template('src/js/admin/admin.js')

		m.plugin_module.config( self, config, target_dir, plugin )
