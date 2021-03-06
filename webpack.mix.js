let mix = require('laravel-mix')

mix.setPublicPath('crowdeval/static')

mix.sass('assets/scss/app.scss', 'css')
  .js('assets/js/app.js', 'js')
  .copy('assets/img', 'crowdeval/static/img')
