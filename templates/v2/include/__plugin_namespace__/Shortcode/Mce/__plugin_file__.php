<?php


namespace {{plugin_namespace}}\Shortcode\Mce;
use {{plugin_namespace}}\Admin\Mce;

class {{plugin_class}} extends Mce\Mce {
	
	protected $module_name = '{{shortcode_slug}}-shortcode';

	protected $editor_buttons = array(
		'mce_buttons_2' => array(
			'{{shortcode_slug}}'	=> -1,
		),
	);
	
	protected $toolbar_css	= true;

	protected $editor_css	= true;
	
	protected function __construct() {
		$this->plugin_params = array(
			'l10n' => array(
				'insert_{{shortcode_slug}}'	=> __( 'Insert {{shortcode_name}}', '{{wp_plugin_slug}}' ),
			),
		);

		parent::__construct();
	}
}