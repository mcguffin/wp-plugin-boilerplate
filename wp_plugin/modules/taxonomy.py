
from wp_plugin import plugin_slug, plugin_classname, slugify
import wp_plugin.modules.plugin_module as m

class taxonomy(m.plugin_module):
	templates = [
		'include/{{plugin_namespace}}/Taxonomy/Taxonomy.php'
	]

	def configure( self, config, target_dir, plugin=False ):
		items = []
		for name, cnf in config.items():
			tax_config = {}
			tax_config.update(cnf)
			tax_config.update({
				'module' : {
					'name'		: name,
					'classname'	: plugin_classname(name),
					'slug'		: slugify( name, '-' ),
				}
			})

			items.append(tax_config)

			template_vars = {}
			template_vars.update(tax_config)
			template_vars.update(plugin._config)

			self.add_template('include/{{plugin_namespace}}/Taxonomy/Taxonomy{{module.classname}}.php', template_vars )


		super().configure( config, target_dir, plugin )
