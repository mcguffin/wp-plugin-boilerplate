#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, pystache, re, pwd, pprint, shutil,codecs,subprocess
from datetime import date
from pprint import pprint

class wp_plugin:
	template_path = '/templates/v2/'
	defaults = {
		'plugin_name' : '',
		'plugin_slug' : '',
		'wp_plugin_slug' : '',
		'plugin_namespace' : '',
		'plugin_author' : '',
		'plugin_author_uri' : '',

		# command line args
		'core'			: 'core',
		'admin'			: False,
		'admin_page'	: False,
		'settings'		: False,
		'shortcode'		: False,
		'widget'		: False,
		'post_type'		: False,
		'taxonomy'		: False,
		'model'			: False,
		'git'			: False,
		'gulp'			: False,

		'github_user'	: False
	}
	_private_defaults = {
		'shell_command' : False
	}
	allowed_admin_pages = [
		'dashboard',
		'posts',
		'media',
		'links',
		'pages',
		'comments',
		'theme',
		'plugins',
		'users',
		'management'
	]
	wp_settings_pages = [
		'general',
		'writing',
		'reading',
		'discussion',
		'media',
		'permalink'
	]
	templates = []

	def __init__(self,config):
		self.config = self.process_config(config)
		self.plugin_dir = os.getcwd()+'/'+slugify(self.config['plugin_name'],'-')
		pass

	def process_config(self,config):
		# set names
		config['plugin_slug'] 		= plugin_slug( config['plugin_name'] )
		config['plugin_slug_upper'] = config['plugin_slug'].upper()
		config['wp_plugin_slug']	= slugify(config['plugin_name'],'-')
		config['plugin_namespace']  = plugin_classname( config['plugin_name'] )
		author 						= pwd.getpwuid( os.getuid() ).pw_gecos

		try:
			github_user = subprocess.check_output(["git","config","user.name"]).strip()
			print "github user is",github_user
		except:
			github_user = ''
			pass

		config['github_user'] 		= github_user.decode('utf-8')#.encode('utf-8')
		config['plugin_author'] 	= author.decode('utf-8')#.encode('utf-8')
		config['plugin_author_uri'] = ''
		config['this_year'] 		= date.today().year

		if config['post_type'] and not len( config['post_type'][0] ):
			config['post_type'] = False
			print 'Could not generate post_type.'
			print 'post_type usage is: post_type:"Post Type Name"[+caps]'

		if config['taxonomy'] and not len( config['taxonomy'][0] ):
			config['taxonomy'] = False
			print 'Could not generate Taxonomy.'
			print 'taxonomy usage is:taxonomy:"taxonomy Name"'

		if config['shortcode'] and not len( config['shortcode'][0] ):
			config['shortcode'] = False
			print 'Could not generate shortcode.'
			print 'shortcode usage is: shortcode:a_shortcode'

		if config['widget'] and not len( config['widget'][0] ):
			config['widget'] = False
			print 'Could not generate widget.'
			print 'widget usage is: widget:"Widget Name"'


		for section in 'admin_page','post_type','shortcode','widget':
			if config[section]:
				config[section+'?'] = True
				config[section+'s'] = []
				for it,flags in config[section][0]:
					config[section+'s'].append( plugin_classname( it ) )


		return config

	def make(self):
		# make plugin dir
		try:
			os.mkdir(self.plugin_dir)
		except OSError as e:
			return e

		self.templates.append( ( 'readme.txt', self.config ) )
		self.templates.append( ( 'languages/__wp_plugin_slug__.pot', self.config ) )
		self.templates.append( ( 'include/autoload.php', self.config ) )
		self.templates.append( ( 'include/__plugin_namespace__/Core/Core.php', self.config ) )
		self.templates.append( ( 'include/__plugin_namespace__/Core/Singleton.php', self.config ) )
		self.templates.append( ( 'include/__plugin_namespace__/Core/Plugin.php', self.config ) )
		self.templates.append( ( 'include/__plugin_namespace__/Core/PluginComponent.php', self.config ) )
		self.templates.append( ( 'include/__plugin_namespace__/Compat/Sample.php', self.config ) )
		self.templates.append( ( 'include/__plugin_namespace__/Ajax/Ajax.php', self.config ) )
		self.templates.append( ( 'include/__plugin_namespace__/Ajax/AjaxHandler.php', self.config ) )
		self.templates.append( ( 'include/__plugin_namespace__/Cron/Cron.php', self.config ) )
		self.templates.append( ( 'include/__plugin_namespace__/Cron/Job.php', self.config ) )
		self.templates.append( ( 'src/scss/mixins/_mixins.scss', self.config ) )
		self.templates.append( ( 'src/scss/variables/_variables.scss', self.config ) )
		self.templates.append( ( 'src/scss/variables/_dashicons.scss', self.config ) )
		self.templates.append( ( 'src/scss/variables/_colors.scss', self.config ) )

		if self.config['gulp']:

			self.gulp_scss = []
			self.gulp_scss_admin = []
			self.gulp_js = []
			self.gulp_js_admin = []

		if self.config['git']:
			self.templates.append( ( 'README.md', self.config ) )
			self.templates.append( ( '.gitignore', self.config ) )
			self.templates.append( ( '.gitattributes', self.config ) )

		if self.config['admin']:
			flags = self.config['admin'][1]
			config_copy = self.config.copy()
			config_copy.update( dict( (x,True) for x in flags )  )
			self.templates.append( ( 'include/__plugin_namespace__/Admin/Admin.php', config_copy ) );
			if 'css' in flags:
				self.templates.append( ( 'src/scss/admin/admin.scss', config_copy ) );
				if self.config['gulp']:
					self.gulp_scss_admin.append('admin/admin')
			if 'js' in flags:
				self.templates.append( ( 'src/js/admin/admin.js', config_copy ) );
				if self.config['gulp']:
					self.gulp_js_admin.append( 'admin/admin' )

		if self.config['admin_page']:
			if self.config['admin_page'][0]:
				self.templates.append( ( 'include/__plugin_namespace__/Admin/Page.php', self.config ) );

			for admin_page,flags in self.config['admin_page'][0]:
				config_copy = self.config.copy()

				if admin_page == 'tools':
					wp_page_slug = 'management'
				else:
					wp_page_slug = admin_page
				config_copy.update({
					'wp_page_slug': wp_page_slug,
					'plugin_file': admin_page.title(),
					'plugin_class': plugin_classname( admin_page ),
					'plugin_asset': admin_page.lower(),
				})
				config_copy.update( dict( (x,True) for x in flags ) )
				self.templates.append( ( 'include/__plugin_namespace__/Admin/Admin__plugin_file__.php', config_copy ) );

				if 'css' in flags:
					self.templates.append( ( 'src/scss/admin/page/__plugin_asset__.scss', config_copy ) );
					if self.config['gulp']:
						self.gulp_scss_admin.append( pystache.render( 'admin/page/{{plugin_asset}}', config_copy ) )
				if 'js' in flags:
					self.templates.append( ( 'src/js/admin/page/__plugin_asset__.js', config_copy ) );
					if self.config['gulp']:
						self.gulp_js_admin.append( pystache.render( 'admin/page/{{plugin_asset}}', config_copy ) )


		if self.config['core']:
			flags = self.config['core'][1]
			config_copy = self.config.copy()
			config_copy.update( dict( (x,True) for x in flags )  )
			self.templates.append( ( 'include/__plugin_namespace__/Core/Core.php', config_copy ) );
			if 'css' in flags:
				self.templates.append( ( 'src/scss/frontend.scss', config_copy ) );
				if self.config['gulp']:
					self.gulp_scss.append( 'frontend' )
			if 'js' in flags:
				self.templates.append( ( 'src/js/frontend.js', config_copy ) );
				if self.config['gulp']:
					self.gulp_js.append( 'frontend' )
			pass


		if self.config['post_type']:
			if self.config['post_type'][0]:
				self.templates.append( ( 'include/__plugin_namespace__/PostType/PostType.php', self.config ) );

			for post_type,flags in self.config['post_type'][0]:
				config_copy = self.config.copy()

				config_copy.update({
					'post_type_slug': slugify( post_type, '-' ),
					'post_type_name': post_type,
					'plugin_file': plugin_classname( post_type ),
					'plugin_class': plugin_classname( post_type ),
				})
				config_copy.update( dict( (x, True) for x in flags ) )
				self.templates.append( ( 'include/__plugin_namespace__/PostType/PostType__plugin_file__.php', config_copy ) );

		if self.config['taxonomy']:
			if self.config['taxonomy'][0]:
				self.templates.append( ( 'include/__plugin_namespace__/Taxonomy/Taxonomy.php', self.config ) );

			for taxonomy,flags in self.config['taxonomy'][0]:
				config_copy = self.config.copy()

				config_copy.update({
					'taxonomy_slug': slugify( taxonomy, '-' ),
					'taxonomy_name': taxonomy,
					'plugin_file': plugin_classname( taxonomy ),
					'plugin_class': plugin_classname( taxonomy ),
				})
				config_copy.update( dict( (x, True) for x in flags ) )
				self.templates.append( ( 'include/__plugin_namespace__/Taxonomy/Taxonomy__plugin_file__.php', config_copy ) );

		admin_settings_classes = [];

		if self.config['settings']:

			flags = self.config['settings'][1]

			self.templates.append( ( 'include/__plugin_namespace__/Settings/Settings.php', config ) );

			for settings,flags in self.config['settings'][0]:
				config_copy = self.config.copy()
				config_copy.update( dict( (x,True) for x in flags )  )
				if settings in self.wp_settings_pages:
					classname = plugin_classname( 'Settings ' + settings )
					section = settings
				else:
					classname = plugin_classname( 'Settings Page ' + settings )
					section = slugify( settings, '_' )

				config_copy.update({
					'settings_section'	: section,
					'settings_class'	: classname,
					'plugin_file'		: classname,
					'is_page'			: settings not in self.wp_settings_pages,
					'is_section'		: settings in self.wp_settings_pages,
				})

				self.templates.append( ( 'include/__plugin_namespace__/Settings/Settings__plugin_file__.php', config_copy ) );

				admin_settings_classes.append( classname )

				if 'css' in flags:
					self.templates.append( ( 'src/scss/admin/settings/__plugin_asset__.scss', config_copy ) );
					if self.config['gulp']:
						self.gulp_scss_admin.append( pystache.render( 'admin/settings/{{plugin_asset}}', config_copy ) )
				if 'js' in flags:
					self.templates.append( ( 'src/js/admin/settings/__plugin_asset__.js', config_copy ) );
					if self.config['gulp']:
						self.gulp_js_admin.append( pystache.render( 'admin/settings/{{plugin_asset}}', config_copy ) )

		if self.config['model']:
			if self.config['model'][0]:
				self.templates.append( ( 'include/__plugin_namespace__/Model/Model.php', self.config ) );

			for model,flags in self.config['model'][0]:
				config_copy = self.config.copy()
				config_copy.update({
					'model_slug': slugify( model, '-' ),
					'model_name': model.title(),
					'plugin_file': plugin_classname( model ),
					'plugin_class': plugin_classname( model ),
				})
				self.templates.append( ( 'include/__plugin_namespace__/Model/Model__plugin_file__.php', config_copy ) );


		if self.config['shortcode']:
			if self.config['shortcode'][0]:
				self.templates.append( ( 'include/__plugin_namespace__/Shortcode/Shortcode.php', self.config ) );
				self.templates.append( ( 'include/__plugin_namespace__/Admin/Mce/Mce.php', config_copy ) );

			for shortcode,flags in self.config['shortcode'][0]:
				config_copy = self.config.copy()
				config_copy.update({
					'shortcode_slug': slugify( shortcode, '-' ),
					'shortcode_name': shortcode.title(),
					'plugin_file': plugin_classname( shortcode ),
					'plugin_asset': slugify( shortcode, '-' ),
					'plugin_class': plugin_classname( shortcode ),
				})
				config_copy.update( dict( (x, True) for x in flags ) )
				self.templates.append( ( 'include/__plugin_namespace__/Shortcode/Shortcode__plugin_file__.php', config_copy ) );

				if 'mce' in flags:
					# add mce templates
					self.templates.append( ( 'include/__plugin_namespace__/Shortcode/Mce/Mce__plugin_file__.php', config_copy ) );
					self.templates.append( ( 'src/js/admin/mce/__plugin_asset__-shortcode.js', config_copy ) );
					self.templates.append( ( 'src/scss/admin/mce/__plugin_asset__-shortcode-mce-editor.scss', config_copy ) );
					self.templates.append( ( 'src/scss/admin/mce/__plugin_asset__-shortcode-mce-toolbar.scss', config_copy ) );
					if self.config['gulp']:
						self.gulp_scss_admin.append( pystache.render( 'admin/mce/{{plugin_asset}}-shortcode-mce-editor', config_copy ) )
						self.gulp_scss_admin.append( pystache.render( 'admin/mce/{{plugin_asset}}-shortcode-mce-toolbar', config_copy ) )
						self.gulp_js_admin.append( pystache.render( 'admin/mce/{{plugin_asset}}-shortcode', config_copy ) )


		if self.config['widget']:
			if self.config['widget'][0]:
				self.templates.append( ( 'include/__plugin_namespace__/Widget/Widgets.php', self.config ) );

			for widget,flags in self.config['widget'][0]:
				config_copy = self.config.copy()

				config_copy.update({
					'widget_slug': slugify( widget, '-' ),
					'widget_name': widget.title(),
					'plugin_file': plugin_classname( widget ),
					'plugin_class': plugin_classname( widget ),
				})
				self.templates.append( ( 'include/__plugin_namespace__/Widget/Widget__plugin_file__.php', config_copy ) );

		config_copy = self.config.copy()
		config_copy.update({
			'settings_classes'	: admin_settings_classes,
		})

		self.templates.append( ( 'index.php', config_copy ) )

		self.init_gulp()

		self.process_templates()

		self.do_gulp()

		self.do_git()

		return ''

	def init_gulp(self):

		if self.config['gulp']:
			gulp_config = self.config.copy()
			gulp_config['scss'] = self.gulp_scss
			gulp_config['js'] = self.gulp_js
			gulp_config['scss_admin'] = self.gulp_scss_admin
			gulp_config['js_admin'] = self.gulp_js_admin

			self.templates.append( ( 'gulpfile.js', gulp_config ) )
			self.templates.append( ( 'package.json', self.config ) )

	def do_gulp(self):
		if self.config['gulp']:
			print 'Installing npm dependencies'

			subprocess.call( [ "npm","install", "--prefix", "./" + self.config['wp_plugin_slug'] ] )

			print 'cd into `%s`, run `gulp` and have fun coding!' % ( self.config['wp_plugin_slug'] )


	def do_git(self):
		if self.config['git'] and self.config['github_user']:

			if self.config['github_user']:
				repo_name = 'git@github.com:%s/%s.git' % ( self.config['github_user'] , self.config['wp_plugin_slug'] )
				print "Creating git repository %s" % repo_name
			else:
				print "Creating git repository"
			print self.plugin_dir
			os.chdir(self.plugin_dir);
			subprocess.call(["git","init"])
			subprocess.call(["git","add" , '.'])
			subprocess.call(["git","commit" , '-m "Initial commit"'])
			if self.config['github_user']:
				subprocess.call(['git','remote' , 'add' , 'origin' , repo_name ])
				print 'Git repository created. Now head over to github.com and create a repository named `%s`' % ( self.config['wp_plugin_slug'] )
				print 'Finally come back and type `git push -u origin master` here.'

		pass

	def process_templates(self):
		for template, template_config in self.templates:
			content = pystache.render( self._read_template(template), template_config )
			self._write_plugin_file( template, content, template_config )


	def _read_template(self,template):
		template_path = os.path.dirname(os.path.realpath(__file__)) + self.template_path + template
		return self._read_file_contents( template_path )

	def _write_plugin_file( self , template , contents, config ):
		template_filename = template
		for confkey in config.keys():
			if confkey.find('plugin') >= 0:
#				print '__' + confkey + '__', config[confkey]
				template_filename = template_filename.replace( '__' + confkey + '__', config[confkey] )
#		print 'Process File:',template_filename
		plugin_path = self.plugin_dir + '/'+template_filename
		return self._write_file_contents( plugin_path , contents )


	def _read_file_contents( self , file_path ):
		if not os.path.exists(file_path):
			return ''
		f = codecs.open(file_path,'rb',encoding='utf-8')
		contents = f.read()
		f.close()
		return contents

	def _write_file_contents( self , file_path , contents ):
		dir = os.path.dirname(file_path)
		if not os.path.exists(dir):
			os.makedirs(dir)
		f = codecs.open(file_path,'wb',encoding='utf-8')
		f.write(contents)
		f.close()

def rm_wp(str):
	return re.sub(r'(?i)^(WP|WordPress\s?)-?','',str).strip()

def slugify(plugin_name,separator='_'):
	return re.sub(r'\s',separator,plugin_name.strip()).lower()

def plugin_slug(plugin_name):
	return slugify(rm_wp(plugin_name),'_')

def plugin_classname(plugin_name):
	return ''.join(x for x in rm_wp(plugin_name).title() if x.isalnum())


usage = '''
usage ./plugin.py 'Plugin Name' options
  options can be any of:
    core[+css][+js]
              Add +css and/or +js to enqueue frontend css / js
    admin[+css][+js]
              Add an admin class. Add +css and/or +js to enqueue css / js
              in the entire wp admin.

    model:a_model[:another_model]
              Add a model class.

    admin_page[:a_page[+css][+js]][:a_page:...]...
              Add submenu page to admin.
              `a_page` can either be any of
                dashboard
                posts
                media
                links
                pages
                comments
                theme
                plugins
                users
                management
                tools (Alias of management)
                (or any custom page slug.)

              With `+css` and `+js` appended to the page slug CSS and
              JS will also be enqueued on the given page.

    settings:page[+css][+js][:page:...]...
              Create a new settings section on a WP settings page.
              `page` can be any of the WordPress settings page slugs:
                general
                writing
                reading
                discussion
                media
                permalink
              For any other value a standalone settings page will be generated
              With `+css` and `+js` appended to the settings slug custom CSS and JS will
              also be enqueued on the given settings page.

    shortcode:a_shortcode[:another_shortcode]:...
              Add shortcode handlers

    post_type:'Post Type name'[+caps]:'Another Post type'...
              Register post type. +caps will register post type's capabilities

    taxonomy:'Taxonomy'[:'Another Taxonomy']...
              Register taxonomies

    widget:'Widget Name'[:'Another Widget']
              Register one or more Widgets

    git       Inits a git repository

    gulp      Use gulp

    --force   Override existing plugin
'''


defaults = config = wp_plugin.defaults

try:
	config['plugin_name']	= sys.argv[1]
except IndexError as e:
	print usage
	sys.exit(0)

config['shell_args']		= "\"%s\" %s" % ( sys.argv[1] , ' '.join(sys.argv[2:]) )

def getflags( param ):
	paramlist = param.split('+')
	return paramlist[0],paramlist[1:]

for arg in sys.argv[2:]:
	param = []
	flags = True
	conf  = arg.split(':')
	# conf = cmd, param+js+css, param+css, ...
	# OR conf = cmd+js+css
	if len(conf) > 1:
		param = conf[1:]
	conf = conf[0]
	# conf = cmd
	# OR conf = cmd+js+css
	conf,flags = getflags( conf )
	param = [ getflags( par ) for par in param ]

	if conf in defaults.keys():
		config[conf] = param,flags
#pprint(config)

print "Generating Plugin:", config['plugin_name']
maker = wp_plugin(config)

if '--force' in sys.argv and os.path.exists(maker.plugin_dir):
	print "remove existing plugin"
	shutil.rmtree( maker.plugin_dir )

result = maker.make()

if isinstance(result, Exception):
	print 'Plugin exists:',result
	print 'use --force to override existing plugin'
