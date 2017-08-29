Plugin Scaffold
===============

Create a basic Wordpress plugin from the command line.

Usage:

```
$ cd /wordpress/wp-content/plugins
$ python /path/to/plugin.py "Plugin Name" [options]
```

# Options: #

```
    core[+css][+js]
              Add +css and/or +js to enqueue frontend css / js
    admin[+css][+js]
              Add an admin class. Add +css and/or +js to enqueue css / js 
              in the entire wp admin.

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
              or you can use a custom page slug.

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
              register post type. +caps will register post type's caabilities

    widget:'Widget Name'[:'Another Widget']
              Register one or more Widgets

    git       Inits a git repository

    gulp      Use gulp
    --force   Override existing plugin
```


# Make plugin.py available from everywhere #
```
$ mkdir ~/.scripts
$ cd ~/.scripts
$ git clone git@github.com:mcguffin/wp-plugin-scaffold.git
$ ln -s ./wp-plugin-scaffold/plugin.py ./wp-plugin
```
Finally add `~/.scripts/` to the PATH variable in your `~/.bash_profile`

