import wp_plugin.modules.plugin_module as m

class compat(m.plugin_module):

	templates = [
	]

	def configure( self, config, target_dir, plugin=False ):

		super().configure( config, target_dir, plugin )

		if 'acf' in config:
			self.add_template('acf-json/group_PREFIX_GROUPNAME.json.tpl', plugin._config )
			self.add_template('include/{{plugin_namespace}}/Compat/ACF.php', plugin._config )

		if 'wpmu' in config:
			self.add_template('include/{{plugin_namespace}}/Compat/WPMU.php', plugin._config )

		if 'polylang' in config:
			self.add_template('include/{{plugin_namespace}}/Compat/Polylang.php', plugin._config )

		if 'regenerate_thumbnails' in config:
			self.add_template('include/{{plugin_namespace}}/Compat/RegenerateThumbnails.php', plugin._config )
