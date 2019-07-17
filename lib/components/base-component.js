
const change_case = require('change-case');
const Template = require('../template.js');

class BaseComponent {

	constructor( components = [], flags = [] ) {
		this.components = components;
		this.flags = flags;
		this.templates = []; // template files to render
	}

	setup() {
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

	/**
	 *	@param source string or path to file
	 *	@param dest path to dest file
	 */
	addTemplate( source = '', dest = null ) {
		this.templates.push( new Template( source, dest ) )
	}

	get package() {
		return { components: this.components, flags: this.flags }
	}
	set package( p ) {
		Object.keys(p).forEach( k => this[k] = p[k] )
	}
}

module.exports = BaseComponent;
