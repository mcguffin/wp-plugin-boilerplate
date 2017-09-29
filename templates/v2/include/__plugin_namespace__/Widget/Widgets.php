<?php

namespace {{plugin_namespace}}\Widget;
use {{plugin_namespace}}\Core;

class Widgets extends Core\Singleton {

	/**
	 * Private constructor
	 */
	protected function __construct() {
		parent::__construct();
		add_action('widgets_init', array( $this, 'widgets_init' ) );
	}

	public function widgets_init(){
{{#widgets}}
		register_widget("{{plugin_namespace}}\Widget\Widget{{.}}");
{{/widgets}}
	}

}
