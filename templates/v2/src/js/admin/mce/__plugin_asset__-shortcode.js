tinymce.PluginManager.add( '{{shortcode_slug}}' , function( editor ) {

	var placeholder_img			= tinymce.Env.transparentSrc,
		placeholder_img			= 'data:image/svg+xml;base64,' + window.btoa('<svg version="1.1" id="Ebene_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" width="500px" height="40px" viewBox="0 0 500 40"><text transform="matrix(1 0 0 1 12.5127 22.9082)" font-family="-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Oxygen-Sans,Ubuntu,Cantarell,\'Helvetica Neue\',sans-serif" font-size="12" style="fill: #FFFFFF;stroke:none;font-weight:bold;">'+mce_catcal.l10n.catcal+'</text></svg>'),
		/*
		the_shortcode			= /\[{{shortcode_slug}} ?(([^\]]+)\]/g, // matches shortcodes without content [shortcodes attr="1"]
		/*/
		the_shortcode			= /\[{{shortcode_slug}} ?([^\]]*)\](.*)\[\/{{shortcode_slug}}\]/g, // matches shortcodes with content [shortcodes attr="1"]
		//*/
		the_visible_shortcode	= '<img title="'+mce_catcal.l10n.catcal+'" data-attr="{attr}" data-wp-entity="cateringcalendar" src="'+placeholder_img+'" data-mce-resize="false" data-mce-placeholder="1" />',
		l10n					= {{shortcode_slug}}.l10n;

	function nodeStr( node ) {
		var txt, ax, $el = jQuery("<div />");
		$el.append( node.cloneNode(false) );
		return $el.html();
	}


	function replaceShortcodes( content ) {
		return content.replace( the_catcal, function( all, attr ) {
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
[{{shortcode_slug}} ' + attr + ']\
\
		';
			}
			return match;
		});
	}	
	function openLunchcalDialog( callback, values ) {
		var sel		= editor.selection.getNode(),
			$sel	= jQuery( sel ),
			d = {
				sources	: '',
				period	: 'this-week'
			},
			str, wpsh;

		if ( $sel.is('[data-wp-entity="{{shortcode_slug}}"]') ) {
			str		= restoreShortcodes( nodeStr( sel ) );
			wpsh	= wp.shortcode.next( '{{shortcode_slug}}', str );
			d		= wpsh.shortcode.attrs.named;
		}
		editor.windowManager.open({
			title: l10n.dialogTitle,
			body: [
// 				{
// 					type	: 'label', 
// 					text	: mce_catcal.l10n.url
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
// 						{ text: mce_catcal.l10n.this_week, 		value: 'this-week' },
// 						{ text: mce_catcal.l10n.next_week, 		value: 'next-week' }
// 					]
// 				},
			],
			onsubmit: callback
		});
	}

	editor.addCommand( 'cmd_{{shortcode_slug}}', function() {
		openLunchcalDialog( function(e){
			var shortcode = '[{{shortcode_slug}}]';
			editor.insertContent( shortcode );
		} );
	});

	editor.addButton('{{shortcode_slug}}', {
		icon: '{{shortcode_slug}}-icon',
		tooltip: mce_catcal.l10n.catcal,
		cmd : 'cmd_{{shortcode_slug}}',
// 		onPostRender: function() {
// 			var cateringcalendarBtn = this;
// 			editor.on( 'nodechange', function( event ) {
// 				var cateringcalendar_around = false;
// 				cateringcalendarBtn.disabled( ! editor.selection.isCollapsed() && ! cateringcalendar_around );
// 			});
// 		}
	});

	editor.on('BeforeSetcontent', function(event) {
		event.content = replaceShortcodes( event.content );
	});
	editor.on('GetContent', function(event) {
		event.content = restoreShortcodes( event.content );
	});

} );

