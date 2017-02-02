<?php

namespace {{plugin_namespace}}\Core;
{{#post_types?}}
use {{plugin_namespace}}\PostType;
{{/post_types?}}

class Core extends Singleton {

	/**
	 *	Private constructor
	 */
	protected function __construct() {
		add_action( 'plugins_loaded' , array( $this , 'load_textdomain' ) );
		add_action( 'init' , array( $this , 'init' ) );
		add_action( 'wp_enqueue_scripts' , array( $this , 'wp_enqueue_style' ) );

		register_activation_hook( {{plugin_slug_upper}}_FILE, array( __CLASS__ , 'activate' ) );
		register_deactivation_hook( {{plugin_slug_upper}}_FILE, array( __CLASS__ , 'deactivate' ) );
		register_uninstall_hook( {{plugin_slug_upper}}_FILE, array( __CLASS__ , 'uninstall' ) );
		
		parent::__construct();
	}

	/**
	 *	Load frontend styles and scripts
	 *
	 *	@action wp_enqueue_scripts
	 */
	public function wp_enqueue_style() {
{{#css}}
		wp_enqueue_style( '{{wp_plugin_slug}}-style', $this->get_asset_url( 'css/frontend.css' ) );
{{/css}}
{{#js}}
		wp_enqueue_script( '{{wp_plugin_slug}}-script', $this->get_asset_url( 'js/frontend.js' ), array( 'jquery' ) );
{{/js}}
	}

	
	/**
	 *	Load text domain
	 * 
	 *  @action plugins_loaded
	 */
	public function load_textdomain() {
		load_plugin_textdomain( '{{wp_plugin_slug}}' , false, {{plugin_slug_upper}}_DIRECTORY . '/languages/' );
	}

	/**
	 *	Init hook.
	 * 
	 *  @action init
	 */
	public function init() {
	}

	/**
	 *	Get asset url for this plugin
	 *
	 *	@param	string	$asset	URL part relative to plugin class
	 *	@return wp_enqueue_editor
	 */
	public function get_asset_url( $asset ) {
		return plugins_url( $asset, {{plugin_slug_upper}}_FILE );
	}


	/**
	 *	Fired on plugin activation
	 */
	public static function activate() {
{{#post_types}}
		PostType\{{.}}::activate();
{{/post_types}}
	}

	/**
	 *	Fired on plugin deactivation
	 */
	public static function deactivate() {
{{#post_types}}
		PostType\{{.}}::deactivate();
{{/post_types}}
	}

	/**
	 *	Fired on plugin deinstallation
	 */
	public static function uninstall() {
{{#post_types}}
		PostType\{{.}}::uninstall();
{{/post_types}}
	}

}
