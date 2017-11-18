WP Plugin Boilerplate
=====================

CLI usage
---------

From anywhere:
$ `wp-plugin "Plugin Name" features`
Will create a plugin with given features

Inside a plugin directory
$ `wp-plugin features`
Will add selected features to plugin_name

Features syntax:
----------------
    <feature>:<feature_argument>+<flag>+<another_flag>+....:<next_feature_argument>...
    <feature>+<flag>+flag2

Example:
---------
    wp-plugin "Fancy Plugin" core+css+js widget:"Fancy Widget"+css:"Even Cooler Widget"+css+js git gulp --force


Available features
------------------
```
admin_page
  Add submenu page to admin.
  Takes multiple arguments.
    argument: dashboard|posts|media|links|pages|comments|theme|plugins|users|management|tools
              Or a freely choosen Name for the admin page
    flags:    js  Enqueue js
	          css Enqueue css

admin
  Add an admin class.
  Takes no arguments.
    flags:    js  Enqueue js
              css Enqueue css

ajax
  Add Ajax handler class.
  Takes no arguments.

autoupdate
  Enable Auto-Update from github.
  You will have to create a Release, to trigger AutoUpdate.
  Takes no arguments.

core
  Load frontend assets.
    flags:    js  Enqueue js
              css Enqueue css

compat
  Add a compatibility class for use with other plugins
  Takes no arguments.

git
  Init a get repo
  Takes no arguments.

gulp
  npm install
  Takes no arguments.

model
  Add a datablase table class.
  Takes multiple arguments.
    argument: a table name for the model.

posttype
  Add Post types
  Takes multiple arguments.
    argument: Post type name
    flags:    caps Register custom post type capabilities

settings
  Add a settings page
  Takes multiple arguments.
    argument: general|writing|reading|discussion|media|permalink
              Or anything else for custom settings page
    flags:    js  Enqueue js
              css Enqueue css

shortcode
  Register a shortcode.
  Takes multiple arguments.
    argument: The Shortcode.
    flags:    mce Add Button to tinyMCE.

taxonomy
  Add Taxonomy
  Takes multiple arguments.
    argument: Taxonomy name

widget
  Add Widgets
  Takes multiple arguments.
    argument: Widget name
    flags:    js  Enqueue js
              css Enqueue css
```



# Make plugin.py available from everywhere #
```
$ mkdir ~/.scripts
$ cd ~/.scripts
$ git clone git@github.com:mcguffin/wp-plugin-boilerplate.git
$ ln -s ./wp-plugin-boilerplate/plugin.py ./wp-plugin
```
Finally add `~/.scripts/` to the PATH variable in your `~/.bash_profile`
