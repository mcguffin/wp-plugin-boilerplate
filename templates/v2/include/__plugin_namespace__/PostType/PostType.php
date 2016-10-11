<?php

namespace {{plugin_namespace}}\PostType;

abstract class PostType {
	protected $post_type_caps = null;
	
	abstract function register_post_types();

	public static function activate() {
		$self = get_called_class();
		$inst = $self::instance();
		$inst->register_post_types();
		$inst->add_custom_capabilities();
		flush_rewrite_rules();
	}

	public static function deactivate() {
		flush_rewrite_rules();
	}

	public static function uninstall() {
		$self = get_called_class();
		$inst = $self::instance();
		$inst->remove_custom_capabilities();
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

