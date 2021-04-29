import Chart from 'chart.js/auto'

const charts = []

const chartCanvases = [].slice.call(document.querySelectorAll('[data-chart'))
chartCanvases.forEach((el) => {
  const dataKey = el.getAttribute('data-data-key')

  const data = window.CHART_DATA[dataKey]
  charts.push(new Chart(el, data))
})
