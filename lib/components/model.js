const ParentComponent = require('./parent-component.js');

class ModelComponent extends ParentComponent {
	setup() {
		this.namespace = 'Model';
		this.addTemplate( `include/{{plugin.namespace}}/${this.namespace}/${this.namespace}.php` )
		super.setup();
	}
}

module.exports =  ModelComponent;
