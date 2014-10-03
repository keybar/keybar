var
	configuration = require('../configuration')
;

module.exports = function(grunt) {
	grunt.config('jscs', {
		all: [
			configuration.js.gruntfile,
			configuration.js.grunttasks,
			configuration.js.sources
		],
		options: {
			config: '.jscs.json'
		}
	});

	grunt.loadNpmTasks('grunt-jscs-checker');
};
