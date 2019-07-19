const basedir = require('../package.json').templateDir;
const fs = require('fs');
const path = require('path');
const Mustache = require('mustache');

const dests = {};
let _srcdir, _destdir;

class TemplateExistsError extends Error {
}

class Template {


	static get srcdir() {
		return _srcdir;
	}

	static set srcdir( dir ) {
		_srcdir = dir;
	}

	static get destdir() {
		return _destdir;
	}

	static set destdir( dir ) {
		_destdir = dir;
	}

	/**
	 *	@param source string or path to file within plugin root
	 *	@param dest false: same as source, other string: dest path within plugin root
	 */
	constructor( source = '', dest = false ) {
		let path;
		try {
			path = fs.realpathSync( `${process.mainModule.path}/${Template.srcdir}/${source}.mustache` );
			fs.accessSync( path, fs.constants.R_OK );
			this.template = fs.readFileSync( path, { encoding: 'utf8' } );

		} catch( err ) {
			this.template = source;
			if ( dest === false ) {
				throw('Must provide dest if source is not a file')
			}
		}
		this.dest = !!dest ? dest : source;
		if ( dests[ this.dest ] ) {
			throw( new TemplateExistsError(`Template already registered ${this.dest}`) );
		}
		dests[ this.dest ] = this;

	}

	render( params = {} ) {
		const view = { plugin: Template.plugin.package, component:params };
		const content = Mustache.render( this.template, view );
		const dest = Mustache.render( this.dest, view );
		const destfile = `${Template.destdir}/${dest}`;

		fs.mkdirSync( path.dirname( destfile ), { recursive: true } );
		fs.writeFileSync( destfile, content, { mode: 0o755 } )
	}
}

module.exports = { Template, TemplateExistsError };
