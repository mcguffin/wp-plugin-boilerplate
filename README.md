WP Plugin Boilerplate
=====================

Create WordPress Plugins from the command line.


Install
-------
```
$ mkdir ~/.scripts
$ cd ~/.scripts
$ git clone git@github.com:mcguffin/wp-plugin-boilerplate.git
$ ln -s ./wp-plugin-boilerplate/plugin.py ./wp-plugin
```
Finally add `~/.scripts/` to the PATH variable in your `~/.bash_profile`


CLI usage
---------

Inside `wp-content/plugins/`:  
$ `wp-plugin "Plugin Name" <features>`  
*Will create a plugin with given features*

Inside a plugin directory  
$ `wp-plugin <features>`  
*Will add selected features to plugin_name*

Features syntax:
----------------
    <feature>:<feature_argument>+<flag>+<another_flag>+....:<next_feature_argument>...
    <feature>+<flag>+flag2

Examples:
---------
#### Plugin with two widgets and frontend CSS + JS
    wp-plugin "Fancy Plugin" core+css+js widget:"Fancy Widget"+css:"Even Cooler Widget"+css+js git gulp --force

#### With Everything
    wp-plugin "Very Fancy Plugin" \
	    admin+css+js settings:reading+css+js:"Plugin Settings"+css+js \ admin_page:tools+css+js \
		autoupdate \
		cron widget:"A Widget" \
		shortcode:"A Shortcode"+mce \
		taxonomy \
		posttype:"Thingy Posts"+caps \
		model:things \
		gulp \
		git \
		core+css+js \
		ajax


Available features
------------------
```
admin_page
  Add submenu page to admin.
  Takes multiple arguments.
    argument: dashboard|posts|media|links|pages|comments|theme|plugins|users|management|tools
              Or a freely choosen Name for the admin page
    flags:    js     Enqueue js
	          css    Enqueue css
			  force  override existing classes

admin
  Add an admin class.
  Takes no arguments.
    flags:    js     Enqueue js
              css    Enqueue css
			  force  override existing classes

ajax
  Add Ajax handler class.
  Takes no arguments.
    flags:    force  override existing classes

autoupdate
  Enable Auto-Update from github.
  You will have to create a Release, to trigger AutoUpdate.
  Takes no arguments.
    flags:    force  override existing classes

core
  Load frontend assets.
    flags:    js     Enqueue js
  			  css    Enqueue css
  			  force  override existing classes

compat
  Add a compatibility class for use with other plugins
  Takes no arguments.
    flags:    force  override existing classes

git
  Init a get repo
  Takes no arguments.
    flags:    force  override existing files (like .gitignore, ...)

gulp
  npm install
  Takes no arguments.
    flags:    force  override existing files

model
  Add a datablase table class.
  Takes multiple arguments.
    argument: a table name for the model.
	flags:    force  override existing files

posttype
  Add Post types
  Takes multiple arguments.
    argument: Post type name
    flags:    caps   Register custom post type capabilities
	flags:    force  override existing files

settings
  Add a settings page
  Takes multiple arguments.
    argument: general|writing|reading|discussion|media|permalink
              Or anything else for custom settings page
    flags:    js     Enqueue js
              css    Enqueue css
			  force  override existing classes

shortcode
  Register a shortcode.
  Takes multiple arguments.
    argument: The Shortcode.
    flags:    mce    Add Button to tinyMCE.
	          force  override existing classes

taxonomy
  Add Taxonomy
  Takes multiple arguments.
    argument: Taxonomy name
	flags:    force  override existing files

widget
  Add Widgets
  Takes multiple arguments.
    argument: Widget name
    flags:    js     Enqueue js
              css    Enqueue css
			  force  override existing classes
```
