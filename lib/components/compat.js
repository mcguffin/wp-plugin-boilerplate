const BaseComponent = require('./base-component.js');
const ChildComponent = require('./child-component.js');
const change_case = require('change-case');

class CompatClass extends BaseComponent {

	async setup() {

		this.children = [];
		Object.keys(this.components).forEach( slug => {
			let c = this.components[slug],
				comp = new ChildComponent( this.plugin ), tpl;

			let m = {
				slug: slug,
				classname: change_case.pascalCase(slug ),
			}
			switch ( slug ) {
				case 'acf':
					m.classname = 'ACF';
					m.isACF = true;
					tpl = 'include/{{plugin.namespace}}/Compat/ACF.php';
					break;
				case 'polylang':
					tpl = 'include/{{plugin.namespace}}/Compat/Polylang.php';
					m.isPLL = true;
					break;
				case 'regenerate-thumbnails':
					tpl = 'include/{{plugin.namespace}}/Compat/RegenerateThumbnails.php';
					m.isREG = true;
					break;
				case 'wpmu':
					m.classname = 'WPMU';
					m.isWPMU = true;
					tpl = 'include/{{plugin.namespace}}/Compat/WPMU.php';
					break;
				default:
					tpl = 'include/{{plugin.namespace}}/Compat/{{component.classname}}.php';
					break;
			}

			this.children.push(comp);
			comp.addTemplate( tpl )
			comp.package = m;
		} );
	}

	generate() {
//		this.children.forEach( m => console.log(m.templates) )
		this.children.forEach( m => m.generate() )
	}
}

module.exports = CompatClass;
