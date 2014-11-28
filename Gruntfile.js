module.exports = function(grunt) {
	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		sass: {
			options: {
				includePaths: ['bower_components/foundation/scss'],
			},
			dist: {
				options: {
					outputStyle: 'expanded'
				},
				files: {
					'src/keybar/static/css/app.css': 'src/keybar/static/scss/app.scss'
				},
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
