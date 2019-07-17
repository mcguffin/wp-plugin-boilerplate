const BaseComponent = require('./base-component.js');
const promts = require('prompts');

class AdminComponent extends BaseComponent {

	async setup() {
		let p = 'include/{{plugin.namespace}}/Admin.php';
		this.addTemplate( 'include/{{plugin.namespace}}/Admin/Admin.php' )
		this.addTemplate( 'Plugin-Namespace: {{plugin.namespace}}', 'foo.txt' )
		super.setup()

	}

}

module.exports = AdminComponent;
