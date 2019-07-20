const ParentComponent = require('./parent-component.js');
const ChildComponent = require('./child-component.js');

class WidgetChildComponent extends ChildComponent {
	setup() {
		this.addTemplate('src/scss/widget/{{component.slug}}.scss');
		this.plugin.components.core.addCommonSCSS()
		super.setup()
	}
}

class WidgetComponent extends ParentComponent {
	namespace = 'Widget';
	componentClass = WidgetChildComponent
	// todo: add main css, add widget css, set componentClass

}

module.exports = WidgetComponent;
