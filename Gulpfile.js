var gulp = require('gulp'),
	del = require('del'),
	plugins = require('gulp-load-plugins')(),
	livereload = require('gulp-livereload'),
	read = require('fs').readFileSync,
	base = 'src/keybar',
	src = {
		foundation: 'bower_components/foundation/scss',
		templates: base + '/templates',
		scss: base + '/static/scss',
		fonts: base + '/static/fonts',
		images: base + '/static/img',
		js: base + '/static/js',
		manageScript: 'manage.py',
		serverScript: base + '/server.py',
	},
	dest = {
		css: base + '/static/css',
		js: base + '/static/js/build'
	};

/**
 * Cleaning css directory
 */
gulp.task('clean:css', function (done) {
	del(dest.css, done);
});

/**
 * Cleaning js directory
 */
gulp.task('clean:js', function (done) {
	del(dest.js, done);
});

/**
 * Compiling sass/scss files to css
 */
gulp.task('scss', ['clean:css'], function () {
	return gulp.src(src.scss + '/*.scss')
		.pipe(plugins.plumber())
		.pipe(plugins.sourcemaps.init())
		.pipe(plugins.sass({
			includePaths: [src.foundation]
		}))
		.pipe(plugins.sourcemaps.write('./'))
		.pipe(gulp.dest(dest.css))
		.pipe(livereload());
});

/**
* Validating scss files
*/
gulp.task('validate:scss', function () {
	return gulp.src(src.scss + '/**/*.scss')
		.pipe(plugins.plumber())
		.pipe(plugins.lintspaces())
		.pipe(plugins.lintspaces.reporter());
});

/**
* Validating js files
*/
gulp.task('validate:js', function () {
	return gulp.src(src.js + '/*.js')
		.pipe(plugins.plumber())
		.pipe(plugins.jscs({
			preset: 'jquery'
		}))
		.pipe(plugins.jshint())
		.pipe(plugins.lintspaces())
		.pipe(plugins.lintspaces.reporter());
});

/**
* Validating files
*/
gulp.task('validate', ['validate:scss', 'validate:js']);

gulp.task('watch', function () {
	gulp.watch(src.js + '/src/*.js', ['validate:js']);
	gulp.watch(src.scss + '/**/*.scss', ['validate:scss', 'scss']);
	livereload.listen({
		host: 'keybar.local',
		port: 35729,
		key: read('src/keybar/tests/resources/certificates/KEYBAR-intermediate-SERVER.key').toString(),
		cert: read('src/keybar/tests/resources/certificates/KEYBAR-intermediate-SERVER.cert').toString()
	});
});

gulp.task('build', ['validate', 'scss']);

gulp.task('default', ['build']);

gulp.task('serve', ['default', 'watch'], plugins.shell.task([
		'env PYTHONUNBUFFERED=true python ' + src.serverScript,
		'env PYTHONUNBUFFERED=true celery worker -A keybar.tasks -l INFO -E',
]));
