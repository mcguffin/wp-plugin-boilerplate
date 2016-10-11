<?php

namespace TestPlugin\Widget;

class Widgets {
	private static $_instance = null;

	/**
	 * Getting a singleton.
	 *
	 * @return object single instance of {{plugin_namespace}}\PostType\{{plugin_class}}
	 */
	public static function instance() {
		if ( is_null( self::$_instance ) )
			self::$_instance = new self();
		return self::$_instance;
	}

	/**
	 *	Prevent Instantinating
	 */
	private function __clone() { }
	private function __wakeup() { }


	/**
	 * Private constructor
	 */
	private function __construct() {
		add_action('widgets_init', array( $this, 'widgets_init' ) );
	}
	
	public function widgets_init(){
{{#widgets}}
		register_widget("TestPlugin\Widget\{{.}}");
{{/widgets}}
	}

}