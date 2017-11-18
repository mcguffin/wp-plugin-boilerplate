
from wp_plugin import getflags, plugin_slug, plugin_classname, slugify
import wp_plugin.modules.plugin_module as m

class widget(m.plugin_module):

	def pre_process(self):
		m.plugin_module.pre_process(self)
		self.plugin.add_template('include/{{plugin_namespace}}/Widget/Widgets.php' )

	def config( self, config, target_dir, plugin=False ):

		wp_page_slugs = [
			'dashboard',
			'posts',
			'media',
			'links',
			'pages',
			'comments',
			'theme',
			'plugins',
			'users',
			'management',
			'options',
		]
		items = []
		for name, cnf in config.items():
			widget_config = {}
			widget_config.update(cnf)
			widget_config.update({
				'module' : {
					'name'			: name,
					'classname'		: plugin_classname(name),
					'slug'			: slugify( name, '-' ),
				}
			})

			items.append(widget_config)

			template_vars = {}
			template_vars.update(widget_config)
			template_vars.update(plugin._config)

			self.add_template('include/{{plugin_namespace}}/Widget/Widget{{module.classname}}.php', template_vars, False )
			if 'css' in widget_config:
				self.add_template('src/scss/widget/{{module.slug}}.scss', template_vars, False )
				plugin.add_template('src/scss/frontend.scss')
				plugin.add_template('src/scss/mixins/_mixins.scss')
				plugin.add_template('src/scss/variables/_colors.scss')
				plugin.add_template('src/scss/variables/_dashicons.scss')
				plugin.add_template('src/scss/variables/_variables.scss')

			if 'js' in widget_config:
				self.add_template('src/js/widget/{{module.slug}}.js', template_vars, False )

		m.plugin_module.config( self, config, target_dir, plugin )

		self.template_vars = {'items' : items}
