import { Tooltip } from 'bootstrap'

const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new Tooltip(tooltipTriggerEl, {
    animation: false // temp turn off animation due to twbs/bootstrap#32372
  })
})
