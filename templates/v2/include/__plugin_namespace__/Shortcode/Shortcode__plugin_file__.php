<?php


namespace {{plugin_namespace}}\Shortcode;

if ( ! defined('ABSPATH') ) {
	die('FU!');
}

use {{plugin_namespace}}\Core;

class Shortcode{{plugin_class}} extends Shortcode {

	protected $shortcode = '{{shortcode_slug}}';

{{#mce}}
	private $mce = null;
{{/mce}}


{{#mce}}
	protected function __construct() {
		parent::__construct();

		$this->mce = Mce\Mce{{plugin_class}}::instance();
	}
{{/mce}}

	public function do_shortcode( $atts, $content ) {
		return sprintf( '<pre>%s</pre><p>%s</p>', var_export( $atts, true ), $content );
	}

}
