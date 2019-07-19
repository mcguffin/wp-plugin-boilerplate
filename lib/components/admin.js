const ParentComponent = require('./parent-component.js');
const promts = require('prompts');

class AdminComponent extends ParentComponent {

	async setup() {
		this.namespace = 'Admin';

		super.setup();

		this.addTemplate( `include/{{plugin.namespace}}/${this.namespace}/${this.namespace}.php` )

		if ( this.flagged.css ) {
			this.plugin.components.core.addCommonSCSS()
		}
		if ( this.flagged.js ) {
			this.plugin.components.core.addCommonJS()
		}
	}

}

module.exports = AdminComponent;
