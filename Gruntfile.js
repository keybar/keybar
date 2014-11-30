module.exports = function(grunt) {
	var appConfig = grunt.file.readJSON('package.json');

	// Load grunt tasks automatically
	// see: https://github.com/sindresorhus/load-grunt-tasks
	require('load-grunt-tasks')(grunt);

	// Time how long tasks take. Can help when optimizing build times
	// see: https://npmjs.org/package/time-grunt
	require('time-grunt')(grunt);

	var pathsConfig = function (appName) {
		this.app = appName || appConfig.name;

		paths = {
			app: this.app,
			foundation: this.app + '/../../bower_components/foundation/scss',
			templates: this.app + '/templates',
			css: this.app + '/static/css',
			sass: this.app + '/static/scss',
			fonts: this.app + '/static/fonts',
			images: this.app + '/static/images',
			js: this.app + '/static/js',
			manageScript: this.app + '/manage.py',
			serverScript: this.app + '/server.py'
		}

		return paths
	};

	grunt.initConfig({
		pkg: appConfig,
		paths: pathsConfig('src/keybar'),

		sass: {
			options: {
				includePaths: ['<%= paths.foundation %>'],
			},
			dist: {
				options: {
					outputStyle: 'expanded'
				},

				files: [{
					expand: true,
					cwd: '<%= paths.sass %>',
					src: ['app.scss'],
					dest: '<%= paths.css %>',
					ext: '.css'
				}]
			}
		},
		watch: {
			options: {
				livereload: {
					key: grunt.file.read('extras/certificates/server.key'),
					cert: grunt.file.read('extras/certificates/server.crt')
				},
			},
			sass: {
				files: [
					'src/keybar/static/scss/app.scss',
					'src/keybar/static/scss/_settings.scss'
				],
				tasks: ['sass'],
			},
			html: {
				files: ['src/keybar/templates/keybar/web/*.html']
			}
		}
	});

	grunt.loadTasks('extras/grunt/tasks');

	grunt.loadNpmTasks('grunt-sass');
	grunt.loadNpmTasks('grunt-contrib-watch');

	grunt.registerTask(
		'default',
		'Run all tasks in a row.',
		['build']
	);

	grunt.registerTask(
		'validate',
		'Validate all files.',
		['jshint', 'jscs', 'lintspaces']
	);

	grunt.registerTask(
		'test',
		'Run JS tests.',
		[]
	);

	grunt.registerTask(
		'build',
		'Build all JS files for a deploy.',
		['validate', 'clean', 'sass']
	);
};
