
from wp_plugin import plugin_slug, plugin_classname, slugify
import wp_plugin.modules.plugin_module as m

class widget(m.plugin_module):
	templates = [
		'include/{{plugin_namespace}}/Widget/Widgets.php'
	]

	def configure( self, config, target_dir, plugin=False ):

		super().configure( config, target_dir, plugin )

		for name, cnf in config.items():
			widget_config = {}
			widget_config.update({
				'module' : {
					'name'			: name,
					'classname'		: plugin_classname(name),
					'slug'			: slugify( name, '-' ),
				}
			})

			template_vars = {}
			template_vars.update(widget_config)
			template_vars.update(plugin._config)

			self.add_template('include/{{plugin_namespace}}/Widget/Widget{{module.classname}}.php', template_vars )
			if 'css' in widget_config:
				self.add_template('src/scss/widget/{{module.slug}}.scss', template_vars )
				plugin.add_template('src/scss/frontend.scss')
				plugin.add_template('src/scss/mixins/_mixins.scss')
				plugin.add_template('src/scss/variables/_colors.scss')
				plugin.add_template('src/scss/variables/_dashicons.scss')
				plugin.add_template('src/scss/variables/_variables.scss')

			if 'js' in widget_config:
				self.add_template('src/js/widget/{{module.slug}}/index.js', template_vars )
