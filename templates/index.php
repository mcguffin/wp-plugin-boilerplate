<?php

/*
Plugin Name: {{plugin_name}}
Plugin URI: http://wordpress.org/
Description: Enter description here.
Author: {{plugin_author}}
Version: 1.0.0
Author URI: {{plugin_author_uri}}
License: GPL3

Text Domain: {{plugin_slug}}
Domain Path: /languages/
*/

/*  Copyright {{this_year}}  {{plugin_author}}

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License, version 2, as 
    published by the Free Software Foundation.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
*/


if ( ! class_exists( '{{plugin_class_name}}' ) ):
class {{plugin_class_name}} {
	private static $_instance = null;

	/**
	 * Getting a singleton.
	 *
	 * @return object single instance of {{plugin_class_name}}
	 */
	public static function get_instance() {
		if ( is_null( self::$_instance ) )
			self::$_instance = new self();
		return self::$_instance;
	}

	/**
	 * Private constructor
	 */
	private function __construct() {
		add_action( 'plugins_loaded' , array( &$this , 'load_textdomain' ) );
		add_action( 'init' , array( &$this , 'init' ) );
{{#post_type}}		add_action( 'init' , array( &$this , 'register_post_type' ) , 0 );
{{/post_type}}
		add_action( 'wp_enqueue_scripts' , array( &$this , 'enqueue_assets' ) );
		{{#shortcodes}}
		add_shortcode( '{{.}}' , array( &$this , 'shortcode_{{.}}' ) );
		{{/shortcodes}}
	}

	/**
	 * Load text domain
	 */
	public function load_textdomain() {
		load_plugin_textdomain( '{{plugin_slug}}' , false, dirname( plugin_basename( __FILE__ ) ) . '/languages/' );
	}
	/**
	 * Init hook.
	 * 
	 *  - Register assets
	 */
	function init() {
{{#frontend_js}}		wp_register_script( '{{plugin_slug}}' , plugins_url( '/js/{{plugin_slug}}.js' , __FILE__ ) , array() , false , true );
{{/frontend_js}}{{#frontend_css}}		wp_register_style( '{{plugin_slug}}' , plugins_url( '/css/{{plugin_slug}}.css' , __FILE__ ) , array() , '1.0' );
{{/frontend_css}}
	}
	/**
	 *  Enqueue Frontend Scripts
	 */
	function enqueue_assets() {	
		wp_enqueue_script( '{{plugin_slug}}' );
		wp_enqueue_style( '{{plugin_slug}}' );
	}

{{#shortcodes}}
	/**
	 * Init hook.
	 * 
	 *  - Register assets
	 */
	public function shortcode_{{.}}( $atts , $content = null ) {
		$atts = shortcode_atts( array(
			'default_attr' => 'Default Value',
		), $atts );
		return $content;
	}
{{/shortcodes}}

{{#post_type}}
	/**
	 * Init hook.
	 * 
	 *  - Register assets
	 */
	public function register_post_type( $atts , $content = null ) {
		$labels = array(
			'name'                => _x( '{{post_type}}s', 'Post Type General Name', '{{plugin_slug}}' ),
			'singular_name'       => _x( '{{post_type}}', 'Post Type Singular Name', '{{plugin_slug}}' ),
			'menu_name'           => __( '{{post_type}}', '{{plugin_slug}}' ),
			'parent_item_colon'   => __( 'Parent Item:', '{{plugin_slug}}' ),
			'all_items'           => __( 'All Items', '{{plugin_slug}}' ),
			'view_item'           => __( 'View Item', '{{plugin_slug}}' ),
			'add_new_item'        => __( 'Add New Item', '{{plugin_slug}}' ),
			'add_new'             => __( 'Add New', '{{plugin_slug}}' ),
			'edit_item'           => __( 'Edit Item', '{{plugin_slug}}' ),
			'update_item'         => __( 'Update Item', '{{plugin_slug}}' ),
			'search_items'        => __( 'Search Item', '{{plugin_slug}}' ),
			'not_found'           => __( 'Not found', '{{plugin_slug}}' ),
			'not_found_in_trash'  => __( 'Not found in Trash', '{{plugin_slug}}' ),
		);
		$args = array(
			'label'               => __( '{{post_type}}', '{{plugin_slug}}' ),
			'description'         => __( '{{post_type}} Description', '{{plugin_slug}}' ),
			'labels'              => $labels,
			'supports'            => array( 'title' , 'editor' ),
			'taxonomies'          => array( ),
			'hierarchical'        => false,
			'public'              => true,
			'show_ui'             => true,
			'show_in_menu'        => true,
			'show_in_nav_menus'   => true,
			'show_in_admin_bar'   => true,
			'menu_position'       => 25,
			'can_export'          => true,
			'has_archive'         => true,
			'exclude_from_search' => false,
			'publicly_queryable'  => true,
			'capability_type'     => 'page',
		);
		register_post_type( '{{post_type}}', $args );		
	}
{{/post_type}}

{{#post_type_with_caps}}
	/**
	 * Init hook.
	 * 
	 *  - Register assets
	 */
	public function register_post_type_with_caps( $atts , $content = null ) {
		$labels = array(
			'name'                => _x( '{{post_type_with_caps}}s', 'Post Type General Name', '{{plugin_slug}}' ),
			'singular_name'       => _x( '{{post_type_with_caps}}', 'Post Type Singular Name', '{{plugin_slug}}' ),
			'menu_name'           => __( '{{post_type_with_caps}}', '{{plugin_slug}}' ),
			'parent_item_colon'   => __( 'Parent Item:', '{{plugin_slug}}' ),
			'all_items'           => __( 'All Items', '{{plugin_slug}}' ),
			'view_item'           => __( 'View Item', '{{plugin_slug}}' ),
			'add_new_item'        => __( 'Add New Item', '{{plugin_slug}}' ),
			'add_new'             => __( 'Add New', '{{plugin_slug}}' ),
			'edit_item'           => __( 'Edit Item', '{{plugin_slug}}' ),
			'update_item'         => __( 'Update Item', '{{plugin_slug}}' ),
			'search_items'        => __( 'Search Item', '{{plugin_slug}}' ),
			'not_found'           => __( 'Not found', '{{plugin_slug}}' ),
			'not_found_in_trash'  => __( 'Not found in Trash', '{{plugin_slug}}' ),
		);
		$capabilities = array(
			'edit_post'           => 'edit_{{post_type_with_caps}}',
			'read_post'           => 'read_{{post_type_with_caps}}',
			'delete_post'         => 'delete_{{post_type_with_caps}}',
			'edit_posts'          => 'edit_{{post_type_with_caps}}s',
			'edit_others_posts'   => 'edit_others_{{post_type_with_caps}}s',
			'publish_posts'       => 'publish_{{post_type_with_caps}}s',
			'read_private_posts'  => 'read_private_{{post_type_with_caps}}s',
		);
		$args = array(
			'label'               => __( '{{post_type_with_caps}}', '{{plugin_slug}}' ),
			'description'         => __( '{{post_type_with_caps}} Description', '{{plugin_slug}}' ),
			'labels'              => $labels,
			'supports'            => array( 'title' , 'editor' ),
			'taxonomies'          => array( ),
			'hierarchical'        => false,
			'public'              => true,
			'show_ui'             => true,
			'show_in_menu'        => true,
			'show_in_nav_menus'   => true,
			'show_in_admin_bar'   => true,
			'menu_position'       => 25,
			'can_export'          => true,
			'has_archive'         => true,
			'exclude_from_search' => false,
			'publicly_queryable'  => true,
			'capabilities'        => $capabilities,
		);
		register_post_type( '{{post_type_with_caps}}', $args );
	}
{{/post_type_with_caps}}

}
{{plugin_class_name}}::get_instance();

endif;

{{#widget}}require_once plugin_dir_path(__FILE__) . 'include/class-{{plugin_class_name}}_Widget.php';
{{/widget}}
{{#backend}}if ( is_admin() ) {
{{#admin}}	require_once plugin_dir_path(__FILE__) . 'include/class-{{plugin_class_name}}Admin.php';
{{/admin}}
{{#settings}}	require_once plugin_dir_path(__FILE__) . 'include/class-{{plugin_class_name}}Settings.php';
{{/settings}}
}
{{/backend}}
