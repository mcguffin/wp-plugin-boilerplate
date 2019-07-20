const ParentComponent = require('./parent-component.js');
const ChildComponent = require('./child-component.js');
//const AdminPageChildComponent = require('./admin-page-child-component.js');
const promts = require('prompts');


class AdminPageChildComponent extends ChildComponent {

	// getter seems to be required...
	get slug() {
		return super.slug
	}
	set slug( s ) {
		if ( -1 === ['comments','dashboard','links','management','media','pages','plugins','posts','theme','tools','users'].indexOf(s) ) {
			throw( `${s} is not a vald admin page slug` )
		}
		super.slug = s;
	}


	// comments|dashboard|links|management|media|pages|plugins|posts|theme|tools|users
	get prefix() {
		let p = super.prefix;
		if ( p === 'tools' ) {
			return 'management';
		}
		return p;
	}


}

class AdminPageComponent extends ParentComponent {

	componentClass = AdminPageChildComponent

	namespace = 'Admin/Page';

}

module.exports = AdminPageComponent;
