<?php

namespace {{plugin_namespace}}\AutoUpdate;

use GitupdateTest\Core;

class AutoUpdatePodpirate extends AutoUpdate {

	private $info_url = 'https://download.podpirate.org/info/%s/%s/release.json';


	/**
	 *	@var string plugin | theme
	 */
	protected $type = null;

	/**
	 *	@var string plugins | themes
	 */
	protected $dl_prefix = null;

	/**
	 *	@param string $type plugin | theme
	 */
	public function set_type( $type ) {
		$this->type = $type;
		$this->dl_prefix = $type . 's';
	}

	/**
	 *	@inheritdoc
	 */
	public function get_remote_release_info() {
		error_log('REMOTE CHECK');
		error_log(var_export($this->get_release_info_url(),true));

		if ( $release_info_url = $this->get_release_info_url() ) {

			$response = wp_remote_get( $release_info_url, array() );
			$slug = basename( {{plugin_slug_upper}}_DIRECTORY );

			if ( ! is_wp_error( $response ) ) {
				$release_info = json_decode( wp_remote_retrieve_body( $response ) );
				$release_info->download_link = add_query_arg(array(
					'token' => $this->get_access_token(),
					'domain'	=> preg_replace( '/https?:\/\/([a-z0-9.-])\/?/','\1',get_option('home')),
				), $release_info->download_link );
				error_log(var_export($release_info->download_link,true));

				return $release_info;
			} else {
				error_log($response->get_error_message());
			}
		}

		return false;
	}

	/**
	 *	@inheritdoc
	 */
	protected function get_plugin_sections() {
		$release_info = $this->get_release_info();
		return $release_info['sections'];
	}

	/**
	 *	@inheritdoc
	 */
	protected function get_plugin_banners() {
		return array();
	}


	/**
	 *	@return	string	access token
	 */
	private function get_access_token() {
		if ( $token = get_option('podpirate_access_token') ) {
			return $token;
		}
		if ( defined( 'PODPIRATE_ACCESS_TOKEN' ) ) {
			return PODPIRATE_ACCESS_TOKEN;
		}
		return apply_filters( 'podpirate_access_token', '' );
	}

	/**
	 *	@return	string	github api url
	 */
	private function get_release_info_url() {

		if ( $token = $this->get_access_token() ) {
			$slug = basename( {{plugin_slug_upper}}_DIRECTORY );
			return sprintf( $this->info_url, $this->dl_prefix, $slug );
		}
		return false;
	}

}
