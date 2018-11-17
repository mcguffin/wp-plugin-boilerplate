import wp_plugin.modules.plugin_module as m

class cron(m.plugin_module):

	def pre_process(self):
		super().pre_process()
		self.add_template('include/{{plugin_namespace}}/Cron/Cron.php')
		self.add_template('include/{{plugin_namespace}}/Cron/Job.php')
