var
	configuration = require('../configuration')
;

module.exports = function(grunt) {
	grunt.config('jshint', {
		all: [
			configuration.js.gruntfile,
			configuration.js.grunttasks,
			configuration.js.sources
		],
		options: {
			jshintrc: '.jshintrc'
		}
	});

	grunt.loadNpmTasks('grunt-contrib-jshint');
};
