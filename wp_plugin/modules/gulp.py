
import subprocess
import wp_plugin.modules.plugin_module as m

class gulp(m.plugin_module):

	def pre_process(self):
		m.plugin_module.pre_process(self)
		self.add_template('package.json')
		self.add_template('gulpfile.js', self.plugin._config)

	def process(self):

		m.plugin_module.process(self)

		subprocess.call( [ "npm","install", "--prefix", "./" + self.plugin._config['wp_plugin_slug'] ] )

		print ( 'cd into `%s`, run `gulp` and have fun coding!' % ( self.plugin._config['wp_plugin_slug'] ) )
