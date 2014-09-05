<?php


if ( ! class_exists( '{{plugin_class_name}}Admin' ) ):
class {{plugin_class_name}}Admin {
	private static $_instance = null;
	
	/**
	 * Getting a singleton.
	 *
	 * @return object single instance of {{plugin_class_name}}Admin
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
		add_action( 'admin_init' , array( &$this , 'admin_init' ) );
{{#admin_assets}}
		add_action( "admin_print_scripts" , array( &$this , 'enqueue_assets' ) );
{{/admin_assets}}
	}

	/**
	 * Admin init
	 */
	function admin_init() {
	}

	/**
	 * Enqueue options Assets
	 */
	function enqueue_assets() {
{{#admin_css}}
		wp_enqueue_style( '{{plugin_slug}}-admin' , plugins_url( '/css/{{plugin_slug}}-admin.css' , dirname(__FILE__) ));
{{/admin_css}}

{{#admin_js}}
		wp_enqueue_script( '{{plugin_slug}}-admin' , plugins_url( 'js/{{plugin_slug}}-admin.js' , dirname(__FILE__) ) );
		wp_localize_script('{{plugin_slug}}-admin' , '{{plugin_slug}}_admin' , array(
		) );
{{/admin_js}}
	}

}

{{plugin_class_name}}Admin::get_instance();
endif;