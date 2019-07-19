const BaseComponent = require('./base-component.js');
const promts = require('prompts');
const exec = require('child_process');

class GitComponent extends BaseComponent {
	async setup() {
		let data, repo_uri;

		[
			'.gitattributes',
			'.gitignore',
		].forEach( t => this.addTemplate( t ) );

		console.log(this.user);
		this.user = exec.execSync( 'git config user.name', { encoding: 'utf8' } ).trim();
		data = await promts([
			{
				type: 'text',
				name: 'user',
				message: 'git user:',
				initial: this.user
			},
		], { onCancel: process.exit });
		this.user = data.user;

		this.remote = `git@github.com:${this.user}/${this.plugin.slug}.git`;
		data = await promts([
			{
				type: 'text',
				name: 'remote',
				message: 'Git remote URL:',
				initial: this.remote
			},
		], { onCancel: process.exit });
		this.remote = data.remote;

		// make https-URL
		repo_uri = this.remote.replace( /^git@(.*):(.*)(\.git?)$/, 'https://$1/$2')

		this.plugin.mergeRootPackage( {
			repository: {
				type: "git",
				url: `git+${repo_uri}.git`
		    },
			bugs: {
		    	url: `${repo_uri}/issues`
		    },
			homepage: repo_uri
		});

	}

	get package() {
		return { user: this.user, remote: this.remote }
	}
	set package( p ) {
		super.package = p
	}
	finish() {
		// git init, set remote, add, commit
		console.log('git init')
	}

}
module.exports =  GitComponent;
