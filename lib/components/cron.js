const BaseComponent = require('./base-component.js');

class CronComponent extends BaseComponent {

	async setup() {
		this.addTemplate( `include/{{plugin.namespace}}/Cron/Cron.php` )
		this.addTemplate( `include/{{plugin.namespace}}/Cron/Job.php` )
		super.setup();
	}

}

module.exports = CronComponent;
