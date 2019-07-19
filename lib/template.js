const basedir = require('../package.json').templateDir;
const fs = require('fs');
const path = require('path');
const Mustache = require('mustache');

const dests = {};
let _srcdir, _destdir, _override = false;

class TemplateExistsError extends Error {
}

class Template {


	static get override() {
		return _override;
	}
	static set override( o ) {
		_override = o;
	}

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

	destExists(dest) {
		try {
			fs.accessSync( dest, fs.constants.R_OK );
			return true;
		} catch( e ) {
			return false;
		}
	}


	exists() {
		const destdir = process.cwd() + '/' + this.slug;

	}
	static fromDest( dest ) {
		return dests[ dest ];
	}

	/**
	 *	@param source string or path to file within plugin root
	 *	@param dest false: same as source, other string: dest path within plugin root
	 */
	constructor( source = '', dest = false ) {
		let path;

		path = fs.realpathSync( `${process.mainModule.path}/${Template.srcdir}/${source}.mustache` );
		fs.accessSync( path, fs.constants.R_OK );
		this.template = fs.readFileSync( path, { encoding: 'utf8' } );

		this.dest = !!dest ? dest : source;
		if ( dests[ this.dest ] ) {
			throw( new TemplateExistsError(`Template already registered ${this.dest}`) );
		}
		dests[ source ] = this;
	}

	render( component = {} ) {
		const view = { plugin: Template.plugin, component };
		const content = Mustache.render( this.template, view );
		const dest = Mustache.render( this.dest, view );
		const destfile = `${Template.destdir}/${dest}`;

		if ( Template.override || ! this.destExists( destfile ) ) {
			fs.mkdirSync( path.dirname( destfile ), { recursive: true } );
			fs.writeFileSync( destfile, content, { mode: 0o755 } )
		}
	}
}

module.exports = { Template, TemplateExistsError };
