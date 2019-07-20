const ParentComponent = require('./parent-component.js');
const ChildComponent = require('./child-component.js');

class SettingsChildComponent extends ChildComponent {

	get isWP() {
		return -1 !== ['general','writing','reading','discussion','media','permalink'].indexOf(this.slug);
	}

}
class SettingsComponent extends ParentComponent {

	namespace = 'Admin/Settings';
	componentClass = SettingsChildComponent

}

module.exports = SettingsComponent;
