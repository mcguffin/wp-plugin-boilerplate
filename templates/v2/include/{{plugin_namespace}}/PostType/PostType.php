<?php

namespace {{plugin_namespace}}\PostType;

if ( ! defined('ABSPATH') ) {
	die('FU!');
}

use {{plugin_namespace}}\Core;

abstract class PostType extends Core\PluginComponent {

	protected $post_type_caps = null;

	/**
	 *	@inheritdoc
	 */
	protected function __construct() {
		parent::__construct();
		add_action( 'init' , array( &$this , 'register_post_types' ) , 0 );
	}

	/**
	 *	Register Post Type
	 *
	 *	@action init
	 */
	abstract function register_post_types();

	/**
	 *	@inheritdoc
	 */
	public function activate() {
		// register post types, taxonomies
		$this->register_post_types();

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

		$deleted_posts = 0;
		$posts = get_posts(array(
			'post_type' 		=> $this->post_type_slug,
			'post_status'		=> 'any',
			'posts_per_page'	=> -1,
		));
		foreach ( $posts as $post ) {
			wp_delete_post( $post->ID, true );
			$deleted_posts++;
		}

		return array(
			'success'	=> true,
			'messages'	=> array(
				sprintf( _n( 'Deleted %d Post',  'Deleted %d Posts', $deleted_posts, '{{plugin_slug}}' ), $deleted_posts ),
			),
		);
	}

	/**
	 *	@inheritdoc
	 */
	public function upgrade( $new_version, $old_version ) {
	}



	protected function add_custom_capabilities() {
		if ( ! is_null( $this->post_type_caps ) ) {
			$admin_role = get_role('administrator');
			if ( ! is_null($admin_role) ) {
				foreach ( $this->post_type_caps as $cap ) {
					if ( ! $admin_role->has_cap($cap) ) {
						$admin_role->add_cap($cap);
						error_log('add cap: '.$cap);
					}
				}
			} else {
				// error case!
			}
		}
	}

	/**
	 *	Remove custom capabilities from all roles
	 */
	protected function remove_custom_capabilities() {
		// all roles!
		global $wp_roles;
		$roles = $wp_roles->roles;
		foreach ( array_keys( $wp_roles->roles ) as $role_slug ) {
			$role = get_role($role_slug);
			foreach ( $this->_post_type_caps as $cap ) {
				if ( $role->has_cap($cap) ) {
					$role->remove_cap($cap);
					error_log('rm cap '.$cap.' role: '.$role_slug);
				}
			}
		}
	}

}
