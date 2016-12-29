<?php

namespace {{plugin_namespace}}\Shortcode;
use {{plugin_namespace}}\Core;

abstract class Shortcode extends Core\Singleton {

	protected $shortcode = false;

	protected function __construct(){
		parent::__construct();
		if ( $this->shortcode ) {
			add_shortcode( $this->shortcode, array( $this, 'do_shortcode' ) );
		}
	}	

	abstract function do_shortcode( $atts, $content );

}