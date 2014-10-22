Plugin Scaffold
===============

Create a basic Wordpress plugin from the command line.

Usage:
```
$ cd /wordpress/wp-content/plugins
$ python /path/to/plugin.py "Plugin Name" [options]
```
# options: #
- `--force`         Override existing plugin
- `admin_css`       Enqueue css globally in admin
- `admin_js`        Enqueue js globally in admin
- `frontend_css`    Enqueue css in frontend
- `frontend_js`     Enqueue js in frontend
- `settings_css`    Enqueue css on settings page (only if settings is present)
- `settings_js`     Enqueue js on settings page (only if settings is present)
- `admin` 			Create an admin class
- `settings` | `settings_section` Create Settings section
- `settings_page`	Create Settings page
- `shortcodes:a_shortcode[:another_shortcode[:..]]` Add shortcode handler(s)
- `post_type:"Post Type name"` Register post type.
- `post_type_with_caps:"Post Type name"` Will register a post type having its own capability type.
- `widget`			Register a Widget

# Make plugin.py available from everywhere #
```
$ mkdir ~/.scripts
$ cd ~/.scripts
$ git clone git@github.com:mcguffin/wp-plugin-scaffold.git
$ ln -s ./wp-plugin-scaffold/plugin.py ./wp-plugin
```
Finally add `~/.scripts/` to the PATH variable in your `~/.bash_profile`

Todo:
- add Autoload
- add admin page
