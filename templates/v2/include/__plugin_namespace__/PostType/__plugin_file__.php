<?php

namespace {{plugin_namespace}}\PostType;
use {{plugin_namespace}}\Core;

class {{plugin_class}} extends PostType {

/*
	private static $_instance = null;
*/

{{#caps}}
	protected $post_type_caps = array(
			'edit_{{post_type_slug}}',
			'read_{{post_type_slug}}',
			'delete_{{post_type_slug}}',
			'edit_{{post_type_slug}}s',
			'edit_others_{{post_type_slug}}s',
			'publish_{{post_type_slug}}s',
			'read_private_{{post_type_slug}}s',
		);
{{/caps}}


	/**
	 * Private constructor
	 */
	protected function __construct() {
		parent::__construct();
		add_action( 'init' , array( &$this , 'register_post_types' ) , 0 );
	}

	/**
	 * Register Post Types
	 * 
	 */
	public function register_post_types( ) {
		// register post type {{post_type_name}}
		$labels = array(
			'name'                => _x( '{{post_type_name}}s', 'Post Type General Name', '{{wp_plugin_slug}}' ),
			'singular_name'       => _x( '{{post_type_name}}', 'Post Type Singular Name', '{{wp_plugin_slug}}' ),
			'menu_name'           => __( '{{post_type_name}}', '{{wp_plugin_slug}}' ),
			'parent_item_colon'   => __( 'Parent Item:', '{{wp_plugin_slug}}' ),
			'all_items'           => __( 'All Items', '{{wp_plugin_slug}}' ),
			'view_item'           => __( 'View Item', '{{wp_plugin_slug}}' ),
			'add_new_item'        => __( 'Add New Item', '{{wp_plugin_slug}}' ),
			'add_new'             => __( 'Add New', '{{wp_plugin_slug}}' ),
			'edit_item'           => __( 'Edit Item', '{{wp_plugin_slug}}' ),
			'update_item'         => __( 'Update Item', '{{wp_plugin_slug}}' ),
			'search_items'        => __( 'Search Item', '{{wp_plugin_slug}}' ),
			'not_found'           => __( 'Not found', '{{wp_plugin_slug}}' ),
			'not_found_in_trash'  => __( 'Not found in Trash', '{{wp_plugin_slug}}' ),
		);

{{#caps}}
		$capabilities = array_combine( array(
			'edit_post',
			'read_post',
			'delete_post',
			'edit_posts',
			'edit_others_posts',
			'publish_posts',
			'read_private_posts',
		), $this->post_type_caps );
{{/caps}}

		$args = array(
			'label'               => __( '{{post_type_name}}', '{{wp_plugin_slug}}' ),
			'description'         => __( '{{post_type_name}} Description', '{{wp_plugin_slug}}' ),
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
{{#caps}}
			'capabilities'        => $capabilities,
{{/caps}}
{{^caps}}
			'capability_type'     => 'post',
{{/caps}}

		);
		register_post_type( '{{post_type_slug}}', $args );
	}

}

