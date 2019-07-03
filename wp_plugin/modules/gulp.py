
import subprocess
import wp_plugin.modules.plugin_module as m

class gulp(m.plugin_module):

	templates = [
		'package.json',
		'gulpfile.js',
		'.babelrc',
		'.eslintrc',
		'.eslintignore',
		'.sassrc',
	]

	# def process(self):
	#
	# 	super().process()
	#
	# 	subprocess.call( [ "npm","install" ] )
