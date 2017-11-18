from wp_plugin import getflags, plugin_slug, plugin_classname, slugify
import wp_plugin.modules.plugin_module as m

class admin_page(m.plugin_module):

	def pre_process(self):
		super().pre_process()
		self.plugin.add_template('include/{{plugin_namespace}}/Admin/AdminPage.php')


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
			page_config = {}
			page_config.update(cnf)
			if name in wp_page_slugs:
				wp_page_slug = name
			else:
				wp_page_slug = 'dashboard'

			page_config.update({
				'module' : {
					'name'			: name,
					'classname'		: plugin_classname(name),
					'slug'			: slugify( name, '-' ),
					'wp_page_slug'	: wp_page_slug,
				}
			})

			items.append(page_config)

			template_vars = {}
			template_vars.update(plugin._config)
			template_vars.update(page_config)

			self.add_template('include/{{plugin_namespace}}/Admin/AdminPage{{module.classname}}.php', template_vars, False )

			if 'css' in page_config:
				self.add_template('src/scss/admin/page/{{module.slug}}.scss', template_vars, False )
				plugin.add_template('src/scss/mixins/_mixins.scss')
				plugin.add_template('src/scss/variables/_colors.scss')
				plugin.add_template('src/scss/variables/_dashicons.scss')
				plugin.add_template('src/scss/variables/_variables.scss')

			if 'js' in page_config:
				self.add_template('src/js/admin/page/{{module.slug}}.js', template_vars, False )

		super().config( config, target_dir, plugin )

		self.template_vars = {'items' : items }
