require "compass-selector-warn"
require "rgbapng"

selector_warn_max     = 2000

# Require any additional compass plugins here.
add_import_path "bower_components/foundation/scss"

# Set this to the root of your project when deployed:
http_path = "/"
css_dir = "src/keybar/static/css"
sass_dir = "src/keybar/static/scss"
images_dir = "src/keybar/static/img"
javascripts_dir = "src/keybar/static/js"

# You can select your preferred output style here (can be overridden via the command line):
# or :nested or :compact or :compressed
output_style = :expanded

line_comments = true

relative_assets = true
