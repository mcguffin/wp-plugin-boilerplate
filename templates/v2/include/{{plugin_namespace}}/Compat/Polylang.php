<?php
/**
 *	@package {{plugin_namespace}}\Compat
 *	@version 1.0.0
 *	2018-09-22
 */

namespace {{plugin_namespace}}\Compat;

if ( ! defined('ABSPATH') ) {
	die('FU!');
}


use {{plugin_namespace}}\Core;


class Polylang extends Core\PluginComponent {

	protected function __construct() {
	}

	/**
	 *	@inheritdoc
	 */
	 public function activate(){

	 }

	 /**
	  *	@inheritdoc
	  */
	 public function deactivate(){

	 }

	 /**
	  *	@inheritdoc
	  */
	 public function uninstall() {
		 // remove content and settings
	 }

	/**
 	 *	@inheritdoc
	 */
	public function upgrade( $new_version, $old_version ) {
	}

}
