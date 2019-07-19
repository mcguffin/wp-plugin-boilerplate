#!/usr/bin/env node
const colors = require('colors');
const Plugin = require('./lib/plugin.js');
const {Template,TemplateExistsError} = require('./lib/template.js');
const prompts = require('prompts');
const fs = require('fs');

const [ , , ...args ] = process.argv;

const usage = `Usage \`wp-plugin [components]\`

# Components

component syntax: <component>[+<component-flag>+<component-flag>][:<slug>[+<flag>+<flag>]][:<slug>+<flag,..][:...]

## Available Components

### admin
Add admin pages. Slug refers to the parent page in the admin menu.
	slug: dashboard|posts|media|links|pages|comments|theme|plugins|users|management|options
	component-flags: - none -
	flags: css, js

### ajax
Include Ajax-Action base class.
	slug: - none -
	component-flags: - none -
	flags: - none -

### block
Register a block type.
	slug: Custom, The Block name in kebab-case
	component-flags: - none -
	flags: - none -

### cli
Add a WP-CLI-Command
	slug: Custom, The ClI-Command in kebab-case
	component-flags: - none -
	flags: - none -

### compat
Add compatibility to other plugins.
	slug: acf|polylang|regenerate-thumbnail|wpmu
	component-flags: - none -
	flags: - none -

### core
Configure core classes to include js and/or css in the frontend.
	slug: - none -
	component-flags: css, js
	flags: - none -

### cron
Add cronjob base classes
	slug: - none -
	component-flags: - none -
	flags: - none -

### model
Add database table class. Use wpmu flag if the table should be global in a network.
	slug: The model name in kebab-case
	component-flags: - none -
	flags: wpmu

### network-admin
Add a network admin page. The menu-flag will add the page to the network admin settings menu. This component implicates compat:wpmu.
	slug: network admin action
	component-flags: css, js
	flags: menu

### network-settings
Add settings setion to network settings. This component implicates compat:wpmu.
	slug: network admin action
	component-flags: css, js
	flags: menu

### posttype
Register a posttype
	slug: the posttype name
	component-flags: - none -
	flags: caps

### rest
Add a rest endpoint
	slug: rest endpoint in kebab-case
	component-flags: - none -
	flags: - none -

### settings
Add plugin settings. Slug can be either
	slug: general|writing|reading|discussion|media|permalink or custom settings page
	component-flags: - none -
	flags: css, js

### shortcode
Register a shortcode. The css and js flags will include assets in the frontend. The mce flag will add a button to tinyMCE.
	slug: the shortcode in kebab-case
	component-flags: - none -
	flags: css, js, mce

### taxonomy
Register a taxonomy
	slug: the taxonomy slug in kebab-case
	component-flags: - none -
	flags: - none -

### widget
Register a widget.
	slug: the widget name in kebab-case
	component-flags: - none -
	flags: js, css
`;

// input: slug+flag+flag
const parse_flags = s => {
	let flags;
	[ slug, ...flags ] = s.split('+')
	return { slug, flags };
}

const plugin_collection = [];
let current_task;
// show help
if ( args.indexOf('--help') !== -1 ) {
	console.log(usage);
	process.exit();
}

const parse_args = () => {
	let ret = args.slice(0);
	// core is mandatory
	return ret.filter( arg => arg.indexOf('--') !== 0 ).map( arg => {
		let slug, flags, comp, components;

		[ comp, ...components ] = arg.split(':');
		comp = parse_flags(comp)
		components = components || [];
		components = components.map( parse_flags );
		return { slug: comp.slug, flags: comp.flags, components }
	} );
}

Template.srcdir = require('./package.json').templateDir;


(async () => {
	const plugin = new Plugin();
	let package, currdir;
	plugin.force = args.indexOf('--force') !== -1;
	try {
		// Existing plugin
		//*
		plugin.root_package = require( process.cwd() + '/package.json');
		plugin.package = plugin.root_package.wpPlugin;
		plugin.destdir = process.cwd();
		/*/
		plugin.package = { name:'WP Async Foobar Extruder'}
		plugin.guessNames();
		//*/
	} catch ( e ) {
		// test if in wp directory
		currdir = process.cwd();

		while ( currdir != '/' ) {
			if ( fs.existsSync(currdir+'/wp-load.php') ) {
				break;
			}
			currdir = fs.realpathSync( currdir + '/..' );
		}
		if ( currdir === '/' ) {
			throw( 'Not in a wordpress directory' )
		}
		try {
			// set cwd to plugins dir
			currdir = fs.realpathSync( currdir + '/wp-content/plugins' )
			process.chdir( currdir );
		} catch(e2) {
			throw(e2)
		}
	}

	parse_args().forEach( c => plugin.addComponent( ...Object.values(c) ) )
	try {
		await plugin.setup(); // prompt for setup
	} catch ( err ) {
		console.error('Error:'.red,err.toString().white)
		throw(err)
		process.exit();
	}
	await plugin.generate(); // make code, store in location
	await plugin.finish(); // run post-generate scripts like git init

})();
