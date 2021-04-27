const disableOnSubmitList = [].slice.call(document.querySelectorAll('.behaviour--disable-on-submit'))
disableOnSubmitList.forEach(function (el) {
  el.addEventListener('submit', (event) => {
    // Disable submit button
    const button = event.target.querySelector('button[type="submit"]')
    button.disabled = true
    button.innerHTML = 'Submitting...'

    // Disable inputs
    const fields = [...event.target.querySelectorAll('input'), ...event.target.querySelectorAll('textarea')]
    console.log(event.target)
    console.log(fields)

    fields.forEach((field) => {
      field.readOnly = true
    })
  })
})
