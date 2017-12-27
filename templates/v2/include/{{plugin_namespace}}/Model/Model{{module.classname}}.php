<?php


namespace {{plugin_namespace}}\Model;

if ( ! defined('ABSPATH') ) {
	die('FU!');
}


class Model{{module.classname}} extends Model {

	protected $fields = array(
		'ID'	=> '%d',
//		'title'	=> '%s',
//		...
	);


	/**
	 *	@inheritdoc
	 */
	protected $_table = '{{module.slug}}';

	/**
	 *	@inheritdoc
	 */
	public function activate() {
		// create table
		$this->update_db();
	}

	/**
	 *	@inheritdoc
	 */
	public function upgrade( $new_version, $old_version ) {
		$this->update_db();
	}

	/**
	 *	@inheritdoc
	 */
	private function update_db(){
		global $wpdb, $charset_collate;

		require_once(ABSPATH . 'wp-admin/includes/upgrade.php');

		$sql = "CREATE TABLE $wpdb->{{module.slug}} (
			`ID` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
			PRIMARY KEY (`id`)
		) $charset_collate;";

		// updates DB
		dbDelta( $sql );
	}
}
