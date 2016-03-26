#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys, os, pystache, re, pwd, pprint, shutil,codecs,subprocess
from datetime import date
from pprint import pprint

class wp_plugin:
	defaults = {
		'plugin_name' : '',
		'plugin_slug' : '',
		'wp_plugin_slug' : '',
		'plugin_class_name' : '',
		'plugin_author' : '',
		'plugin_author_uri' : '',
		'frontend_css' : False,
		'frontend_js' : False,
		'admin_css' : False,
		'admin_js' : False,
		'admin_page' : False,
		'admin_page_css' : False,
		'admin_page_js' : False,
		'admin_page_hook' : False,
		'settings_css' : False,
		'settings_js' : False,
		'admin' : False,
		'settings' : False,
		'settings_section' : False,
		'settings_page' : False,
		'backend' : False,
		'shortcodes':False,
		'widget':False,
		'post_type':False,
		'post_type_slug':False,
		'post_type_with_caps':False,
		'post_type_with_caps_slug':False,
		'github_user':False,
		'git':False
	}
	_private_defaults = {
		'settings_assets' : False,
		'admin_assets' : False,
		'admin_pages' : False,
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
	
	def __init__(self,config):
		self.config = self.process_config(config)
		self.plugin_dir = os.getcwd()+'/'+slugify(self.config['plugin_name'],'-')
		pass
		
	def process_config(self,config):
		# set names
		config['plugin_slug'] 		= plugin_slug(config['plugin_name'])
		config['wp_plugin_slug']	= slugify(config['plugin_name'],'-')
		config['plugin_class_name'] = plugin_classname(config['plugin_name'])
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

		# default is settings section
		if config['settings'] and not config['settings_page'] and not config['settings_section']:
			config['settings_section'] = True

		config['settings'] 			= config['settings_page'] or config['settings_section']
		config['settings_section'] 	= not config['settings_page']
		config['settings_assets'] 	= config['settings_css'] or config['settings_js']
		config['admin_assets'] 		= config['admin_css'] or config['admin_js']

		config['admin_page'] = config['admin_pages'] = config['admin_page'] or config['admin_page_css'] or config['admin_page_js']
		
		if isinstance(config['admin_page'],list) :
			admin_pages					= config['admin_page']
			if 'all' in admin_pages:
				config['admin_pages']	= self.allowed_admin_pages
			else:
				# replace tools alias
				admin_pages				= [x if (x != 'tools') else 'management' for x in admin_pages]
				# unique list, containing only alloewd items
				config['admin_pages']	= []
				[config['admin_pages'].append(x) for x in admin_pages if x in self.allowed_admin_pages and x not in config['admin_pages'] ]

			config['admin_page']	= True
	
		config['admin_page_hook']	= config['admin_page'] or config['admin_pages']
		
		config['admin']				= config['admin'] or config['admin_page']

		config['backend'] 			= config['settings'] or config['admin']
		
		if config['shortcodes'] and config['shortcodes'] == True:
			config['shortcodes'] == False
			print 'Could not generate shortcode.'
			print 'shortcode usage is: shortcode:my_shortcode'

		if config['post_type'] and config['post_type'] == True:
			config['post_type'] == False
			print 'Could not generate post_type.'
			print 'post_type usage is: post_type:"Post Type Name"'

		if config['post_type_with_caps'] and config['post_type_with_caps'] == True:
			config['post_type_with_caps'] == False
			print 'Could not generate post_type_with_caps.'
			print 'post_type_with_caps usage is: post_type_with_caps:"Post Type Name"'
		
		if config['frontend_js'] or config['frontend_css']:
			config['frontend_assets'] = true
		
		if config['post_type']:
			config['post_type'] = map(lambda post_type: {'post_type_slug':slugify(post_type),'post_type_name':post_type}, config['post_type'])

		if config['post_type_with_caps']:
			config['post_type_with_caps'] = map(lambda post_type: {'post_type_slug':slugify(post_type),'post_type_name':post_type,'capabilities':True}, config['post_type_with_caps'])
			config['has_post_type_caps'] = True
		
		if config['post_type']:
			config['post_type'] = config['post_type'] + config['post_type_with_caps']
		else :
			config['post_type'] = config['post_type_with_caps']
		config['has_post_types'] = bool(config['post_type'])
		return config
	
	def make(self):
		# make plugin dir
		try:
			os.mkdir(self.plugin_dir)
		except OSError as e:
			return e

		templates = ['index.php','readme.txt','README.md'] # ,'languages/__wp_plugin_slug__.pot'
		
		templates.append('languages/__wp_plugin_slug__.pot')

		if self.config['frontend_css']:
			templates.append('css/__slug__.css')
		if self.config['frontend_js']:
			templates.append('js/__slug__.js')

		if self.config['settings_css']:
			templates.append('css/__slug__-settings.css')
		if self.config['settings_js']:
			templates.append('js/__slug__-settings.js')

		if self.config['admin_css']:
			templates.append('css/__slug__-admin.css')
		if self.config['admin_js']:
			templates.append('js/__slug__-admin.js')

		if self.config['admin_page_css']:
			templates.append('css/__slug__-admin-page.css')
		if self.config['admin_page_js']:
			templates.append('js/__slug__-admin-page.js')


		if self.config['admin']:
			templates.append('include/class-__class__Admin.php')
			
		if self.config['widget']:
			templates.append('include/class-__class___Widget.php')
			
		if self.config['settings']:
			templates.append('include/class-__class__Settings.php')

		if self.config['git']:
			templates.append('README.md')
			templates.append('.gitignore')
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
				print 'Git repository created. Now go to github.com and create a repository named `%s`' % ( self.config['wp_plugin_slug'] )
				print 'Finally come back and type `git push -u origin master` here.'

		return ''

	def process_templates(self,templates):
		for template in templates:
			content = pystache.render( self._read_template(template),self.config)
			self._write_plugin_file(template,content)
	

	def _read_template(self,template):
		template_path = os.path.dirname(os.path.realpath(__file__))+'/templates/'+template
		return self._read_file_contents( template_path )

	def _write_plugin_file( self , template , contents ):
		template_filename = template.replace('__slug__',self.config['plugin_slug']).replace('__class__',self.config['plugin_class_name']).replace('__wp_plugin_slug__',self.config['wp_plugin_slug']);
		print template,template_filename
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
	return slugify(rm_wp(plugin_name))

def plugin_classname(plugin_name):
	return ''.join(x for x in rm_wp(plugin_name).title() if not x.isspace())


usage = '''
usage ./plugin.py 'Plugin Name' options
    options can be any of:
        --force         Override existing plugin
        admin_css       Enqueue css globally in admin
        admin_js        Enqueue js globally in admin
        frontend_css    Enqueue css in frontend
        frontend_js     Enqueue js in frontend
        settings_css    Enqueue css on settings page (only if settings is present)
        settings_js     Enqueue js on settings page (only if settings is present)

        admin           Create an admin class
        admin_page      Add an admin page (will create admin also)
        admin_page:a_page[:a_page]
                        Add submenu page to admin. a_page can be any of
                        Page can be any of
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
        admin_page_js   Add js to admin page (adds admin_page also)
        admin_page_css  Add css to admin page (adds admin_page also)

        settings | settings_section
                        Create Settings section
        settings_page
                        Create Settings page

        shortcodes:a_shortcode[:another_shortcode[:..]]
                        Add shortcode handler(s)
		post_type:'Post Type name'
						register post type
		post_type_with_caps:'Post Type name'
						register post type having its own capabilities
        widget          Register a Widget
        git             Inits a git repository
'''


defaults = config = wp_plugin.defaults

try:
	config['plugin_name']	= sys.argv[1]
except IndexError as e:
	print usage
	sys.exit(0)

config['shell_args']		= "\"%s\" %s" % ( sys.argv[1] , ' '.join(sys.argv[2:]) )

for arg in sys.argv[2:]:
	conf = arg.split(':')
	param = True
	if len(conf) > 1:
		param = conf[1:]
		conf = conf[0]
	elif len(conf) == 1:
		conf = conf[0]
	if conf in defaults.keys():
		config[conf] = param

if "all" in sys.argv[2:]:
	for arg in config.keys():
		if config[arg] == False:
			config[arg] = True

print "Generating Plugin:", config['plugin_name']
maker = wp_plugin(config)
if '--force' in sys.argv and os.path.exists(maker.plugin_dir):
	shutil.rmtree( maker.plugin_dir )
result = maker.make()

if isinstance(result, Exception):
	print 'Plugin exists:',result
	print 'use --force to override existing plugin'
