const BaseComponent = require('./base-component.js');
const ChildComponent = require('./child-component.js');
const change_case = require('change-case');

class ParentComponent extends BaseComponent {

	componentClass = ChildComponent

	async setup() {
		const cls = this.namespace.split('/').pop();
		this.addTemplate( `include/{{plugin.namespace}}/${this.namespace}/${cls}.php` )

		super.setup()

		this.children = [];
		Object.keys( this.components ).forEach( slug => {
			let c = this.components[slug],
				comp = new this.componentClass( this.plugin ), tpl;

			let m = {
				slug: slug,
				classname: change_case.pascalCase( slug ),
				flags: c.flags
			}

			tpl = `include/{{plugin.namespace}}/${this.namespace}/{{component.classname}}.php`;

			this.children.push(comp);
			comp.package = m;
			comp.addTemplate( tpl )
			comp.setup()
		} );
	}

	generate() {
		super.generate()
		this.children.forEach( m => m.generate() )
	}
}
module.exports = ParentComponent;
