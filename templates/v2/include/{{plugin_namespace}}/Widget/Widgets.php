<?php

namespace {{plugin_namespace}}\Widget;

if ( ! defined('ABSPATH') ) {
	die('FU!');
}

use {{plugin_namespace}}\Core;

class Widgets extends Core\Singleton {

	/**
	 *	@inheritdoc
	 */
	protected function __construct() {
		parent::__construct();
		add_action( 'widgets_init', array( $this, 'widgets_init' ) );
	}

	/**
	 *	@action widgets_init
	 */
	public function widgets_init(){
{{#modules.widget.items}}
		register_widget("{{plugin_namespace}}\Widget\Widget{{module.classname}}");
{{/modules.widget.items}}
	}

}
