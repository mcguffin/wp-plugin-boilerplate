<?php

namespace {{plugin_namespace}}\Admin;


class Admin {
	private static $_instance = null;
	
	/**
	 *	Getting a singleton.
	 *
	 *	@return object single instance of {{plugin_class_name}}Admin
	 */
	public static function instance() {
		if ( is_null( self::$_instance ) )
			self::$_instance = new self();
		return self::$_instance;
	}

	/**
	 *	Prevent Instantinating
	 */
	private function __clone() { }
	private function __wakeup() { }


	/**
	 *	Private constructor
	 */
	private function __construct() {
		add_action( 'admin_init', array( $this , 'admin_init' ) );
{{#flags}}
		add_action( 'admin_print_scripts', array( $this , 'enqueue_assets' ) );
{{/flags}}
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
{{#css}}
		wp_enqueue_style( '{{plugin_slug}}-admin' , plugins_url( '/css/admin.css' , dirname(__FILE__) ) );
{{/css}}

{{#js}}
		wp_enqueue_script( '{{plugin_slug}}-admin' , plugins_url( 'js/admin.js' , dirname(__FILE__) ) );
		wp_localize_script('{{plugin_slug}}-admin' , '{{plugin_slug}}_admin' , array(
		) );
{{/js}}
	}

}

