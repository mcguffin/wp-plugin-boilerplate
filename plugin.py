#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, codecs, pwd, shutil, json#, pystache, re, subprocess, string
from datetime import date
from pprint import pprint

from wp_plugin import plugin_slug, plugin_classname, slugify, usage
import wp_plugin.plugin as p


if len(sys.argv) == 1 or sys.argv[1] == '?':
	print(usage)
	sys.exit(0)

def get_flags( param ):
	paramlist = param.split('+')
	return paramlist[0],paramlist[1:]


def parse_arg(arg):
	flags = True
	parts = arg.split(':')
	# conf = cmd:arg+js+css:arg+css:...
	# OR conf = cmd+js+css
	mod,flags = get_flags( parts[0] )

	conf = {}
	for flag in flags:
		conf[flag] = True

	if len(parts) == 1:
		return mod,{}

	for part in parts[1:]:
		prt,flags = get_flags( part )
		conf[prt] = {}
		for flag in flags:
			conf[prt][flag] = True

	return mod, conf

def parse_args(args):
	config = {}
	for arg in args:
		if arg[:2] == '--':
			return
		mod, conf = parse_arg(arg)
		config[mod] = conf

	return config


source_dir = os.path.dirname(os.path.realpath(__file__))

first,conf = parse_arg(sys.argv[1])

if first in p.factory.factory.modules:
	# first arg is a module
	plugin_name = False
	module_argv = sys.argv[1:]
	plugin_dir = os.getcwd()
else:
	# first arg is a plugin name
	plugin_name = sys.argv[1]
	module_argv = sys.argv[2:]
	plugin_dir = os.getcwd() + '/' + slugify( plugin_name, '-' )



try:
	# update existing
	f = codecs.open( plugin_dir + '/' + 'wp-plugin-boilerplate.json', 'rb', encoding = 'utf-8' )
	config = json.loads(f.read())
	f.close()
	plugin_name = config['plugin_name']
	module_args = parse_args( module_argv )

	# add module args
	for mod_key,module in config['modules'].items():
		if mod_key in module_args:
			module.update(module_args[mod_key])

	for mod_key,module in module_args.items():
		if mod_key not in config['modules']:
			config['modules'][mod_key] = module

	print( "Update existsing plugin:", plugin_name )
except IOError as a:
	if plugin_name:
		# create new
		config = {
			'plugin_name' 		: plugin_name,
			'plugin_slug' 		: plugin_slug( plugin_name ),
			'wp_plugin_slug'	: slugify( plugin_name, '-' ),
			'plugin_namespace'	: plugin_classname( plugin_name ),
			'plugin_author'		: pwd.getpwuid( os.getuid() ).pw_gecos,
			'plugin_author_uri'	: '',
			'modules'			: parse_args( module_argv ),
			'this_year'			: date.today().year
		}
		print( "Create new plugin:", plugin_name )

	else:
		print('`wp-plugin-boilerplate.json` does not exist in cwd')
		sys.exit(1)


plug = p.plugin()
plug.config( config, plugin_dir )
plug.set_override( '--force' in sys.argv )
plug.pre_process()
plug.process()
plug.post_process()

sys.exit(0)



try:
	# existsing plugin
	f = codecs.open('wp-plugin-boilerplate.json','rb',encoding='utf-8')

	config = json.loads(f.read())

	f.close()

	modules = parse_args( sys.argv[1:] )
	config['modules'].update(modules)

	plugin_dir = os.getcwd()

	print( "Found plugin:", config['plugin_name'])

except IOError as a:
	# create plugin
	plugin_name = sys.argv[1]
	plugin_dir = os.getcwd() + '/' + slugify( plugin_name, '-' )
	author = pwd.getpwuid( os.getuid() ).pw_gecos

	# new plugin
	config = {
		'plugin_name' 		: plugin_name,
		'plugin_slug' 		: plugin_slug( plugin_name ),
		'wp_plugin_slug'	: slugify( plugin_name, '-' ),
		'plugin_namespace'	: plugin_classname( plugin_name ),
		'plugin_author'		: author,
		'plugin_author_uri'	: '',
		'modules'			: parse_args( sys.argv[2:] ),
		'this_year'			: date.today().year
	}

	print( "Create plugin:", config['plugin_name'])



#
# defaults = config = wp_plugin.defaults
#
# try:
# 	config['plugin_name']	= sys.argv[1]
# except IndexError as e:
# 	print usage
# 	sys.exit(0)
#
# config['shell_args']		= "\"%s\" %s" % ( sys.argv[1] , ' '.join(sys.argv[2:]) )
#
#
# for arg in sys.argv[2:]:
# 	param = []
# 	flags = True
# 	conf  = arg.split(':')
# 	# conf = cmd, param+js+css, param+css, ...
# 	# OR conf = cmd+js+css
# 	if len(conf) > 1:
# 		param = conf[1:]
# 	conf = conf[0]
# 	# conf = cmd
# 	# OR conf = cmd+js+css
# 	conf,flags = getflags( conf )
# 	param = [ getflags( par ) for par in param ]
#
# 	if conf in defaults.keys():
# 		config[conf] = param,flags
# #pprint(config)
#
# print "Generating Plugin:", config['plugin_name']
# maker = wp_plugin(config)
#
# if '--force' in sys.argv and os.path.exists(maker.plugin_dir):
# 	print "remove existing plugin"
# 	shutil.rmtree( maker.plugin_dir )
#
# result = maker.make()
#
# if isinstance(result, Exception):
# 	print 'Plugin exists:',result
# 	print 'use --force to override existing plugin'
