const BaseComponent = require('./base-component.js');
const ChildComponent = require('./child-component.js');
const change_case = require('change-case');
class ParentComponent extends BaseComponent {

	async setup() {

		this.children = [];
		Object.keys( this.components ).forEach( slug => {
			let c = this.components[slug],
				comp = new ChildComponent( this.plugin ), tpl;

			let m = {
				slug: slug,
				classname: change_case.pascalCase(slug ),
				flags: c.flags
			}

			tpl = `include/{{plugin.namespace}}/${this.namespace}/{{component.classname}}.php`;

			this.children.push(comp);
			comp.addTemplate( tpl )
			comp.package = m;
		} );
	}

	generate() {
		super.generate()
		this.children.forEach( m => m.generate() )
	}
}
module.exports = ParentComponent;
