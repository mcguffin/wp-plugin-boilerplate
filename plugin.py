#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, os, codecs, pwd, shutil#, pystache, re, subprocess, json, string
from datetime import date

from wp_plugin import getflags, plugin_slug, plugin_classname, slugify, usage
import wp_plugin.plugin as p


if len(sys.argv) == 1 or sys.argv[1] == '?':
	print(usage)
	sys.exit(0)

def parse_argv(args):
	config = {}
	for arg in args:
		param = []
		flags = True
		parts = arg.split(':')
		if arg[:2] == '--':
			continue
		# conf = cmd, param+js+css, param+css, ...
		# OR conf = cmd+js+css
		mod,flags = getflags( parts[0] )

		config[mod] = {}
		for flag in flags:
			config[mod][flag] = True

		if len(parts) == 1:
			continue

		for part in parts[1:]:
			prt,flags = getflags( part )
			config[mod][prt] = {}
			for flag in flags:
				config[mod][prt][flag] = True
	return config


source_dir = os.path.dirname(os.path.realpath(__file__))

try:
	# existsing plugin
	f = codecs.open('wp-plugin-boilerplate.json','rb',encoding='utf-8')
	config = json.loads(f.read())
	f.close()
	modules = parse_argv( sys.argv[1:] )
	plugin_dir = os.getcwd()
	do_create = False
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
		'modules'			: parse_argv( sys.argv[2:] ),
		'this_year'			: date.today().year
	}

	do_create = True

	# rm if force
	if '--force' in sys.argv and os.path.exists( plugin_dir ):
		print( "remove existing plugin")
		shutil.rmtree( plugin_dir )

	print( "Create plugin:", config['plugin_name'])

plug = p.plugin()
plug.config( config, plugin_dir )

# for m,mconf in modules.items():
# 	print ("Adding module", m )
# 	plug.add_module( m, mconf )
#

plug.pre_process()

plug.process()

plug.post_process()



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
