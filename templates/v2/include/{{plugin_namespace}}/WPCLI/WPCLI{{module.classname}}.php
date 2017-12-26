<?php

namespace {{plugin_namespace}}\WPCLI;

if ( ! defined('ABSPATH') ) {
	die('FU!');
}

use {{plugin_namespace}}\Core;

class WPCLI{{module.classname}} extends Core\Singleton {

	/**
	 *	@inheritdoc
	 */
	protected function __construct() {
		\WP_CLI::add_command( '{{module.slug}}', '{{plugin_namespace}}\WPCLI\Commands\{{module.classname}}', array(
//			'before_invoke'	=> 'a_callable',
//			'after_invoke'	=> 'another_callable',
			'shortdesc'		=> '{{plugin_name}} commands',
//			'when'			=> 'before_wp_load',
			'is_deferred'	=> false,
		) );
	}

}
