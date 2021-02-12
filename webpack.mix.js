let mix = require('laravel-mix')

mix.setPublicPath('crowdeval/static')

mix.sass('assets/scss/app.scss', 'css')