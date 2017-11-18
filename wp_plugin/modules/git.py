
import os,subprocess
import wp_plugin.modules.plugin_module as m

class git(m.plugin_module):

	def pre_process(self):
		super().pre_process()
		self.add_template('README.md')
		self.add_template('.gitattributes')
		self.add_template('.gitignore')

	def config(self,config,target_dir, plugin=False ):
		github_user = subprocess.check_output(["git","config","user.name"]).strip().decode('ascii')
		print( "github user is",github_user)

		super().config( config, target_dir, plugin )

		if github_user:
			self.plugin.template_vars['plugin_author_uri'] = 'https://github.com/%s' % (github_user)
			self.template_vars = {
				'github_user' : github_user,
				'github_repo' : '%s/%s' % ( github_user, plugin._config['wp_plugin_slug'] )
			}

	def post_process(self):
		super().post_process()
		os.chdir(self.target_dir);
		subprocess.call(["git","init"])
		subprocess.call(["git","add" , '.'])
		subprocess.call(["git","commit" , '-m "Initial commit"'])
		if self.template_vars['github_user']:
			repo_uri = 'git@github.com:%s.git' % self.template_vars['github_repo']
			subprocess.call(['git','remote' , 'add' , 'origin' , repo_uri ])
			print( 'Git repository created. Now head over to github.com and create a repository named `%s`' % ( self.template_vars['github_repo'] ) )
			print( 'Finally come back and type `git push -u origin master` here.' )
		pass
