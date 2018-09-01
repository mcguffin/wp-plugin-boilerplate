{{plugin_name}}
===============

#### Developer info here. ####


Installation
------------

### Production (Stand-Alone)
 - Head over to [releases](../../releases)
 - Download '{{wp_plugin_slug}}.zip'
 - Upload and activate it like any other WordPress plugin
 - AutoUpdate will run as long as the plugin is active

### Production (using Github Updater – recommended for Multisite)
 - Install [Andy Fragen's GitHub Updater](https://github.com/afragen/github-updater) first.
 - In WP Admin go to Settings / GitHub Updater / Install Plugin. Enter `{{modules.git.github_repo}}` as a Plugin-URI.

### Development
 - cd into your plugin directory
 - $ `git clone git@github.com:{{modules.git.github_repo}}.git`
 - $ `cd {{wp_plugin_slug}}`{{#modules.gulp}}
 - $ `npm install`
 - $ `gulp`{{/modules.gulp}}
