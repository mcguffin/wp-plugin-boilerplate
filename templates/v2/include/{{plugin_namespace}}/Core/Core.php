<?php
/**
 *	@package {{plugin_namespace}}\Core
 *	@version 1.0.1
 *	2018-09-22
 */

namespace {{plugin_namespace}}\Core;

if ( ! defined('ABSPATH') ) {
	die('FU!');
}

{{#modules.compat}}
use {{plugin_namespace}}\Compat;
{{/modules.compat}}

class Core extends Plugin {

	/**
	 *	@inheritdoc
	 */
	protected function __construct() {

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
		{{#modules.compat.wpmu}}
		if ( is_multisite() && function_exists('is_plugin_active_for_network') && is_plugin_active_for_network( $this->get_wp_plugin() ) ) {
			Compat\WPMU::instance();
		}
		{{/modules.compat.wpmu}}
		{{#modules.compat.acf}}
		if ( function_exists('\acf') && version_compare( acf()->version,'5.0.0','>=') ) {
			Compat\ACF::instance();
		}
		{{/modules.compat.acf}}
		{{#modules.compat.polylang}}
		if ( defined('POLYLANG_VERSION') && version_compare( POLYLANG_VERSION, '1.0.0', '>=' ) ) {
			Compat\Polylang::instance();
		}
		{{/modules.compat.polylang}}
		{{#modules.compat.regenerate_thumbnails}}
		if ( class_exists( '\RegenerateThumbnails' ) ) {
			Compat\RegenerateThumbnails::instance();
		}
		{{/modules.compat.regenerate_thumbnails}}

	}
{{/modules.compat}}


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
	 *	@return string URL
	 */
	public function get_asset_url( $asset ) {
		return plugins_url( $asset, $this->get_plugin_file() );
	}


	/**
	 *	Get asset url for this plugin
	 *
	 *	@param	string	$asset	URL part relative to plugin class
	 *	@return string URL
	 */
	public function get_asset_path( $asset ) {
		return $this->get_plugin_dir() . '/' . preg_replace( '/^(\/+)/', '', $asset );
	}


}
