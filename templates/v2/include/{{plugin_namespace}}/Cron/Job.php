<?php
/**
 *	@package {{plugin_namespace}}\Cron
 *	@version 1.0.0
 *	2018-09-22
 */

namespace CalendarImporter\Cron;

if ( ! defined('ABSPATH') ) {
	die('FU!');
}


class Job {

	/**
	 *	@var callable
	 */
	private $callback;

	/**
	 *	@var string
	 */
	private $hook;

	/**
	 *	@var string
	 */
	private $schedule;


	/**
	 *	@param	string		$hook
	 *	@param	callable	$callback
	 *	@param	array		$args
	 *	@param	string		$schedule
	 */
	public function __construct( $hook, $callback, $args = array(), $schedule = 'hourly' ) {

		$this->hook		= $hook;
		$this->callback	= $callback;
		$this->schedule	= $schedule;
		$this->args		= $args;

	}


	/**
	 *	@return Cron\Job
	 */
	public function start() {
		Cron::instance()->register_job( $this );

		if ( ! wp_next_scheduled( $this->hook, $this->args ) ) {
			$result = wp_schedule_event( time(), $this->schedule, $this->hook, $this->args );
		}

		return $this;
	}

	/**
	 *	@return Cron\Job
	 */
	public function stop() {

		Cron::instance()->unregister_job( $this );

		//*
		if ( $time = wp_next_scheduled( $this->hook, $this->args ) ) {
			wp_unschedule_event( $time, $this->hook, $this->args );
		}
		/*/
		wp_clear_scheduled_hook( $this->hook, $this->args );
		//*/
		return $this;
	}

	/**
	 *	@return string
	 */
	public function get_hook() {
		return $this->hook;
	}

	/**
	 *	@return string
	 */
	public function get_key() {
		return md5( var_export( $this->callback, true ) . var_export( $this->args, true ) );
	}

	/**
	 *	@return callable
	 */
	public function get_callback() {
		return $this->callback;
	}

}
