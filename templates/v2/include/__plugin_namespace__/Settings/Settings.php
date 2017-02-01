<?php

namespace {{plugin_namespace}}\Settings;
use {{plugin_namespace}}\Core;

abstract class Settings extends Core\Singleton {

	protected $shortcode = false;

	/**
	 *	Constructor
	 */
	protected function __construct(){

		add_action( 'admin_init' , array( $this, 'register_settings' ) );

		parent::__construct();

	}


	abstract function register_settings();

}