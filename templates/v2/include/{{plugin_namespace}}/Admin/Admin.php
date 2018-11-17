<?php
/**
 *	@package {{plugin_namespace}}\Admin
 *	@version 1.0.0
 *	2018-09-22
 */

namespace {{plugin_namespace}}\Admin;

if ( ! defined('ABSPATH') ) {
	die('FU!');
}

use {{plugin_namespace}}\Core;


class Admin extends Core\Singleton {

	private $core;

	/**
	 *	@inheritdoc
	 */
	protected function __construct() {

		$this->core = Core\Core::instance();

		add_action( 'admin_init', array( $this , 'admin_init' ) );
		add_action( 'admin_print_scripts', array( $this , 'enqueue_assets' ) );
	}


	/**
	 *	Admin init
	 *	@action admin_init
	 */
	public function admin_init() {
	}

	/**
	 *	Enqueue options Assets
	 *	@action admin_print_scripts
	 */
	public function enqueue_assets() {
{{#modules.admin.css}}
		wp_enqueue_style( '{{plugin_slug}}-admin' , $this->core->get_asset_url( '/css/admin.css' ) );
{{/modules.admin.css}}

{{#modules.admin.js}}
		wp_enqueue_script( '{{plugin_slug}}-admin' , $this->core->get_asset_url( 'js/admin.js' ) );
		wp_localize_script('{{plugin_slug}}-admin' , '{{plugin_slug}}_admin' , array(
		) );
{{/modules.admin.js}}
	}

}
