
import subprocess
import wp_plugin.modules.plugin_module as m

class gulp(m.plugin_module):

	templates = [
		'package.json',
		'gulpfile.js',
	]

	def process(self):

		super().process()

		subprocess.call( [ "npm","install" ] )
