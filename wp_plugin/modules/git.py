
import sys, os, subprocess
import wp_plugin.modules.plugin_module as m

class git(m.plugin_module):

	templates = [
		'README.md',
		'.gitattributes',
		'.gitignore',
	]

	def configure( self, config, target_dir, plugin=False ):
		git_user = subprocess.check_output(["git","config","user.name"]).strip().decode('ascii')

		git_host = False
		# could be better...
		if 'bitbucket' in config:
			git_host = 'bitbucket.org'

		if 'github' in config:
			git_host = 'github.com'
		config = {}

		print( "github user is",git_user)
		print(repr(config))
		super().configure( {}, target_dir, plugin )

		# update plugin config
		if git_user and 'git_user' not in self.plugin._config['modules']['git']:
			self.plugin._config['plugin_author_uri'] = 'https://github.com/%s' % (git_user)
			self.plugin._config['modules']['git'].update({
				'git_user' : git_user,
				'git_repo' : '%s/%s' % ( git_user, plugin._config['wp_plugin_slug'] ),
				'git_host' : git_host
			})
		print(repr(self.plugin._config['modules']['git']))

	def post_process(self):
		super().post_process()

		if os.path.exists( self.target_dir + '/.git'):
			return

		subprocess.call(["git","init"])
		subprocess.call(["git","add" , '.'])
		subprocess.call(["git","commit" , '-m "Initial commit"'])
		print(repr(self.plugin._config['modules']['git']))
		if self.plugin._config['modules']['git']['git_user']:
			repo_uri = 'git@%s:%s.git' % ( self.plugin._config['modules']['git']['git_host'], self.plugin._config['modules']['git']['git_repo'] )
			subprocess.call(['git','remote' , 'add' , 'origin' , repo_uri ])
			print( 'Git repository created. Now head over to %s and create a repository named `%s`' % ( self.plugin._config['modules']['git']['git_host'], self.plugin._config['modules']['git']['git_repo'] ) )
			print( 'Finally come back and type `git push -u origin master` here.' )
