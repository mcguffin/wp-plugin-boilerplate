<?php

namespace {{plugin_namespace}}\WPRest;

if ( ! defined('ABSPATH') ) {
	die('FU!');
}

use {{plugin_namespace}}\Core;

class WPRest extends Core\Singleton {

	/**
	 *	@inheritdoc
	 */
	protected function __construct() {
		parent::__construct();
		add_action( 'rest_api_init', array( $this, 'rest_api_init' ) );
	}

	/**
	 *	@return string
	 */
	public function get_namespace() {
		return '{{plugin_slug}}/v1';
	}

	/**
	 *	@action widgets_init
	 */
	public function rest_api_init(){
{{#modules.wprest.items}}
		WPRest{{module.classname}}::instance();
{{/modules.wprest.items}}
	}

}
