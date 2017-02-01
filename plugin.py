#!/usr/local/bin/python
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

		templates = [
			( 'readme.txt', self.config ),
			( 'languages/__wp_plugin_slug__.pot', self.config ),
			( 'include/vendor/autoload.php', self.config ),
			( 'include/__plugin_namespace__/Core/Singleton.php', self.config ),
			( 'scss/mixins/_mixins.scss', self.config ),
			( 'scss/variables/_variables.scss', self.config ),
			( 'scss/variables/_dashicons.scss', self.config )
			];

		if self.config['gulp']:
			templates.append( ( 'package.json', self.config ) )
		
			gulp_scss = []
		

		if self.config['admin']:
			flags = self.config['admin'][1]
			config_copy = self.config.copy()
			config_copy.update( dict( (x,True) for x in flags )  )
			templates.append( ( 'include/__plugin_namespace__/Admin/Admin.php', config_copy ) );
			if 'css' in flags:
				templates.append( ( 'css/admin/admin.css', config_copy ) );
				templates.append( ( 'scss/admin/admin.scss', config_copy ) );
			if 'js' in flags:
				templates.append( ( 'js/admin/admin.js', config_copy ) );

		if self.config['admin_page']:
			if self.config['admin_page'][0]:
				templates.append( ( 'include/__plugin_namespace__/Admin/Page.php', self.config ) );

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
				templates.append( ( 'include/__plugin_namespace__/Admin/__plugin_file__.php', config_copy ) );

				if 'css' in flags:
					templates.append( ( 'css/admin/admin-page-__plugin_asset__.css', config_copy ) );
					templates.append( ( 'scss/admin/admin-page-__plugin_asset__.scss', config_copy ) );
					if self.config['gulp']:
						gulp_scss.append( pystache.render( 'admin/admin-page-{{plugin_asset}}', config_copy ) )
				if 'js' in flags:
					templates.append( ( 'js/admin/admin-page-__plugin_asset__.js', config_copy ) );


		if self.config['core']:
			flags = self.config['core'][1]
			config_copy = self.config.copy()
			config_copy.update( dict( (x,True) for x in flags )  )
			templates.append( ( 'include/__plugin_namespace__/Core/Core.php', config_copy ) );
			if 'css' in flags:
				templates.append( ( 'css/frontend.css', config_copy ) );
				templates.append( ( 'scss/frontend.scss', config_copy ) );
				if self.config['gulp']:
					gulp_scss.append( 'frontend' )
			if 'js' in flags:
				templates.append( ( 'js/frontend.js', config_copy ) );
			pass


		if self.config['post_type']:
			if self.config['post_type'][0]:
				templates.append( ( 'include/__plugin_namespace__/PostType/PostType.php', self.config ) );

			for post_type,flags in self.config['post_type'][0]:
				config_copy = self.config.copy()
				
				config_copy.update({
					'post_type_slug': slugify( post_type, '-' ),
					'post_type_name': post_type,
					'plugin_file': plugin_classname( post_type ),
					'plugin_class': plugin_classname( post_type ),
				})
				config_copy.update( dict( (x, True) for x in flags ) )
				templates.append( ( 'include/__plugin_namespace__/PostType/__plugin_file__.php', config_copy ) );

		admin_settings_classes = [];
		
		if self.config['settings']:

			flags = self.config['settings'][1]

			templates.append( ( 'include/__plugin_namespace__/Settings/Settings.php', config ) );

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

				templates.append( ( 'include/__plugin_namespace__/Settings/__plugin_file__.php', config_copy ) );
				
				admin_settings_classes.append( classname )
					
#			templates.append( ( 'include/__plugin_namespace__/Settings/Settings.php', config_copy ) );
#			templates.append( ( 'include/__plugin_namespace__/Settings/__settings_file__.php', config_copy ) );
			# settings_section: 
			#			@section: general | writing | reading | discussion | media | permalink
			#			@page: {{plugin_slug}}_options
			# 
			# settings_class = plugin_file
			#			@section: ucword($section) + 'Settings'
			#			@page: {{plugin_slug}} + 'SettingsPage'
			# is_page = ! is_section
			# is_section = ! is_page



		if self.config['shortcode']:
			if self.config['shortcode'][0]:
				templates.append( ( 'include/__plugin_namespace__/Shortcode/Shortcode.php', self.config ) );
				templates.append( ( 'include/__plugin_namespace__/Admin/Mce/Mce.php', config_copy ) );

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
				templates.append( ( 'include/__plugin_namespace__/Shortcode/__plugin_file__.php', config_copy ) );

				if 'mce' in flags:
					# add mce templates
					templates.append( ( 'include/__plugin_namespace__/Shortcode/Mce/__plugin_file__.php', config_copy ) );
					templates.append( ( 'js/admin/mce/__plugin_asset__-shortcode.js', config_copy ) );
					templates.append( ( 'css/admin/mce/__plugin_asset__-shortcode.css', config_copy ) );
					templates.append( ( 'css/admin/mce/__plugin_asset__-shortcode-mce.css', config_copy ) );
					templates.append( ( 'scss/admin/mce/__plugin_asset__-shortcode.scss', config_copy ) );
					templates.append( ( 'scss/admin/mce/__plugin_asset__-shortcode-mce.scss', config_copy ) );
					if self.config['gulp']:
						gulp_scss.append( pystache.render( 'admin/mce/{{plugin_asset}}-shortcode', config_copy ) )
						gulp_scss.append( pystache.render( 'admin/mce/{{plugin_asset}}-shortcode-mce', config_copy ) )


		if self.config['widget']:
			if self.config['widget'][0]:
				templates.append( ( 'include/__plugin_namespace__/Widget/Widgets.php', self.config ) );

			for widget,flags in self.config['widget'][0]:
				config_copy = self.config.copy()
				
				config_copy.update({
					'widget_slug': slugify( widget, '-' ),
					'widget_name': widget.title(),
					'plugin_file': plugin_classname( widget ),
					'plugin_class': plugin_classname( widget ),
				})
				templates.append( ( 'include/__plugin_namespace__/Widget/__plugin_file__.php', config_copy ) );

		config_copy = self.config.copy()
		config_copy.update({
			'settings_classes'	: admin_settings_classes,
		})

		templates.append( ( 'index.php', config_copy ) )

		if self.config['git']:
			templates.append( ( 'README.md', self.config ) )
			templates.append( ( '.gitignore', self.config ) )

		if self.config['gulp']:
			gulp_config = self.config.copy()
			gulp_config['scss'] = gulp_scss
			templates.append( ( 'gulpfile.js', gulp_config ) )


		self.process_templates(templates);
		
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

		if self.config['gulp']:
			print 'Installing npm dependencies'
			subprocess.call(["npm","install"])

			print 'cd into `%s`, run `gulp` and have fun coding!' % ( self.config['wp_plugin_slug'] )


		return ''

	def process_templates(self,templates):
		for template, template_config in templates:
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
                        Add an admin class. If admin_page, settings or settings_page is
                        selected, the class will be generated implicitly. Add +css and/or +js
                        to enqueue css / js in the entire wp admin.

        admin_page[+css][+js]
                        Add a standalone admin page

        admin_page[:a_page[+css][+js]][:a_page:...]...
                        Add submenu page to admin. 
                        `a_page` can be any of
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
                        With `+css` and `+js` appended to the page slug CSS and JS will 
                        also be enqueued on the given page.

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
                        register post type. +caps will register post type's caabilities

        widget:'Widget Name'[:'Another Widget']
                        Register one or more Widgets

        git             Inits a git repository

        gulp            Use gulp
        --force         Override existing plugin
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
