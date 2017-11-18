<?php

namespace {{plugin_namespace}}\Taxonomy;

if ( ! defined('ABSPATH') ) {
	die('FU!');
}


use {{plugin_namespace}}\Core;

abstract class Taxonomy extends Core\PluginComponent {

	protected $taxonomy_slug;

	abstract function register_taxonomy();

	/**
	 *	@inheritdoc
	 */
	public function activate() {
		// register post types, taxonomies
		$this->register_taxonomy();

		// flush rewrite rules
		flush_rewrite_rules();

		return array(
			'success'	=> true,
			'messages'	=> array(),
		);
	}

	/**
	 *	@inheritdoc
	 */
	public function deactivate() {

		// flush rewrite rules
		flush_rewrite_rules();

		return array(
			'success'	=> true,
			'messages'	=> array(),
		);
	}

	/**
	 *	@inheritdoc
	 */
	public function uninstall() {

		$deleted_terms = 0;

		$terms = get_terms( array(
			'taxonomy' 		=> $this->taxonomy_slug,
			'hide_empty'	=> false,
		));

		foreach ( $terms as $term ) {

			wp_delete_term( $term->term_id, $this->taxonomy_slug );

			$deleted_terms ++;

		}


		return array(
			'success'	=> true,
			'messages'	=> array(
				sprintf( _n( 'Deleted %d Term',  'Deleted %d Terms', $deleted_terms, '{{plugin_slug}}' ), $deleted_terms ),
			),
		);
	}

	/**
	 *	@inheritdoc
	 */
	public function upgrade( $new_version, $old_version ) {

		return array(
			'success'	=> true,
			'messages'	=> array(),
		);

	}


}
