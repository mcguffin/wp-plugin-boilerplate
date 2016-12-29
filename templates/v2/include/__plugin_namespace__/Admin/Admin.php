<?php

namespace {{plugin_namespace}}\Admin;
use {{plugin_namespace}}\Core;


class Admin extends Core\Singleton {

	private $core;

	/**
	 *	Private constructor
	 */
	protected function __construct() {

		$this->core = Core\Core::instance();

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
		wp_enqueue_style( '{{plugin_slug}}-admin' , $this->core->get_asset_url( '/css/admin.css' ) );
{{/css}}

{{#js}}
		wp_enqueue_script( '{{plugin_slug}}-admin' , $this->core->get_asset_url( 'js/admin.js' ) );
		wp_localize_script('{{plugin_slug}}-admin' , '{{plugin_slug}}_admin' , array(
		) );
{{/js}}
	}

}

