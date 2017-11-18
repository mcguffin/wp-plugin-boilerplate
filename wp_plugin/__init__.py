import re

__all__ = ['plugin','modules','file_template']

def getflags( param ):
	paramlist = param.split('+')
	return paramlist[0],paramlist[1:]

def rm_wp(str):
	return re.sub(r'(?i)^(WP|WordPress\s?)-?','',str).strip()

def slugify(plugin_name,separator='_'):
	return re.sub(r'\s',separator,plugin_name.strip()).lower()

def plugin_slug(plugin_name):
	return slugify(rm_wp(plugin_name),'_')

def plugin_classname(plugin_name):
	return ''.join(x for x in rm_wp(plugin_name).title() if x.isalnum())
