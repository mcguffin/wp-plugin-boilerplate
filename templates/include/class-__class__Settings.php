<?php


if ( ! class_exists( '{{plugin_class_name}}Settings' ) ):
class {{plugin_class_name}}Settings {
	private static $_instance = null;
	
{{#settings_section}}
	/**
	 * Setup which to WP options page the Rainbow options will be added.
	 * 
	 * Possible values: general | writing | reading | discussion | media | permalink
	 */
	private $optionset = 'general'; // writing | reading | discussion | media | permalink
{{/settings_section}}
{{#settings_page}}
	private $optionset = '{{plugin_slug}}_options'; // writing | reading | discussion | media | permalink
{{/settings_page}}

	/**
	 * Getting a singleton.
	 *
	 * @return object single instance of {{plugin_class_name}}Settings
	 */
	public static function instance() {
		if ( is_null( self::$_instance ) )
			self::$_instance = new self();
		return self::$_instance;
	}

	/**
	 * Private constructor
	 */
	private function __construct() {
		add_action( 'admin_init' , array( &$this , 'register_settings' ) );
{{#settings_assets}}

{{#settings_section}}
		add_action( "load-options-{$this->optionset}.php" , array( &$this , 'enqueue_assets' ) );
{{/settings_section}}
{{#settings_page}}
		add_action( "settings_page_{$this->optionset}" , array( &$this , 'enqueue_assets' ) );
{{/settings_page}}
{{/settings_assets}}
		
		add_option( '{{plugin_slug}}_setting_1' , 'Default Value' , '' , False );
{{#settings_page}}
		add_action( 'admin_menu', array( &$this, 'admin_menu' ) );
{{/settings_page}}
	}
{{#settings_page}}
	function admin_menu() {
		add_options_page( __('{{plugin_name}} Settings' , '{{wp_plugin_slug}}' ),__('{{plugin_name}}' , '{{wp_plugin_slug}}'),'manage_options',$this->optionset, array( $this, 'settings_page' ) );
	}
	function settings_page() {
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
{{/settings_page}}

	/**
	 * Enqueue options Assets
	 */
	function enqueue_assets() {
{{#settings_css}}
		wp_enqueue_style( '{{plugin_slug}}-settings' , plugins_url( '/css/{{plugin_slug}}-settings.css' , dirname(__FILE__) ));
{{/settings_css}}

{{#settings_js}}
		wp_enqueue_script( '{{plugin_slug}}-settings' , plugins_url( 'js/{{plugin_slug}}-settings.js' , dirname(__FILE__) ) );
		wp_localize_script('{{plugin_slug}}-settings' , '{{plugin_slug}}_settings' , array(
		) );
{{/settings_js}}
	}
	


	/**
	 * Setup options page.
	 */
	function register_settings() {
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
	public function setting_1_ui(){
		$setting_name = '{{plugin_slug}}_setting_1';
		$setting = get_option($setting_name);
		?><input type="text" name="<?php echo $setting_name ?>" value="<?php esc_attr_e( $setting ) ?>" /><?php
	}
	

	/**
	 * Sanitize value of setting_1
	 *
	 * @return string sanitized value
	 */
	function sanitize_setting_1( $value ) {	
		// do sanitation here!
		return $value;
	}
}

{{plugin_class_name}}Settings::instance();
endif;