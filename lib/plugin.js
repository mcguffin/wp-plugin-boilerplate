const change_case = require('change-case');
const promts = require('prompts');
const exec = require('child_process');
const Template = require('./template.js');
const Components = require('./components/index.js');
const {doing} = require('./lib/doing.js');

const unwp = s => s.replace(/^(wp|wordpress)(\s|-)/i,'');
const wpize = s => s.replace(/^(wp|wordpress)(\s|-)/i,'WP$2');

class Plugin {

	constructor() {
		// names
		Template.plugin = this
		this.name = false;
		this.slug = false;
		this.prefix = false;
		this.textdomain = false;
		this.namespace = false;

		this.git_user = false;
		this.git_remote = false;
		this.author = false;
		this.author_uri = false;

		this.year = false;
		this._components = {
			core: new Components.core()
		}
	}

	async setup() {
		let data;
		const setProps = d => {
			Object.keys(d).forEach( k => this[k] = d[k] )
			this.guessProps()
		}
		const validName = name => !name.match(/^[a-z]/i) ? 'Must begin with a letter!' : true;
		const validSlug = name => !name.match(/^[a-z][a-z0-9_-]/i) ? 'Only letters numbers, dash or underscore. Must begin with a letter' : true;

		if ( this.name !== false ) {

			data = await promts([
				{
					type: 'text',
					name: 'name',
					message: 'Plugin name:',
					validate: validName
				}
			], { onCancel: process.exit });

			setProps(data)

			data = await promts([
				{
					type: 'text',
					name: 'slug',
					message: 'Plugin slug:',
					initial: this.slug,
					validate: validSlug
				},
				{
					type: 'text',
					name: 'prefix',
					message: 'Plugin prefix:',
					initial: this.prefix,
					validate: validSlug
				}
			], { onCancel: process.exit });

			this.textdomain = this.namspace = this.git_user = false;
			setProps(data)

			data = await promts([
				{
					type: 'text',
					name: 'textdomain',
					message: 'textdomain:',
					initial: this.textdomain,
					validate: validSlug
				},
				{
					type: 'text',
					name: 'namspace',
					message: 'PHP Namespace:',
					initial: this.namespace,
					validate: validSlug
				},
				{
					type: 'text',
					name: 'git_user',
					message: 'git user:',
					initial: this.git_user
				}
			], { onCancel: process.exit });

			this.git_remote = this.author = this.author_uri = false;
			setProps(data)

			data = await promts([
				{
					type: 'text',
					name: 'git_remote',
					message: 'Git remote URL:',
					initial: this.git_remote
				},
				{
					type: 'text',
					name: 'author',
					message: 'Author:',
					initial: this.author
				},
				{
					type: 'text',
					name: 'author_uri',
					message: 'Author URI:',
					initial: this.author_uri
				}
			], { onCancel: process.exit });

			setProps(data)

		}

		let c = Object.values(this._components);
		while ( c.length ) {
			await c.shift().setup();
		}

	}

	async generate() {
		let c = Object.values(this._components);
		while ( c.length ) {
			await c.shift().generate();
		}
	}

	async finish() {
		let c = Object.values(this._components);
		while ( c.length ) {
			await c.shift().finish();
		}
	}

	guessProps() {

		// names
		if ( this.slug === false ) {
			this.slug = change_case.paramCase( this.wp_short_name );
		}
		if ( this.prefix === false ) {
			this.prefix = change_case.paramCase( this.short_name )
		}
		if ( this.textdomain === false ) {
			this.textdomain = this.slug
		}
		if ( this.namespace === false ) {
			this.namespace = change_case.pascalCase( this.short_name );
		}

		// author
		if ( this.git_user === false ) {
			this.git_user = exec.execSync( 'git config user.name', { encoding: 'utf8' } ).trim();
		}
		if ( this.git_remote === false && this.git_user !== false ) {
			this.git_remote = `git@github.com:${this.git_user}/${this.slug}.git`;
		}
		if ( this.author === false && this.git_user !== false ) {
			this.author = this.git_user;
		}
		if ( this.author_uri === false && this.git_user !== false ) {
			this.author_uri = `https://github.com/${this.git_user}`;
		}
		if ( this.year === false ) {
			this.year = new Date().getFullYear();
		}
	}

	get short_name() {
		return unwp(this.name);
	}

	get wp_short_name() {
		return wpize(this.name);
	}


	// readonly
	get slug_upper() {
		return change_case.constantCase( this.slug )
	}

	get package() {
		return {
			name:		this.name,
			slug:		this.slug,
			prefix:		this.prefix,
			textdomain:	this.textdomain,
			namespace:	this.namespace,

			git_user:	this.git_user,
			git_remote:	this.git_remote,
			author:		this.author,
			author_uri:	this.author_uri,
			year:		this.year,
			components:	this.components
		};
	}
	set package( p ) {
		Object.keys(p).forEach( k => this[k] = p[k] )
	}
	get components() {
		var ret = {};
		Object.keys(this._components).forEach( k => {
			ret[k] = this._components[k].package;
		});
		return ret;
	}
	set components( c ) {
		Object.keys(c).forEach( k => this.addComponent( k, c.flags, c.components ) )
	}

	addComponent( slug, flags, components ) {
		const c = new Components[slug]()
		c.package = { components, flags }
		this._components[slug] = c;
	}
}

module.exports = Plugin;

/*
"author": "J\u00f6rn Lund",
"author_uri": "https://github.com/mcguffin",
"name": "WPMS Blog Alias",
"namespace": "BlogAlias",

"slug": "blog_alias",
"slug_upper": "BLOG_ALIAS",
"wp_plugin_slug": "multisite-blog-alias"

"this_year": 2018,

*/
