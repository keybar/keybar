var
	jsGruntfile = 'Gruntfile',
	jsGrunttasks = 'extras/grunt/**/*.js',
	jsSource = 'src/keybar/static/js/src/',
	jsSources = jsSource + '**/*.js',
	jsTemplates = 'src/keybar/static/js/src/**/*.html',
	jsBuild = 'src/keybar/static/js/build/',
	sassSources = 'src/config/static/scss/**/*.scss'
;

module.exports = {
	js: {
		gruntfile: jsGruntfile,
		grunttasks: jsGrunttasks,
		sourceDir: jsSource,
		sources: jsSources,
		buildDir: jsBuild,
		templates: jsTemplates,
	},

	sass: {
		sources: sassSources
	},
};
