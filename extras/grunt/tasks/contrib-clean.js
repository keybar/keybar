var
	configuration = require('../configuration')
;


module.exports = function(grunt) {

	grunt.config('clean', {
		options: {
			force: true /* delete files outside of current directory */
		},
		build: [
			configuration.js.buildDir + '**/*',
			'!' + configuration.js.buildDir + '*.js',
			configuration.js.buildDir + '_*.js'
		]
	});

	grunt.loadNpmTasks('grunt-contrib-clean');
};
