tinymce.PluginManager.add( '{{module.slug_underscore}}_shortcode' , function( editor ) {

	var placeholder_img			= tinymce.Env.transparentSrc,
		l10n					= mce_{{module.slug_underscore}}_shortcode.l10n,
		placeholder_img			= 'data:image/svg+xml;base64,' + window.btoa('<svg version="1.1" id="Ebene_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="500px" height="40px" viewBox="0 0 500 40"><text transform="matrix(1 0 0 1 12.5127 22.9082)" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Oxygen-Sans,Ubuntu,Cantarell,\'Helvetica Neue\',sans-serif" font-size="12" style="fill: #FFFFFF;stroke:none;font-weight:bold;">'+l10n.name+'</text></svg>'),

		// https://stackoverflow.com/questions/34393501/regex-for-processing-wordpress-shortcode
		the_shortcode			= /\[{{module.slug_underscore}}([^\]]*)\]([\s\S]*?)\[\/{{module.slug_underscore}}\]/g,
		the_visible_shortcode	= '<img title="'+l10n.name+'" data-attr="{attr}" data-wp-entity="cateringcalendar" src="'+placeholder_img+'" data-mce-resize="false" data-mce-placeholder="1" />';

	function nodeStr( node ) {
		var txt, ax, $el = jQuery("<div />");
		$el.append( node.cloneNode(false) );
		return $el.html();
	}

	function replaceShortcodes( content ) {
		return content.replace( the_shortcode, function( all, attr ) {
			var attr = window.encodeURIComponent( attr );
			return the_visible_shortcode.replace('{attr}', attr );
		});
	}
	function restoreShortcodes( content ) {
		//match any image tag with our class and replace it with the shortcode's content and attributes
		return content.replace( /(?:<p(?: [^>]+)?>)*(<img [^>]+>)(?:<\/p>)*/g, function( match, image ) {
			var attr = jQuery( image ).attr('data-attr'),
				attr = window.decodeURIComponent( attr );

			if ( attr ) {
				return '\
\
[{{module.slug_underscore}} ' + attr + ']\
\
		';
			}
			return match;
		});
	}
	function openShortcodeDialog( callback, values ) {
		var sel		= editor.selection.getNode(),
			$sel	= jQuery( sel ),
			d = {
				sources	: '',
				period	: 'this-week'
			},
			str, wpsh;

		if ( $sel.is('[data-wp-entity="{{module.slug_underscore}}"]') ) {
			str		= restoreShortcodes( nodeStr( sel ) );
			wpsh	= wp.shortcode.next( '{{module.slug_underscore}}', str );
			d		= wpsh.shortcode.attrs.named;
		}
		editor.windowManager.open({
			title: l10n.dialogTitle,
			body: [
// 				{
// 					type	: 'label',
// 					text	: 'some...'
// 				},
// 				{
// 					type		: 'textbox',
// 					name		: 'sources',
// 					multiline	: true,
// 					layout		: 'flow',
// 					minWidth	: 320,
// 					style		: 'min-height:3.9em;white-space: nowrap;',
// 					value		: d.sources.split(',').join('\n')
// 				},
// 				{
// 					type	: 'listbox',
// 					name	: 'period',
// 					value	: d.period,
// 					values : [
// 						{ text: 'some...', 		value: 'this-week' },
// 						{ text: 'some...', 		value: 'next-week' }
// 					]
// 				},
			],
			onsubmit: callback
		});
	}

	editor.addCommand( 'cmd_{{module.slug_underscore}}_shortcode', function() {
		openShortcodeDialog( function(e){
			var shortcode = '[{{module.slug_underscore}}]';
			editor.insertContent( shortcode );
		} );
	});

	editor.addButton('{{module.slug_underscore}}_shortcode', {
		icon: '{{module.slug_underscore}}-shortcode-icon',
		tooltip: l10n.insert,
		cmd : 'cmd_{{module.slug_underscore}}_shortcode',
		onPostRender: function() {
			var btn = this;
			editor.on( 'nodechange', function( event ) {
				var shortcode_around = false;
				btn.disabled( ! editor.selection.isCollapsed() && ! shortcode_around );
			});
		}
	});

	editor.on('BeforeSetcontent', function(event) {
		event.content = replaceShortcodes( event.content );
	});
	editor.on('GetContent', function(event) {
		event.content = restoreShortcodes( event.content );
	});

} );
