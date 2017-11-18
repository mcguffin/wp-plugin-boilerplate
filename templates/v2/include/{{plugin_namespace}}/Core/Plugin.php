<?php

namespace {{plugin_namespace}}\Core;

if ( ! defined('ABSPATH') ) {
	die('FU!');
}


use {{plugin_namespace}}\PostType;
use {{plugin_namespace}}\Compat;

class Plugin extends Singleton {

	private static $components = array(
{{#modules.model.items}}
		'{{plugin_namespace}}\Model\Model{{module.classname}}',
{{/modules.model.items}}
{{#modules.posttype.items}}
		'{{plugin_namespace}}\PostType\PostType{{module.classname}}',
{{/modules.posttype.items}}
{{#modules.taxonomy.items}}
		'{{plugin_namespace}}\Taxonomy\Taxonomy{{module.classname}}',
{{/modules.taxonomy.items}}
	);

	/**
	 *	@inheritdoc
	 */
	protected function __construct() {

		register_activation_hook( {{plugin_slug_upper}}_FILE, array( __CLASS__ , 'activate' ) );
		register_deactivation_hook( {{plugin_slug_upper}}_FILE, array( __CLASS__ , 'deactivate' ) );
		register_uninstall_hook( {{plugin_slug_upper}}_FILE, array( __CLASS__ , 'uninstall' ) );

		add_action( 'admin_init', array( $this, 'maybe_upgrade' ) );

		parent::__construct();
	}

	/**
	 *	@action plugins_loaded
	 */
	public function maybe_upgrade() {
		// trigger upgrade
		$meta = get_plugin_data( {{plugin_slug_upper}}_FILE );
		$new_version = $meta['Version'];
		$old_version = get_option( '{{plugin_slug}}_version' );

		// call upgrade
		if ( version_compare($new_version, $old_version, '>' ) ) {

			$this->upgrade( $new_version, $old_version );

			update_option( '{{plugin_slug}}_version', $new_version );

		}

	}

	/**
	 *	Fired on plugin activation
	 */
	public static function activate() {


		update_site_option( '{{plugin_slug_lower}}_version', $new_version );

		foreach ( self::$components as $component ) {
			$comp = $component::instance();
			$comp->activate();
		}


	}


	/**
	 *	Fired on plugin updgrade
	 *
	 *	@param string $nev_version
	 *	@param string $old_version
	 *	@return array(
	 *		'success' => bool,
	 *		'messages' => array,
	 * )
	 */
	public function upgrade( $new_version, $old_version ) {

		$result = array(
			'success'	=> true,
			'messages'	=> array(),
		);

		foreach ( self::$components as $component ) {
			$comp = $component::instance();
			$upgrade_result = $comp->upgrade( $new_version, $old_version );
			$result['success'] 		&= $upgrade_result['success'];
			$result['messages'][]	=  $upgrade_result['message'];
		}

		return $result;
	}

	/**
	 *	Fired on plugin deactivation
	 */
	public static function deactivate() {
		foreach ( self::$components as $component ) {
			$comp = $component::instance();
			$comp->deactivate();
		}
	}

	/**
	 *	Fired on plugin deinstallation
	 */
	public static function uninstall() {
		foreach ( self::$components as $component ) {
			$comp = $component::instance();
			$comp->unistall();
		}
	}

}
