<?php

namespace {{plugin_namespace}};

class Core {
	private static $_instance = null;

	/**
	 * Getting a singleton.
	 *
	 * @return object single instance of Core
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
	 *	Private constructor
	 */
	private function __construct() {
		add_action( 'plugins_loaded' , array( $this , 'load_textdomain' ) );
		add_action( 'init' , array( $this , 'init' ) );
		add_action( 'wp_enqueue_scripts' , array( $this , 'wp_enqueue_style' ) );

		register_activation_hook( PLUGIN_FILE, array( __CLASS__ , 'activate' ) );
		register_deactivation_hook( PLUGIN_FILE, array( __CLASS__ , 'deactivate' ) );
		register_uninstall_hook( PLUGIN_FILE, array( __CLASS__ , 'uninstall' ) );
	}
	
	/**
	 *	Load frontend styles and scripts
	 *
	 *	@action wp_enqueue_scripts
	 */
	function wp_enqueue_style() {
{{#css}}
		wp_enqueue_style( '{{wp_plugin_slug}}-style', plugins_url( 'css/frontend.css', PLUGIN_FILE ) );
{{/css}}
{{#js}}
		wp_enqueue_script( '{{wp_plugin_slug}}-script', plugins_url( 'js/frontend.js', PLUGIN_FILE ), array( 'jquery' ) );
{{/js}}
	}

	
	/**
	 *	Load text domain
	 * 
	 *  @action plugins_loaded
	 */
	public function load_textdomain() {
		load_plugin_textdomain( '{{wp_plugin_slug}}' , false, PLUGIN_DIRECTORY . '/languages/' );
	}

	/**
	 *	Init hook.
	 * 
	 *  @action init
	 */
	function init() {
	}



	/**
	 *	Fired on plugin activation
	 */
	public static function activate() {
{{#post_types}}
		PostType\{{.}}::activate();
{{/post_types}}
	}

	/**
	 *	Fired on plugin deactivation
	 */
	public static function deactivate() {
{{#post_types}}
		PostType\{{.}}::deactivate();
{{/post_types}}
	}

	/**
	 *	Fired on plugin deinstallation
	 */
	public static function uninstall() {
{{#post_types}}
		PostType\{{.}}::uninstall();
{{/post_types}}
	}

}
