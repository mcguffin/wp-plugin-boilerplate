<?php

namespace {{plugin_namespace}};

function __autoload( $class ) {
	if ( strpos( $class, '{{plugin_namespace}}\\' ) === false ) {
		// not our plugin.
		return;
	}
	$ds = DIRECTORY_SEPARATOR;
	$file = {{plugin_slug_upper}}_DIRECTORY . 'include' . $ds . str_replace( '\\', $ds, $class ) . '.php';

	if ( file_exists( $file ) ) {
		require_once $file;
	} else {
		throw new \Exception( sprintf( 'Class `%s` could not be loaded. File `%s` not found.', $class, $file ) );
	}
}


spl_autoload_register( '{{plugin_namespace}}\__autoload' );