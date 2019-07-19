const BaseComponent = require('./base-component.js');

class ChildComponent extends BaseComponent {


	get slug() {
		return this._slug;
	}
	set slug( s ) {
		this._slug = s;
	}
	toString() {
		return `<ChildComponent ${this.slug}>`
	}
}
module.exports = ChildComponent;
