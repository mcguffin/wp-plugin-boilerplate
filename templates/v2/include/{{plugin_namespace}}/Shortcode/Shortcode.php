<?php
/**
 *	@package {{plugin_namespace}}\Shortcode
 *	@version 1.0.0
 *	2018-09-22
 */
namespace {{plugin_namespace}}\Shortcode;

if ( ! defined('ABSPATH') ) {
	die('FU!');
}

use {{plugin_namespace}}\Core;

abstract class Shortcode extends Core\Singleton {

	protected $shortcode = false;

	/**
	 *	@inheritdoc
	 */
	protected function __construct(){
		parent::__construct();
		if ( $this->shortcode ) {
			add_shortcode( $this->shortcode, array( $this, 'do_shortcode' ) );
		}
	}

	abstract function do_shortcode( $atts, $content );

}
