<?php

namespace {{plugin_namespace}};

function __autoload( $class ) {
	$ds = DIRECTORY_SEPARATOR;
	$file = PLUGIN_DIRECTORY . 'include' . $ds . str_replace( '\\', $ds, $class ) . '.php';
	if ( file_exists( $file ) ) {
		require_once $file;
	}
}

spl_autoload_register( '{{plugin_namespace}}\__autoload' );