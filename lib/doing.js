#!/usr/bin/env node
const colors = require('colors');
const { erase, cursor } = require('sisteransi');

/*

usage:

const doing = require('./doing.js')

const p = doing('Biginning to start to try to do something', 'Done!', 'Failed...');

do_something_promising()
    .then( p.ok )
    .catch( p.fail )

*/

var foo = () => {

}

const doing = ( msg, ok_msg = 'OK', fail_msg = 'ERROR' ) => {
    let rot_i = 0;
    let rot_to = null;

    const out = process.stdout;
    const rot = [ '   ', '.  ', '.. ', '...' ];
    const write_end = ( wmsg ) => {
        out.write( cursor.to( msg.length + 2 ) );
        out.write( wmsg + erase.lineEnd );
    }

    const write_done = ( wmsg ) => {
        clearTimeout( rot_to )
        write_end( wmsg )
        out.write( "\n" + cursor.show );
    }

    const ok = () => write_done( ok_msg.green );
    const fail = () => write_done( fail_msg.red );
    const say = msg => {
        rot_i = 0;
        clearTimeout( rot_to );
        write_end( msg );
    }
    const blink = () => {
        rot_i++;
        rot_i = rot_i % rot.length;
        write_end( rot[rot_i].yellow )
        rot_to = setTimeout( blink, 250 );
    };

    out.write( msg + '  ' + rot[rot_i] + cursor.hide );
    blink()

    return { ok, fail, say, blink }
}


const test = async () => {

    const p = doing('Beginning to start to try to do something', 'Done!', 'Failed...');

    let to, i = 0;
    ( function interv() {
        if ( i < 5 ) {
            p.say( Math.random().toString(10) )
            to = setTimeout( interv, 333 );
        } else {
            p.blink();
        }
        i++;
    })();

    const prom = () => new Promise( (resolve,reject) => {
        setTimeout(resolve,5000)
    });

    await prom()
        .then( () => {clearTimeout(to);p.ok();} )
        .catch( p.fail )
	console.log('back to console now...')
}
module.exports = { doing, test };
//test()
