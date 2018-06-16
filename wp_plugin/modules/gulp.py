
import subprocess
import wp_plugin.modules.plugin_module as m

class gulp(m.plugin_module):

	def pre_process(self):
		super().pre_process()
		self.add_template('package.json')
		self.add_template('gulpfile.js', self.plugin._config)

	def process(self):

		super().process()

		if self.update:
			subprocess.call( [ "npm","install" ] )
		else:
			subprocess.call( [ "npm","install", "--prefix", "./" + self.plugin._config['wp_plugin_slug'] ] )

		print ( 'cd into `%s`, run `gulp` and have fun coding!' % ( self.plugin._config['wp_plugin_slug'] ) )
