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

		if ( ! this.user ) {
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


			this.plugin.mergeRootPackage( {
				repository: {
					type: "git",
					url: `git+${this.repo_uri}.git`
			    },
				bugs: {
			    	url: `${this.repo_uri}/issues`
			    },
				homepage: repo_uri
			});
		}
		this.plugin.mergeRootPackage( {
			scripts: {
				rollback: "git reset --hard HEAD~ && git push origin +master"
			},
		});
	}
	generate() {
		super.generate()
		// npm run dashicons
	}

	get repo() {
		return this.remote.replace( /^git@(.*):(.*)(\.git?)$/, '$2' )
	}

	get repo_uri() {
		return this.remote.replace( /^git@(.*):(.*)(\.git?)$/, 'https://$1/$2')
	}

	get package() {
		return { user: this.user, remote: this.remote }
	}
	set package( p ) {
		if (!!p.user && !!p.remote) {
			super.package = p
		}
	}

	async finish() {
		// git init, set remote, add, commit
		let r;
		try {
			// repo exists ... stop here
			r = exec.execSync( 'git status', { encoding: 'utf8' } );
			return;
		} catch ( e ) {
			// init repo
			exec.execSync( 'git init', { encoding: 'utf8' } );
			exec.execSync( `git add .`, { encoding: 'utf8' } );
			exec.execSync( `git commit -m "create with mcguffin/wp-plugin-boilerplate"`, { encoding: 'utf8' } );
			exec.execSync( `git remote add origin ${this.remote}`, { encoding: 'utf8' } );
		}

	}

}
module.exports =  GitComponent;
