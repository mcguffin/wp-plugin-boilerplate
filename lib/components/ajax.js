const BaseComponent = require('./base-component.js');

class AjaxComponent extends BaseComponent {

	async setup() {
		this.addTemplate( `include/{{plugin.namespace}}/Ajax/AjaxHandler.php` )
		super.setup();
	}

}

module.exports = AjaxComponent;
