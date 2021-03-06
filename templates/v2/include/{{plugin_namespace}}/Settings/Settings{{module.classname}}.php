<?php
/**
 *	@package {{plugin_namespace}}\Settings
 *	@version 1.0.0
 *	2018-09-22
 */

namespace {{plugin_namespace}}\Settings;

if ( ! defined('ABSPATH') ) {
	die('FU!');
}

use {{plugin_namespace}}\Core;

class Settings{{module.classname}} extends Settings {

	private $optionset = '{{settings_section}}';


	/**
	 *	@inheritdoc
	 */
	protected function __construct() {

{{#is_section}}
		add_action( "load-options-{$this->optionset}.php" , array( $this, 'enqueue_assets' ) );
{{/is_section}}
{{#is_page}}
		add_action( "settings_page_{$this->optionset}" , array( $this, 'enqueue_assets' ) );
{{/is_page}}

		add_option( '{{plugin_slug}}_setting_1' , 'Default Value' , '' , False );

{{#module.standalone}}
		add_action( 'admin_menu', array( &$this, 'admin_menu' ) );
{{/module.standalone}}

		parent::__construct();

	}

{{#module.standalone}}
	/**
	 *	Add Settings page
	 *
	 *	@action admin_menu
	 */
	public function admin_menu() {
		add_options_page( __('{{plugin_name}} Settings' , '{{wp_plugin_slug}}' ),__('{{plugin_name}}' , '{{wp_plugin_slug}}'),'manage_options',$this->optionset, array( $this, 'settings_page' ) );
	}

	/**
	 *	Render Settings page
	 */
	public function settings_page() {
		if ( ! current_user_can( 'manage_options' ) ) {
			wp_die( __( 'You do not have sufficient permissions to access this page.' ) );
		}
		?>
		<div class="wrap">
			<h2><?php _e('{{plugin_name}} Settings', '{{wp_plugin_slug}}') ?></h2>

			<form action="options.php" method="post">
				<?php
				settings_fields(  $this->optionset );
				do_settings_sections( $this->optionset );
				submit_button( __('Save Settings' , '{{wp_plugin_slug}}' ) );
				?>
			</form>
		</div><?php
	}
{{/module.standalone}}


	/**
	 * Enqueue settings Assets
	 *
{{#module.standalone}}
	 *	@action load-options-{$this->optionset}.php
{{/module.standalone}}

{{^module.standalone}}
	 *	@action "settings_page_{$this->optionset}
{{/module.standalone}}
	 */
	public function enqueue_assets() {
{{#module.css}}
		wp_enqueue_style( "{{plugin_slug}}-settings-{$this->optionset}", $this->core->get_asset_url( "css/settings-{$this->optionset}.css" ) );
{{/module.css}}

{{#module.js}}
		wp_enqueue_script( "{{plugin_slug}}-settings-{$this->optionset}", $this->core->get_asset_url( "js/settings-{$this->optionset}.js" ) );
		wp_localize_script("{{plugin_slug}}-settings-{$this->optionset}", '{{plugin_slug}}_settings' , array(
		) );
{{/module.js}}
	}


	/**
	 *	Setup options.
	 *
	 *	@action admin_init
	 */
	public function register_settings() {

		$settings_section	= '{{plugin_slug}}_settings';

		add_settings_section( $settings_section, __( 'Section #1',  '{{wp_plugin_slug}}' ), array( $this, 'section_1_description' ), $this->optionset );



		// more settings go here ...
		$option_name		= '{{plugin_slug}}_setting_1';
		register_setting( $this->optionset , $option_name, array( $this , 'sanitize_setting_1' ) );
		add_settings_field(
			$option_name,
			__( 'Setting #1',  '{{wp_plugin_slug}}' ),
			array( $this, 'setting_1_ui' ),
			$this->optionset,
			$settings_section,
			array(
				'option_name'			=> $option_name,
				'option_label'			=> __( 'Setting #1',  '{{wp_plugin_slug}}' ),
				'option_description'	=> __( 'Setting #1 description',  '{{wp_plugin_slug}}' ),
			)
		);
	}

	/**
	 * Print some documentation for the optionset
	 */
	public function section_1_description( $args ) {

		?>
		<div class="inside">
			<p><?php _e( 'Section 1 Description.' , '{{wp_plugin_slug}}' ); ?></p>
		</div>
		<?php
	}

	/**
	 * Output Theme selectbox
	 */
	public function setting_1_ui( $args ) {

		@list( $option_name, $label, $description ) = array_values( $args );

		$option_value = get_option( $option_name );

		?>
			<label for="<?php echo $option_name ?>">
				<input type="text" id="<?php echo $option_name ?>" name="<?php echo $option_name ?>" value="<?php esc_attr_e( $option_value ) ?>" />
				<?php echo $label ?>
			</label>
			<?php
			if ( ! empty( $description ) ) {
				printf( '<p class="description">%s</p>', $description );
			}
			?>
		<?php
	}

	/**
	 * Sanitize value of setting_1
	 *
	 * @return string sanitized value
	 */
	public function sanitize_setting_1( $value ) {
		// do sanitation here!
		return $value;
	}

}
