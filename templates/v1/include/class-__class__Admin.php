<?php


if ( ! class_exists( '{{plugin_class_name}}Admin' ) ):
class {{plugin_class_name}}Admin {
	private static $_instance = null;
	
	/**
	 * Getting a singleton.
	 *
	 * @return object single instance of {{plugin_class_name}}Admin
	 */
	public static function instance() {
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
{{#admin_page}}
		add_action( 'admin_menu' , array( &$this , 'add_admin_page' ) );
{{/admin_page}}
	}
{{#admin_page}}	
	/**
	 * 	Add Admin page to menu
	 *
	 *	@action	admin_menu
	 */
	function add_admin_page() {
{{#admin_pages}}
		$page_hook = add_{{.}}_page( __( '{{plugin_name}} ({{.}})' , '{{wp_plugin_slug}}' ), __( '{{plugin_name}}' , '{{wp_plugin_slug}}' ), 'manage_options', '{{plugin_slug}}-{{.}}', array( &$this , 'render_{{.}}_page' ) );
		add_action( "load-{$page_hook}" , array( &$this , 'enqueue_admin_page_assets' ) );
{{/admin_pages}}
{{^admin_pages}}
		$page_hook = add_menu_page( __( '{{plugin_name}} Admin' , '{{wp_plugin_slug}}' ), __( '{{plugin_name}}' , '{{wp_plugin_slug}}' ), 'manage_options', '{{plugin_slug}}', array( &$this , 'render_admin_page' ), 'dashicons-admin-generic' );
		add_action( "load-{$page_hook}" , array( &$this , 'enqueue_admin_page_assets' ) );
{{/admin_pages}}
	}
{{#admin_pages}}
	/**
	 * 	Add Admin page to menu
	 */
	function render_{{.}}_page() {
		?><div class="wrap"><?php
			?><h2><?php _e( '{{plugin_name}} ({{.}})' , '{{wp_plugin_slug}}' ); ?></h2><?php
			?><p><?php _e( 'Content for {{.}}' , '{{wp_plugin_slug}}' ); ?></p><?php
		?></div><?php
	}
{{/admin_pages}}
	
	/**
	 * Render Admin page
	 */
	function render_admin_page() {
		?><div class="wrap"><?php
			?><h2><?php _e( '{{plugin_name}} Admin' , '{{wp_plugin_slug}}' ); ?></h2><?php
			?><p><?php _e( 'Admin Page content' , '{{wp_plugin_slug}}' ); ?></p><?php
		?></div><?php
	}
	function enqueue_admin_page_assets() {
{{#admin_page_css}}
		wp_enqueue_style( '{{plugin_slug}}-admin-page' , plugins_url( '/css/{{plugin_slug}}-admin-page.css' , dirname(__FILE__) ) );
{{/admin_page_css}}

{{#admin_page_js}}
		wp_enqueue_script( '{{plugin_slug}}-admin-page' , plugins_url( 'js/{{plugin_slug}}-admin-page.js' , dirname(__FILE__) ) );
		wp_localize_script('{{plugin_slug}}-admin-page' , '{{plugin_slug}}_admin_page' , array(
		) );
{{/admin_page_js}}
	}
{{/admin_page}}
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
		wp_enqueue_style( '{{plugin_slug}}-admin' , plugins_url( '/css/{{plugin_slug}}-admin.css' , dirname(__FILE__) ) );
{{/admin_css}}

{{#admin_js}}
		wp_enqueue_script( '{{plugin_slug}}-admin' , plugins_url( 'js/{{plugin_slug}}-admin.js' , dirname(__FILE__) ) );
		wp_localize_script('{{plugin_slug}}-admin' , '{{plugin_slug}}_admin' , array(
		) );
{{/admin_js}}
	}

}

{{plugin_class_name}}Admin::instance();
endif;