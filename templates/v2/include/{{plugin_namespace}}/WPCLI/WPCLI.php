<?php
/**
 *	@package {{plugin_namespace}}\WPCLI
 *	@version 1.0.0
 *	2018-09-22
 */

namespace {{plugin_namespace}}\WPCLI;

if ( ! defined('ABSPATH') ) {
	die('FU!');
}

use {{plugin_namespace}}\Core;

class WPCLI extends Core\Singleton {

	/**
	 *	@inheritdoc
	 */
	protected function __construct() {
		$command = Commands\{{module.classname}};
		\WP_CLI::add_command( '{{module.slug}}', array( $command, 'bark' ), array(
//			'before_invoke'	=> 'a_callable',
//			'after_invoke'	=> 'another_callable',
			'shortdesc'		=> '{{plugin_name}} commands',
//			'when'			=> 'before_wp_load',
			'is_deferred'	=> false,
		) );
	}

}
