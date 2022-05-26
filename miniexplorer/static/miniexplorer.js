/* eslint-env browser */
/* global django CodeMirror sqlFormatter */

django.jQuery(
  function () {
    const textarea = document.getElementById('id_sql')
    if (textarea) {
      const editor = CodeMirror.fromTextArea(
        textarea, {
          lineNumbers: true,
          autofocus: true,
          mode: 'sql',
          viewportMargin: 20
        }
      )
      editor.setSize('100%', '50vh')

      const formatButton = document.createElement('input')
      formatButton.type = 'submit'
      formatButton.value = 'Format'
      formatButton.addEventListener('click', function (event) {
        event.preventDefault()
        console.info('Formatting SQL...')
        const rawSQL = editor.getValue()
        const formatedSQL = sqlFormatter.format(rawSQL)
        editor.setValue(formatedSQL)
      })

      const executeButton = document.createElement('input')
      executeButton.type = 'submit'
      executeButton.value = 'Run'
      executeButton.addEventListener(
        'click',
        function (event) {
          event.preventDefault()
          const rawSQL = editor.getValue()
          console.info('Executing SQL...\n', rawSQL)
          const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

          fetch(
            '/admin/miniexplorer/query/execute/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
              },
              credentials: 'same-origin',
              body: JSON.stringify({
                sql: rawSQL
              })
            }
          ).then(function (response) {
            return response.json()
          }).then(function (data) {
            console.info(data)
            const table = document.getElementById('result_list')
            const oldThead = table.querySelector('thead')
            const oldTbody = table.querySelector('tbody')

            table.removeChild(oldThead)
            table.removeChild(oldTbody)

            const thead = document.createElement('thead')
            const tbody = document.createElement('tbody')
            const tr = document.createElement('tr')

            if (!data.fields) { return }
            data.fields.forEach(
              function (field) {
                const th = document.createElement('th')
                th.textContent = field
                tr.appendChild(th)
              })
            thead.appendChild(tr)

            data.results.forEach(function (row) {
              const tr = document.createElement('tr')
              row.forEach(function (col) {
                const td = document.createElement('td')
                td.textContent = col
                tr.appendChild(td)
              })
              tbody.appendChild(tr)
            })

            table.appendChild(thead)
            table.appendChild(tbody)

            const lastTime = new Date(data.last_time)
            const deltaTime = data.delta_time

            const datetimeFormatter = new Intl.DateTimeFormat('en-US', { dateStyle: 'short', timeStyle: 'short' })

            const paginator = document.querySelector('.paginator')
            paginator.textContent = data.results.length + ' rows, '
            paginator.textContent += 'Last Execution ' + datetimeFormatter.format(lastTime)
            paginator.textContent += ' in ' + deltaTime + ' seconds'
          }).catch(function (error) {
            console.error(error)
          })
        })

      const submitRow = document.querySelector('.submit-row')
      submitRow.insertBefore(formatButton, submitRow.firstChild)
      submitRow.insertBefore(executeButton, formatButton)
    }
  })
