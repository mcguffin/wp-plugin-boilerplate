<?php
/**
 *	@package {{plugin_namespace}}\Core
 *	@version 1.0.0
 *	2018-09-22
 */

namespace {{plugin_namespace}}\Core;

if ( ! defined('ABSPATH') ) {
	die('FU!');
}


class Core extends Plugin {

	/**
	 *	@inheritdoc
	 */
	protected function __construct() {

		add_action( 'plugins_loaded' , array( $this , 'load_textdomain' ) );
{{#modules.compat}}
		add_action( 'plugins_loaded' , array( $this , 'init_compat' ), 0 );
{{/modules.compat}}
		add_action( 'init' , array( $this , 'init' ) );

		add_action( 'wp_enqueue_scripts' , array( $this , 'wp_enqueue_style' ) );

		$args = func_get_args();
		parent::__construct( ...$args );
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


{{#modules.compat}}
	/**
	 *	Load Compatibility classes
	 *
	 *  @action plugins_loaded
	 */
	public function init_compat() {
		if ( is_multisite() && is_plugin_active_for_network( $this->get_wp_plugin() ) ) {
			Compat\WPMU::instance();
		}
		if ( function_exists('\acf') && version_comapre( acf()->version,'5.0.0','>=') ) {
			Compat\ACF::instance();
		}
		if ( defined('POLYLANG_VERSION') && version_comapre( POLYLANG_VERSION, '1.0.0', '>=' ) ) {
			Compat\Polylang::instance();
		}
	}
{{/modules.compat}}


	/**
	 *	Load text domain
	 *
	 *  @action plugins_loaded
	 */
	public function load_textdomain() {
		$path = pathinfo( $this->plugin_file(), PATHINFO_FILENAME );
		load_plugin_textdomain( '{{wp_plugin_slug}}', false, $path . '/languages' );
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
		return plugins_url( $asset, $this->plugin_file() );
	}



}
