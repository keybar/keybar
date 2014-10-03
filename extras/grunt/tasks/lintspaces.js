var
	configuration = require('../configuration')
;

module.exports = function(grunt) {
	grunt.config('lintspaces', {
		all: {
			src: [
				configuration.js.gruntfile,
				configuration.js.grunttasks,
				configuration.js.sources,
				configuration.js.templates,
				configuration.sass.sources,
			],
			options: {
				editorconfig: '.editorconfig',
				ignores: ['js-comments']
			}
		}
	});

	grunt.loadNpmTasks('grunt-lintspaces');
};
