
from wp_plugin import getflags, plugin_slug, plugin_classname, slugify
import wp_plugin.modules.plugin_module as m

class shortcode(m.plugin_module):

	def pre_process(self):
		super().pre_process()
		self.add_template('include/{{plugin_namespace}}/Shortcode/Shortcode.php')


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
			shortcode_config = {}
			shortcode_config.update(cnf)
			shortcode_config.update({
				'module' : {
					'name'				: name,
					'classname'			: plugin_classname(name),
					'slug'				: slugify( name, '-' ),
					'slug_underscore'	: slugify( name, '_' ),
				}
			})

			items.append(shortcode_config)
			template_vars = {}
			template_vars.update(shortcode_config)
			template_vars.update(plugin._config)

			self.add_template('include/{{plugin_namespace}}/Shortcode/Shortcode{{module.classname}}.php', template_vars, False )

			if 'mce' in shortcode_config:
				plugin.add_template('include/{{plugin_namespace}}/Admin/Mce/Mce.php')
				self.add_template('include/{{plugin_namespace}}/Shortcode/Mce/Mce{{module.classname}}.php', template_vars, False )

				self.add_template('src/scss/admin/mce/{{module.slug}}-shortcode-mce-editor.scss', template_vars, False )
				self.add_template('src/scss/admin/mce/{{module.slug}}-shortcode-mce-toolbar.scss', template_vars, False )
				self.add_template('src/js/admin/mce/{{module.slug}}-shortcode.js', template_vars, False )


		super().config( config, target_dir, plugin )

		self.template_vars = {'items' : items }
