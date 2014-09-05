#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys, os, pystache, re, pwd, pprint, shutil,codecs
from datetime import date
from pprint import pprint

class wp_plugin:
	defaults = {
		'plugin_name' : '',
		'plugin_slug' : '',
		'plugin_class_name' : '',
		'plugin_author' : '',
		'plugin_author_uri' : '',
		'frontend_css' : False,
		'frontend_js' : False,
		'admin_css' : False,
		'admin_js' : False,
		'settings_css' : False,
		'settings_js' : False,
		'admin' : False,
		'settings' : False,
		'settings_section' : False,
		'settings_page' : False,
		'backend' : False,
		'shortcodes':False,
		'widget':False
	}
	_private_defaults = {
		'settings_assets' : False,
		'admin_assets' : False
	}
	
	def __init__(self,config):
		self.config = self.process_config(config)
		self.plugin_dir = os.getcwd()+'/'+slugify(self.config['plugin_name'],'-')
		pass
		
	def process_config(self,config):
		# set names
		config['plugin_slug'] 		= plugin_slug(config['plugin_name'])
		config['plugin_class_name'] = plugin_classname(config['plugin_name'])
		author 						= pwd.getpwuid( os.getuid() ).pw_gecos

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

		config['backend'] 			= config['settings'] or config['admin']

		return config
	
	def make(self):
		# make plugin dir
		try:
			os.mkdir(self.plugin_dir)
		except OSError as e:
			return e

		templates = ['index.php','readme.txt']
		
		if ( self.config['frontend_css'] ):
			templates.append('css/__slug__.css')
		if ( self.config['frontend_js'] ):
			templates.append('js/__slug__.js')

		if ( self.config['settings_css'] ):
			templates.append('css/__slug__-settings.css')
		if ( self.config['settings_js'] ):
			templates.append('js/__slug__-settings.js')

		if ( self.config['admin_css'] ):
			templates.append('css/__slug__-admin.css')
		if ( self.config['admin_js'] ):
			templates.append('js/__slug__-admin.js')


		if (self.config['admin']):
			templates.append('include/class-__class__Admin.php')
			
		if (self.config['widget']):
			templates.append('include/class-__class___Widget.php')
			
		if (self.config['settings']):
			templates.append('include/class-__class__Settings.php')
			templates.append('uninstall.php')

		if (self.config['shortcodes'] and self.config['shortcodes'] == True):
			self.config['shortcodes'] == False
			print 'Could not generate shortcode.'
			print 'shortcode usage is: shortcode:my_shortcode'

		self.process_templates(templates);
		return ''

	def process_templates(self,templates):
		for template in templates:
			content = pystache.render( self._read_template(template),self.config)
			self._write_plugin_file(template,content)
	

	def _read_template(self,template):
		template_path = os.path.dirname(__file__)+'/templates/'+template
		return self._read_file_contents( template_path )

	def _write_plugin_file( self , template , contents ):
		template_filename = template.replace('__slug__',self.config['plugin_slug']).replace('__class__',self.config['plugin_class_name']);
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
	return re.sub(r'(?i)^(WP|WordPress\s?)','',str).strip()

def slugify(plugin_name,separator='_'):
	return re.sub(r'\s',separator,plugin_name.strip()).lower()

def plugin_slug(plugin_name):
	return slugify(rm_wp(plugin_name))

def plugin_classname(plugin_name):
	return ''.join(x for x in rm_wp(plugin_name).title() if not x.isspace())


usage = '''
usage ./make.py 'Plugin Name' options
    options can be any of:
        --force         Override existing plugin
        admin_css       Enqueue css globally in admin
        admin_js        Enqueue js globally in admin
        frontend_css    Enqueue css in frontend
        frontend_js     Enqueue js in frontend
        settings_css    Enqueue css on settings page (only if settings is present)
        settings_js     Enqueue js on settings page (only if settings is present)

        admin           Create an admin class
        settings | settings_section
                        Create Settings section
        settings_page
                        Create Settings page

        shortcodes:a_shortcode[:another_shortcode[:..]]
                        Add shortcode handler(s)

        widget          Register a Widget
'''


defaults = config = wp_plugin.defaults

try:
	config['plugin_name'] = sys.argv[1]
except IndexError as e:
	print usage
	exit()
	
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
