<?php

namespace {{plugin_namespace}}\Admin;
use {{plugin_namespace}}\Core;


class {{plugin_class}} extends Page {

	/**
	 * Private constructor
	 */
	protected function __construct() {
		parent::__construct();

		$this->core = Core\Core::instance();

		add_action( 'admin_init' , array( $this, 'admin_init' ) );
		add_action( "admin_print_scripts" , array( $this, 'enqueue_assets' ) );
		add_action( 'admin_menu' , array( $this, 'add_admin_page' ) );
	}
	/**
	 * 	Add Admin page to menu
	 *
	 *	@action	admin_menu
	 */
	function add_admin_page() {
		$page_hook = add_{{wp_page_slug}}_page( __( '{{plugin_name}} ({{plugin_class}})' , '{{wp_plugin_slug}}' ), __( '{{plugin_name}}' , '{{wp_plugin_slug}}' ), 'manage_options', '{{plugin_slug}}-{{wp_page_slug}}', array( $this, 'render_page' ) );
		add_action( "load-{$page_hook}" , array( $this, 'enqueue_assets' ) );
	}

	/**
	 * 	Add Admin page to menu
	 */
	function render_page() {
		?><div class="wrap"><?php
			?><h2><?php _e( '{{plugin_name}} ({{plugin_class}})' , '{{wp_plugin_slug}}' ); ?></h2><?php
			?><p><?php _e( 'Content for {{plugin_class}}' , '{{wp_plugin_slug}}' ); ?></p><?php
		?></div><?php
	}
	

	function enqueue_assets() {
{{#css}}
		wp_enqueue_style( '{{plugin_slug}}-admin-page-{{plugin_asset}}' , $this->core->get_asset_url( '/css/admin/admin-page-{{plugin_asset}}.css' ) );
{{/css}}
{{#js}}
		wp_enqueue_script( '{{plugin_slug}}-admin-page-{{plugin_asset}}' , $this->core->get_asset_url( 'js/admin/admin-page-{{plugin_asset}}.js' ) );
		wp_localize_script('{{plugin_slug}}-admin-page-{{plugin_asset}}' , '{{plugin_slug}}_admin_page' , array(
		) );
{{/js}}
	}

	/**
	 * Admin init
	 */
	function admin_init() {
	}

}
