const change_case = require('change-case');
const promts = require('prompts');
const exec = require('child_process');
const path = require('path');
const fs = require('fs');
const rmdir = require('rimraf');
const { Template, TemplateExistsError } = require('./template.js');
const Components = require('./components/index.js');
const {doing} = require('./doing.js');
const _ = require('lodash');
const unwp = s => s.replace(/^(wp|wordpress)(\s|-)/i,'');
const wpize = s => s.replace(/^(wp|wordpress)(\s|-)/i,'WP$2');


class Plugin {

	constructor() {

		// names
		Template.plugin = this;

		this.force = false;

		this.name = false;
		this.slug = false;
		this.prefix = false;
		this.textdomain = false;
		this.namespace = false;

		this.author = false;
		this.author_uri = false;

		this.year = false;
		this._components = {
			core: new Components.core(this)
		}

		this.root_package = null;
	}

	get destdir() {
		return Template.destdir;
	}
	set destdir( p ) {
		Template.destdir = p;
	}


	async setup() {
		let data, destdir, root_package, will_do, exists;
		const setProps = d => {
			Object.keys(d).forEach( k => this[k] = d[k] )
			this.guessProps()
		}
		const validName = name => !name.match(/^[a-z]/i) ? 'Must begin with a letter!' : true;
		const validSlug = name => !name.match(/^[a-z][a-z0-9_-]/i) ? 'Only letters numbers, dash or underscore. Must begin with a letter' : true;

		if ( this.name === false ) {

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
				}
			], { onCancel: process.exit });

			this.prefix = false;

			setProps( data );

			// confirm
			if ( this.destdir === undefined ) {
				// plugin with same slug exists
				exists = this.exists();
				will_do = exists ? 'override' : 'create new';

				if ( ! this.force && exists ) {
					throw( `Plugin ${this.slug} exists. Use --force to override.` );
				}

				if ( ! this.canWrite() ) {
					throw( `Can't write to ${process.cwd()}.` );
				}

				data = await promts([
					{
						type: 'confirm',
						name: 'confirm',
						message: `Please confirm: ${will_do} plugin ${this.slug}:`,
						initial: true
					}
				], { onCancel: process.exit });

				if ( ! data.confirm ) {
					process.exit();
				}

				this.destdir = `${process.cwd()}/${this.slug}`;

				if ( exists ) {
					// reset!
					rmdir.sync( this.destdir );
				}
				fs.mkdirSync( this.destdir, { recursive: true } );
			}


			data = await promts([
				{
					type: 'text',
					name: 'prefix',
					message: 'Plugin prefix:',
					initial: this.prefix,
					validate: validSlug
				}
			], { onCancel: process.exit } );

			this.textdomain = this.namspace = false;
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
				}
			], { onCancel: process.exit });

			this.author = this.author_uri = false;
			setProps(data)

			data = await promts([
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

			this.mergeRootPackage( {
				name: this.slug,
				version: "0.0.0",
				description: "",
				private: true,
				author:this.author,
				license: 'GPLv3',
				engines: {
					node: "12.4.0",
					npm: "^6.9.0"
				}
		  } );
		}


		let c = Object.values(this._components);
		while ( c.length ) {
			await c.shift().setup();
		}
		this.mergeRootPackage({
			wpPlugin: this.package
		});
		this.writeRootPackage()

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


	exists() {
		const destdir = process.cwd() + '/' + this.slug;
		try {
			fs.accessSync( destdir, fs.constants.R_OK | fs.constants.W_OK );
			return true;
		} catch( e ) {
			return false;
		}
	}

	canWrite() {
		try {
			// can write in plugins dir
			if ( this.exists() ) {
				return true;
			}
			fs.accessSync( process.cwd(), fs.constants.R_OK | fs.constants.W_OK );
		} catch(e) {
			return false;
		}
		return true;
	}

	mergeRootPackage( data ) {
		_.merge( this.root_package, data )
	}

	writeRootPackage() {
		fs.writeFileSync( this.destdir + '/package.json', JSON.stringify( this.root_package, null, 2 ) );
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
		if ( this.author === false ) {
			this.author = process.env.USER; // better than nothing ...?
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

	addComponent( slug, p ) {
		const c = new Components[slug](this)
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
