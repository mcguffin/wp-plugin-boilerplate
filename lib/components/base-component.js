
const change_case = require('change-case');

const { Template, TemplateExistsError } = require('../template.js');


class BaseComponent {

	constructor( plugin ) {
		this.components = [];
		this.flags = [];
		this.templates = []; // template files to render
		this.plugin = plugin;
	}

	setup() {
		if ( this.flagged.css ) {
			this.plugin.components.core.addCommonSCSS()
		}
		if ( this.flagged.js ) {
			this.plugin.components.core.addCommonJS()
		}
	}

	generate() {
		this.templates.forEach( t => {
			t.render( this )
		} )
	}

	finish() {

	}

	has( flag ) {
		return this.flags.indexOf(flag) !== -1;
	}

	get slug() {
		return change_case.paramCase( this.constructor.name.replace('Component','') );
	}

	get prefix() {
		return change_case.snakeCase( this.slug );
	}

	get name() {
		return change_case.titleCase( this.slug );
	}

	get flagged() {
		let r = {}
		this.flags.forEach( f => r[f] = true );
		return r;
	}

	/**
	 *	@param source string or path to file
	 *	@param dest path to dest file
	 */
	addTemplate( source = '', dest = false ) {
		let t;
		try {
			t = new Template( source, dest );
			t.plugin = this.plugin;
		} catch ( e ) {
			if ( e.constructor === TemplateExistsError ) {
				t = Template.fromDest( dest || source )
			} else {
				throw(e)
			}
//			e.constructor === TemplateExistsError;
		}
		this.templates.push( t )
		return t;
	}

	get package() {
		return { components: this.components, flags: this.flags }
	}
	set package( p ) {
		Object.keys(p).forEach( k => this[k] = p[k] )
	}
}

module.exports = BaseComponent;
