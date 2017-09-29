<?php


/*  Copyright 2015  Jörn Lund

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

namespace {{plugin_namespace}}\PostType;

class Taxonomy{{plugin_class}} extends Taxonomy {

	/**
	 *	Register taxonomy
	 */
	public function register_taxonomy( ) {

		// labels
		$labels = array(
			'name'              => _x( '{{taxonomy_name}}s', 'taxonomy general name' , '{{wp_plugin_slug}}' ),
			'singular_name'     => _x( '{{taxonomy_name}}', 'taxonomy singular name' , '{{wp_plugin_slug}}' ),
			'search_items'      => __( 'Search {{taxonomy_name}}s' , '{{wp_plugin_slug}}' ),
			'all_items'         => __( 'All {{taxonomy_name}}s' , '{{wp_plugin_slug}}' ),
			'parent_item'       => __( 'Parent {{taxonomy_name}}' , '{{wp_plugin_slug}}' ),
			'parent_item_colon' => __( 'Parent {{taxonomy_name}}:' , '{{wp_plugin_slug}}' ),
			'edit_item'         => __( 'Edit {{taxonomy_name}}' , '{{wp_plugin_slug}}' ),
			'update_item'       => __( 'Update {{taxonomy_name}}' , '{{wp_plugin_slug}}' ),
			'add_new_item'      => __( 'Add New {{taxonomy_name}}' , '{{wp_plugin_slug}}' ),
			'new_item_name'     => __( 'New {{taxonomy_name}}' , '{{wp_plugin_slug}}' ),
			'menu_name'         => __( '{{taxonomy_name}}s' , '{{wp_plugin_slug}}' ),
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
