const basedir = require('../package.json').templateDir;
const fs = require('fs');
const Mustache = require('mustache');


class Template {

	static get destdir() {
		return this._destdir;
	}

	static set destdir( dir ) {
		this._destdir = dir;
	}

	static get plugin() {
		return this._plugin;
	}
	static set plugin( pl ) {
		this._plugin = pl;
	}

	/**
	 *	@param source string or path to file within plugin root
	 *	@param dest false: same as source, other string: dest path within plugin root
	 */
	constructor( source = '', dest = false ) {
		let path;
		try {
			path = fs.realpathSync( basedir +'/'+ source + '.mustache');
			fs.accessSync( path, fs.constants.R_OK );
			this.template = fs.readfileSync( path );

		} catch( err ) {
			this.template = source;
			if ( dest === false ) {
				throw('Must provide dest if source is not a file')
			}
		}
		if ( ! dest ) {
			dest = source;
		}
		this.dest = dest;
		Mustache.parse( this.template )
		Mustache.parse( this.dest );
	}

	render( params = {} ) {
		const rendered = Mustache.render(this.template, params )
		console.log('Write to',Template.destdir + Mustache.render( this.dest, {plugin:this.plugin.package, component:params } ) )
		return;
		fs.writeFileSync( Template.destdir + this.dest( params ), rendered, { mode: 0o755 } )
	}
}

module.exports = Template;
