<?php


namespace {{plugin_namespace}}\Shortcode;

if ( ! defined('ABSPATH') ) {
	die('FU!');
}

use {{plugin_namespace}}\Core;

class Shortcode{{module.classname}} extends Shortcode {

	protected $shortcode = '{{module.slug}}';

{{#module.mce}}
	private $mce = null;
{{/module.mce}}


{{#module.mce}}
	protected function __construct() {
		parent::__construct();

		$this->mce = Mce\Mce{{module.classname}}::instance();
	}
{{/module.mce}}

	public function do_shortcode( $atts, $content ) {
		return sprintf( '<pre>%s</pre><p>%s</p>', var_export( $atts, true ), $content );
	}

}
