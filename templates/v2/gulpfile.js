var gulp = require('gulp');
var concat = require('gulp-concat');  
var uglify = require('gulp-uglify');  
var sass = require('gulp-sass');
var sourcemaps = require('gulp-sourcemaps');
var rename = require('gulp-rename');


gulp.task('styles:dev', function() {
	// dev
{{#scss}}
    gulp.src('scss/{{.}}.scss')
		.pipe(sourcemaps.init())
        .pipe( sass( { outputStyle: 'expanded' } ).on('error', sass.logError) )
        .pipe( sourcemaps.write() )
		.pipe(rename('{{.}}.css'))
        .pipe( gulp.dest('./css/'));
{{/scss}}
});

gulp.task('styles:prod', function() {
	// dev
{{#scss}}
    gulp.src('scss/{{.}}.scss')
		.pipe( sass( { 
			outputStyle: 'compressed', omitSourceMapUrl: true 
		} ).on('error', sass.logError) )
		.pipe(rename('{{.}}.min.css'))
		.pipe( gulp.dest('./css/'));
{{/scss}}
});


gulp.task('default', function() {
	// place code for your default task here
	gulp.watch('scss/**/*.scss',['styles:prod']);
	gulp.watch('scss/**/*.scss',['styles:dev']);
//	gulp.watch('js/src/*.js',['scripts']);
});