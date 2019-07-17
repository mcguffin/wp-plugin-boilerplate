const BaseComponent = require('./base-component.js');

class CoreComponent extends BaseComponent {

	async setup() {
		[
			'.babelrc',
			'.editorconfig',
			'.eslinignore',
			'.eslintrc',
			'.gitattributes',
			'.gitignore',
			'.sassrc',
			'index.php',
			'LICENSE',
			'package.json',
			'README.md',
			'readme.txt',
			'include/{{plugin.namespace}}/Core.php',
			'include/{{plugin.namespace}}/Plugin.php',
			'include/{{plugin.namespace}}/PluginComponent.php',
			'include/{{plugin.namespace}}/Singleton.php',
		].forEach( t => this.addTemplate( t ) );

		super.setup()

	}
}

module.exports = CoreComponent;
