
from wp_plugin import getflags, plugin_slug, plugin_classname, slugify
import wp_plugin.modules.plugin_module as m

class posttype(m.plugin_module):

	def pre_process(self):
		super().pre_process()
		self.add_template('include/{{plugin_namespace}}/PostType/PostType.php')


	def config( self, config, target_dir, plugin=False ):
		items = []
		for name, cnf in config.items():
			pt_config = {}
			pt_config.update(cnf)
			pt_config.update({
				'module' : {
					'name'		: name,
					'classname'	: plugin_classname(name),
					'slug'		: slugify( name, '-' ),
					'caps'		: 'caps' in pt_config
				}
			})

			items.append(pt_config)
			template_vars = {}
			template_vars.update(pt_config)
			template_vars.update(plugin._config)


			self.add_template('include/{{plugin_namespace}}/PostType/PostType{{module.classname}}.php', template_vars, False )

		super().config( config, target_dir, plugin )

		self.template_vars = {'items' : items }
