const ParentComponent = require('./parent-component.js');
const promts = require('prompts');

class AdminComponent extends ParentComponent {

	async setup() {
		this.namespace = 'Model';
		this.addTemplate( `include/{{plugin.namespace}}/${this.namespace}/${this.namespace}.php` )
		super.setup();
	}

}

module.exports = AdminComponent;
