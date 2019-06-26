from wp_plugin import plugin_slug, plugin_classname, slugify
import wp_plugin.modules.plugin_module as m

class wpcli(m.plugin_module):

	templates = [
		'include/{{plugin_namespace}}/WPCLI/WPCLI.php'
	]

	def configure( self, config, target_dir, plugin=False ):
		items = []
		for name, cnf in config.items():
			model_config = {}
			model_config.update(cnf)
			model_config.update({
				'module' : {
					'name'			: name,
					'classname'		: plugin_classname(name),
					'slug'			: slugify( name, '_' ),
				}
			})

			items.append(model_config)
			template_vars = {}
			template_vars.update(model_config)
			template_vars.update(plugin._config)

			self.add_template('include/{{plugin_namespace}}/WPCLI/Commands/{{module.classname}}.php', template_vars )

		super().configure( config, target_dir, plugin )
