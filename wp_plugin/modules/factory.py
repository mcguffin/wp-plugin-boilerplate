
class factory:
	def get( mod ):
		module = __import__('wp_plugin.modules.'+mod, fromlist=[mod])
		mod_class = getattr(module,mod)
		return mod_class()
