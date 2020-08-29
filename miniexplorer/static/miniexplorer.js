/* eslint-env browser */
/* global django CodeMirror */

django.jQuery(function () {
  CodeMirror.fromTextArea(
    document.getElementById('id_sql'), {
      lineNumbers: true,
      autofocus: true
    }
  )
})
