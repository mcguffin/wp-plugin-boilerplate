from wp_plugin import plugin_slug, plugin_classname, slugify
import wp_plugin.modules.plugin_module as m
import sys,os

class core(m.plugin_module):

	templates = [
		'readme.txt',
		'index.php',
		'languages/{{wp_plugin_slug}}.pot',
		'include/autoload.php',
		'include/{{plugin_namespace}}/Core/Core.php',
		'include/{{plugin_namespace}}/Core/Plugin.php',
		'include/{{plugin_namespace}}/Core/PluginComponent.php',
		'include/{{plugin_namespace}}/Core/Singleton.php',
		'src/scss/mixins/_mixins.scss',
		'src/scss/variables/_colors.scss',
		'src/scss/variables/_dashicons.scss',
		'src/scss/variables/_variables.scss',
		'src/run/release.js',
		'src/run/release-github.js',
		'src/run/release-bitbucket.js',
		'src/run/release-wporg.js',
		'src/run/lib/json-extract.js',
		'src/run/lib/wp-release.js',
		'.editorconfig',
	]

	def configure( self, config, target_dir, plugin=False ):

		super().configure( config, target_dir, plugin )

		if 'css' in config:
			self.add_template('src/scss/main.scss')

		if 'js' in config:
			self.add_template('src/js/main/index.js')
