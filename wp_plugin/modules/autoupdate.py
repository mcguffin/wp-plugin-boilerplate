import wp_plugin.modules.plugin_module as m

class autoupdate(m.plugin_module):

	templates = [
		'include/{{plugin_namespace}}/AutoUpdate/AutoUpdate.php',
		'include/{{plugin_namespace}}/AutoUpdate/AutoUpdateGithub.php',
	]
