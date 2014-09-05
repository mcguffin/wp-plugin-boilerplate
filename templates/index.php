<?php

/*
Plugin Name: {{plugin_name}}
Plugin URI: http://wordpress.org/
Description: Enter description here.
Author: {{plugin_author}}
Version: 1.0.0
Author URI: {{plugin_author_uri}}
License: GPL3

Text Domain: {{plugin_slug}}
Domain Path: /languages/
*/

/*  Copyright {{this_year}}  {{plugin_author}}

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License, version 2, as 
    published by the Free Software Foundation.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/


if ( ! class_exists( '{{plugin_class_name}}' ) ):
class {{plugin_class_name}} {
	private static $_instance = null;

	/**
	 * Getting a singleton.
	 *
	 * @return object single instance of {{plugin_class_name}}Settings
	 */
	public static function get_instance() {
		if ( is_null( self::$_instance ) )
			self::$_instance = new self();
		return self::$_instance;
	}

	/**
	 * Private constructor
	 */
	private function __construct() {
		add_action( 'plugins_loaded' , array( &$this , 'load_textdomain' ) );
		add_action( 'init' , array( &$this , 'init' ) );
		add_action( 'wp_enqueue_scripts' , array( &$this , 'enqueue_assets' ) );
		{{#shortcodes}}
		add_shortcode( '{{.}}' , array( &$this , 'shortcode_{{.}}' ) );
		{{/shortcodes}}
	}

	/**
	 * Load text domain
	 */
	public function load_textdomain() {
		load_plugin_textdomain( '{{plugin_slug}}' , false, dirname( plugin_basename( __FILE__ ) ) . '/languages/' );
	}
	/**
	 * Init hook.
	 * 
	 *  - Register assets
	 */
	function init() {
{{#frontend_js}}		wp_register_script( '{{plugin_slug}}' , plugins_url( '/js/{{plugin_slug}}.js' , __FILE__ ) , array() , false , true );
{{/frontend_js}}{{#frontend_css}}		wp_register_style( '{{plugin_slug}}' , plugins_url( '/css/{{plugin_slug}}.css' , __FILE__ ) , array() , '1.0' );
{{/frontend_css}}
	}
	/**
	 *  Enqueue Frontend Scripts
	 */
	function enqueue_assets() {	
		wp_enqueue_script( '{{plugin_slug}}' );
		wp_enqueue_style( '{{plugin_slug}}' );
	}

{{#shortcodes}}
	/**
	 * Init hook.
	 * 
	 *  - Register assets
	 */
	public function shortcode_{{.}}( $atts , $content = null ) {
		$atts = shortcode_atts( array(
			'default_attr' => 'Default Value',
		), $atts );
		return $content;
	}
{{/shortcodes}}

}
{{plugin_class_name}}::get_instance();

endif;

{{#widget}}require_once plugin_dir_path(__FILE__) . 'include/class-{{plugin_class_name}}_Widget.php';
{{/widget}}
{{#backend}}if ( is_admin() ) {
{{#admin}}	require_once plugin_dir_path(__FILE__) . 'include/class-{{plugin_class_name}}Admin.php';
{{/admin}}
{{#settings}}	require_once plugin_dir_path(__FILE__) . 'include/class-{{plugin_class_name}}Settings.php';
{{/settings}}
}
{{/backend}}
