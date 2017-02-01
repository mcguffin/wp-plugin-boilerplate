<?php

namespace {{plugin_namespace}}\Settings;
use {{plugin_namespace}}\Core;

class {{settings_class}} extends Settings {

	private $optionset = '{{settings_section}}'; 


	/**
	 *	Constructor
	 */
	protected function __construct() {

{{#flags}}
{{#is_section}}
		add_action( "load-options-{$this->optionset}.php" , array( &$this , 'enqueue_assets' ) );
{{/is_section}}
{{#is_page}}
		add_action( "settings_page_{$this->optionset}" , array( &$this , 'enqueue_assets' ) );
{{/is_page}}
{{/flags}}

		add_option( '{{plugin_slug}}_setting_1' , 'Default Value' , '' , False );

{{#is_page}}
		add_action( 'admin_menu', array( &$this, 'admin_menu' ) );
{{/is_page}}

		parent::__construct();

	}

{{#is_page}}
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
{{/is_page}}


{{#flags}}
	/**
	 * Enqueue settings Assets
	 *
{{#is_section}}
	 *	@action load-options-{$this->optionset}.php
{{/is_section}}
{{#is_page}}
	 *	@action "settings_page_{$this->optionset}
{{/is_page}}
	 */
	public function enqueue_assets() {
{{#css}}
		wp_enqueue_style( "{{plugin_slug}}-settings-{$this->optionset}", $this->core->get_asset_url( "css/settings-{$this->optionset}.css" ) );
{{/css}}

{{#js}}
		wp_enqueue_script( "{{plugin_slug}}-settings-{$this->optionset}", $this->core->get_asset_url( "js/settings-{$this->optionset}.js" ) );
		wp_localize_script("{{plugin_slug}}-settings-{$this->optionset}", '{{plugin_slug}}_settings' , array(
		) );
{{/js}}
	}
{{/flags}}


	/**
	 *	Setup options.
	 *
	 *	@action admin_init
	 */
	public function register_settings() {

		$settings_section = '{{plugin_slug}}_settings';

		// more settings go here ...
		register_setting( $this->optionset , '{{plugin_slug}}_setting_1' , array( &$this , 'sanitize_setting_1' ) );

		add_settings_section( $settings_section, __( 'Section #1',  '{{wp_plugin_slug}}' ), array( &$this, 'section_1_description' ), $this->optionset );

		// ... and here
		add_settings_field(
			'{{plugin_slug}}_setting_1',
			__( 'Setting #1',  '{{wp_plugin_slug}}' ),
			array( $this, 'setting_1_ui' ),
			$this->optionset,
			$settings_section
		);
	}

	/**
	 * Print some documentation for the optionset
	 */
	public function section_1_description() {
		?>
		<div class="inside">
			<p><?php _e( 'Section 1 Description.' , '{{wp_plugin_slug}}' ); ?></p>
		</div>
		<?php
	}

	/**
	 * Output Theme selectbox
	 */
	public function setting_1_ui( ) {
		$setting_name = '{{plugin_slug}}_setting_1';
		$setting = get_option($setting_name);
		?><input type="text" name="<?php echo $setting_name ?>" value="<?php esc_attr_e( $setting ) ?>" /><?php
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