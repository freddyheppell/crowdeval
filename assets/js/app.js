import * as bootstrap from 'bootstrap'

window.Popper = require('@popperjs/core').default
require('@fortawesome/fontawesome-free/js/all.min.js')

const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl, {
    animation: false // temp turn off animation due to twbs/bootstrap#32372
  })
})
