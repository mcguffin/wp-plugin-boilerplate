const ParentComponent = require('./parent-component.js');
const ChildComponent = require('./child-component.js');


class ShortcodeChildComponent extends ChildComponent {

	setup() {
		super.setup()
		if ( this.flagged.css ) {
			this.addTemplate('src/scss/shortcode/{{component.slug}}.scss');
		}
		if ( this.flagged.mce ) {
			this.addTemplate('include/{{plugin.namespace}}/Admin/Mce/Mce.php');
			this.addTemplate('include/{{plugin.namespace}}/Shortcode/Mce/{{component.classname}}.php');


			this.addTemplate('src/js/admin/mce/{{component.slug}}/index.js');
			this.addTemplate('src/scss/admin/mce/{{component.slug}}-toolbar.scss');
			this.addTemplate('src/scss/admin/mce/{{component.slug}}-editor.scss');
			this.plugin.components.core.addCommonJS();
		}
		if ( this.flagged.css || this.flagged.mce ) {
			this.plugin.components.core.addCommonSCSS();
		}

	}

}

class ShortcodeComponent extends ParentComponent {
	componentClass = ShortcodeChildComponent;
	namespace = 'Shortcode';
}

module.exports = ShortcodeComponent;
