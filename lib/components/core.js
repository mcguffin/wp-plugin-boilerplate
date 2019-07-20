const BaseComponent = require('./base-component.js');

class CoreComponent extends BaseComponent {

	async setup() {
		const tpl = [
			'.editorconfig',
			// '.babelrc',
			// '.eslinignore',
			// '.eslintrc',
			// '.gitattributes',
			// '.gitignore',
			// '.sassrc',
			'index.php',
			'LICENSE',
			'README.md',
			'readme.txt',
			'include/autoload.php',
			'include/{{plugin.namespace}}/Core/Core.php',
			'include/{{plugin.namespace}}/Core/Plugin.php',
			'include/{{plugin.namespace}}/Core/PluginComponent.php',
			'include/{{plugin.namespace}}/Core/Singleton.php',
		];
		const jstpl = [
			'src/js/main/index.js',
		];
		const csstpl = [
			'src/scss/main.scss',
		];
		tpl.forEach( t => this.addTemplate( t ) );
		if ( this.flagged.css ) {
			csstpl.forEach( t => this.addTemplate( t ) );
		}
		if ( this.flagged.js ) {
			jstpl.forEach( t => this.addTemplate( t ) );
		}

		this.plugin.mergeRootPackage({
			scripts: {
				i18n:`wp i18n make-pot . languages/${this.plugin.textdomain}.pot --domain=${this.plugin.textdomain} --exclude=tmp/*`
			}
		});

		super.setup()
	}
	generate() {

		super.generate()
		// npm run dashicons
	}

	addCommonJS() {
		[
			'.babelrc',
			'.eslintignore',
			'.eslintrc',
			'./src/js/lib/__placeholder__.js',
		].forEach( t => this.addTemplate( t ) );

		this.addCommonAssets();

		this.plugin.mergeRootPackage({
			"browserify-shim": {
				jquery: "global:jQuery"
			},
			devDependencies: {
				"@babel/core": "^7.5.4",
			    "@babel/plugin-proposal-class-properties": "^7.5.0",
			    "@babel/plugin-proposal-object-rest-spread": "^7.5.4",
			    "@babel/plugin-transform-react-jsx": "^7.3.0",
			    "@babel/preset-env": "^7.5.4",
			    "babelify": "^10.0.0",
			    "browserify": "^16.3.0",
			    "browserify-shim": "^3.8.14",
			    "event-stream": "^4.0.1",
			    "vinyl-buffer": "^1.0.1",
			    "vinyl-source-stream": "^2.0.0"
			},
			dependencies: {
				jquery: "^1.12.4"
			}
		});
	}
	addCommonSCSS() {
		[
			'.sassrc',
			'./src/scss/mixins/_index.scss',
			'./src/scss/variables/_index.scss',
			'./src/scss/variables/_colors.scss',
			'./src/scss/variables/_dashicons.scss',
			'./src/run/dashicons.js',
		].forEach( t => this.addTemplate( t ) );
		this.addCommonAssets();
		this.plugin.mergeRootPackage({
			scripts:{
				dashicons: "node ./src/run/dashicons.js",
			},
			devDependencies: {
				"gulp-autoprefixer": "^6.1.0",
				"gulp-sass": "^4.0.2",
				"gulp-uglify": "^3.0.2",
			}
		});
	}
	addCommonAssets() {
		this.plugin.mergeRootPackage({
			browserslist: [
				"last 3 versions",
				"> 0.25%",
				"IE 10"
			],
			devDependencies: {
				"gulp": "^4.0.2",
				"gulp-sourcemaps": "^2.6.5",
			}
		});
	}
}

module.exports = CoreComponent;
