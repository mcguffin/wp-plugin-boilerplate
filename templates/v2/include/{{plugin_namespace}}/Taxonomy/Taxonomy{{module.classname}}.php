<?php
/**
 *	@package {{plugin_namespace}}\Taxonomy
 *	@version 1.0.0
 *	2018-09-22
 */

namespace {{plugin_namespace}}\Taxonomy;

if ( ! defined('ABSPATH') ) {
	die('FU!');
}


class Taxonomy{{module.classname}} extends Taxonomy {

	/**
	 *	@inheritdoc
	 */
	protected $taxonomy_slug = '{{module.slug}}';


	/**
	 *	Register taxonomy
	 */
	public function register_taxonomy( ) {

		// labels
		$labels = array(
			'name'              => _x( '{{module.name}}s', 'taxonomy general name' , '{{wp_plugin_slug}}' ),
			'singular_name'     => _x( '{{module.name}}', 'taxonomy singular name' , '{{wp_plugin_slug}}' ),
			'search_items'      => __( 'Search {{module.name}}s' , '{{wp_plugin_slug}}' ),
			'all_items'         => __( 'All {{module.name}}s' , '{{wp_plugin_slug}}' ),
			'parent_item'       => __( 'Parent {{module.name}}' , '{{wp_plugin_slug}}' ),
			'parent_item_colon' => __( 'Parent {{module.name}}:' , '{{wp_plugin_slug}}' ),
			'edit_item'         => __( 'Edit {{module.name}}' , '{{wp_plugin_slug}}' ),
			'update_item'       => __( 'Update {{module.name}}' , '{{wp_plugin_slug}}' ),
			'add_new_item'      => __( 'Add New {{module.name}}' , '{{wp_plugin_slug}}' ),
			'new_item_name'     => __( 'New {{module.name}}' , '{{wp_plugin_slug}}' ),
			'menu_name'         => __( '{{module.name}}s' , '{{wp_plugin_slug}}' ),
			'popular_items'		=> null,
		);

		$args = array(
			'hierarchical'		=> false,
			'labels'			=> $labels,
			'show_ui'			=> true,
			'public'			=> true,
			'show_admin_column' => true,
//			'meta_box_cb'		=> false,
		);

		register_taxonomy( $this->taxonomy_slug, array(), $args );

	}


}
