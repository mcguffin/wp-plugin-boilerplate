import wp_plugin.modules.plugin_module as m

class ajax(m.plugin_module):


	templates = [
		'include/{{plugin_namespace}}/Ajax/AjaxHandler.php'
	]
