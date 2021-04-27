import { Tooltip, Popover } from 'bootstrap'

const archiveInfoTriggerList = [].slice.call(document.querySelectorAll('[data-ce-archive-info]'))
archiveInfoTriggerList.map(function (el) {
  console.log(el.dataset)
  return new Popover(el, {
    animation: false,
    html: true,
    sanitize: false,
    content: `
    <div><strong>Archived by CrowdEval on ${el.dataset.ceArchiveDate}.</strong></div>
    <div>The original post may no longer exist</div>
    <div class="btn-icon-left">
      <a href="${el.dataset.ceOriginalUrl}" target="_blank" rel="nofollow noopener">
        <i class="fas fa-external-link-alt fa-fw"></i>Open original post
      </a>
    </div>
    <div class="btn-icon-left">
      <a href="https://web.archive.org/web/*/${el.dataset.ceOriginalUrl}" target="_blank" rel="nofollow noopener">
        <i class="fas fa-landmark fa-fw"></i>View in Wayback Machine
      </a>
    </div>
    `
  })
})

const externalLinkDisclaimerList = [].slice.call(document.querySelectorAll('.behaviour--add-disclaimer-to-links a'))
externalLinkDisclaimerList.map(function (el) {
  return new Tooltip(el, {
    animation: false,
    title: 'External links are not archived or monitored'
  })
})
