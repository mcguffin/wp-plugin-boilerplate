<?php


namespace {{plugin_namespace}}\Model;

class ModelSchedules extends Model {

	/**
	 *	@inheritdoc
	 */
	protected $_table = '{{model_slug}}';

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

		$sql = "CREATE TABLE $wpdb->{{model_slug}} (
			`id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
			`post_id` bigint(20) NOT NULL,
			`dtstart` datetime NOT NULL,
			`dtend` datetime NOT NULL,
			`all_day` tinyint(1) NOT NULL,
			PRIMARY KEY (`id`),
			KEY dtstart (dtstart),
			KEY dtend (dtend)
		) $charset_collate;";

		// updates DB
		dbDelta( $sql );
	}
}
