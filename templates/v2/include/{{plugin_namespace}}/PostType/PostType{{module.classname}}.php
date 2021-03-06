<?php
/**
 *	@package {{plugin_namespace}}\PostType
 *	@version 1.0.0
 *	2018-09-22
 */

namespace {{plugin_namespace}}\PostType;

if ( ! defined('ABSPATH') ) {
	die('FU!');
}

use {{plugin_namespace}}\Core;

class PostType{{module.classname}} extends PostType {

	/**
	 *	@var string
	 */
	protected $post_type_slug = '{{module.slug}}';

{{#module.caps}}
	/**
	 *	@var array
	 */
	protected $post_type_caps = array(
			'edit_{{module.slug}}',
			'read_{{module.slug}}',
			'delete_{{module.slug}}',
			'edit_{{module.slug}}s',
			'edit_others_{{module.slug}}s',
			'publish_{{module.slug}}s',
			'read_private_{{module.slug}}s',
		);
{{/module.caps}}


	/**
	 *	@inheritdoc
	 */
	public function register_post_types( ) {
		// register post type {{module.name}}
		$labels = array(
			'name'                => _x( '{{module.name}}s', 'Post Type General Name', '{{wp_plugin_slug}}' ),
			'singular_name'       => _x( '{{module.name}}', 'Post Type Singular Name', '{{wp_plugin_slug}}' ),
			'menu_name'           => __( '{{module.name}}', '{{wp_plugin_slug}}' ),
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

{{#module.caps}}
		$capabilities = array_combine( array(
			'edit_post',
			'read_post',
			'delete_post',
			'edit_posts',
			'edit_others_posts',
			'publish_posts',
			'read_private_posts',
		), $this->post_type_caps );
{{/module.caps}}

		$args = array(
			'label'               => __( '{{module.name}}', '{{wp_plugin_slug}}' ),
			'description'         => __( '{{module.name}} Description', '{{wp_plugin_slug}}' ),
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
{{#module.caps}}
			'capabilities'        => $capabilities,
{{/module.caps}}
{{^module.caps}}
			'capability_type'     => 'post',
{{/module.caps}}

		);
		register_post_type( $this->post_type_slug, $args );
	}

}
