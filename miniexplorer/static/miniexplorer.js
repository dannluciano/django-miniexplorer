/* eslint-env browser */
/* global django CodeMirror sqlFormatter */

django.jQuery(function () {
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
    editor.setSize('100%', '100%')

    const formatButton = document.createElement('button')
    formatButton.classList.add('button')
    formatButton.textContent = 'Format'
    formatButton.type = 'button'
    formatButton.addEventListener('click', function (event) {
      const rawSQL = editor.getValue()
      const formatedSQL = sqlFormatter.format(rawSQL)
      editor.setValue(formatedSQL)
    })
    const node = document.createElement('div')
    node.appendChild(formatButton)
    editor.addPanel(node, { position: 'top', stable: true })
  }
})
