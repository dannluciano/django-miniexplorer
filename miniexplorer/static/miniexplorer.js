/* eslint-env browser */
/* global django CodeMirror sqlFormatter */

const LANGUAGE_DICT = {
	en: {
		Run: "Run",
		" in ": " in ",
		Format: "Format",
		"Return ": "Return ",
		" rows, ": " rows, ",
		"Last execution has ": "Last execution has ",
		" seconds": " seconds",
	},
	"pt-br": {
		Run: "Executar",
		" in ": " em ",
		Format: "Formatar",
		"Return ": "Retornou ",
		" rows, ": " linhas, ",
		"Last execution has ": "Última execução em ",
		" seconds": " segundos",
	},
};

function Translator(lang) {
	return function translate(key) {
		return LANGUAGE_DICT[lang][key] || "Not Defined";
	};
}

django.jQuery(() => {
	let gEditor = null;
	fetch("/admin/miniexplorer/query/database_schema/", {
		method: "GET",
		headers: {
			"Content-Type": "application/json",
		},
		credentials: "same-origin",
	})
		.then((response) => response.json())
		.then((data) => {
			const collapserLink = document.getElementById("fieldsetcollapser1");

			collapserLink.addEventListener("click", (event) => {
				if (!gEditor) {
					setTimeout(() => {
						const textarea = document.getElementById("id_sql");
						textarea.autocorrect = "off";
						textarea.spellcheck = false;
						if (textarea) {
							const editor = CodeMirror.fromTextArea(textarea, {
								lineNumbers: true,
								autofocus: true,
								mode: "text/x-sql",
								hint: CodeMirror.hint.sql,
								extraKeys: { "Ctrl-Space": "autocomplete" },
								hintOptions: {
									tables: data,
								},
								viewportMargin: 20,
							});
							editor.setSize("100%", "50vh");
							gEditor = editor;
						}
					}, 100);
				}
			});
		})
		.catch((error) => {
			console.error(error);
		});

	setTimeout(() => {
		const textarea = document.getElementById("id_sql");
		if (textarea.value.length > 0) {
			const executeButton = document.getElementById("execute_button");
			executeButton.click();
		}
	}, 1000);

	const currentLanguage =
		document.querySelector("html").lang.toLowerCase() || "en";
	const translate = Translator(currentLanguage);

	const formatButton = document.createElement("input");
	formatButton.type = "submit";
	formatButton.value = translate("Format");
	formatButton.addEventListener("click", (event) => {
		event.preventDefault();
		console.info("Formatting SQL...");
		const rawSQL = gEditor.getValue();
		const formatedSQL = sqlFormatter.format(rawSQL);
		gEditor.setValue(formatedSQL);
	});

	const executeButton = document.createElement("input");
	executeButton.id = "execute_button";
	executeButton.type = "submit";
	executeButton.value = translate("Run");
	executeButton.addEventListener("click", (event) => {
		event.preventDefault();
		const textarea = document.getElementById("id_sql");
		const rawSQL = gEditor ? gEditor.getValue() : textarea.value;
		console.info("Executing SQL...\n", rawSQL);
		const csrftoken = document.querySelector(
			"[name=csrfmiddlewaretoken]",
		).value;

		fetch("/admin/miniexplorer/query/execute/", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": csrftoken,
			},
			credentials: "same-origin",
			body: JSON.stringify({
				sql: rawSQL,
			}),
		})
			.then((response) => response.json())
			.then((data) => {
				console.info(data);

				if ("error" in data) {
					alert(data.msg);
					return;
				}

				const table = document.getElementById("result_list");
				const oldThead = table.querySelector("thead");
				const oldTbody = table.querySelector("tbody");

				if (!oldThead || !oldTbody) {
					return;
				}

				table.removeChild(oldThead);
				table.removeChild(oldTbody);

				const thead = document.createElement("thead");
				const tbody = document.createElement("tbody");
				const tr = document.createElement("tr");

				if (!data.fields) {
					return;
				}
				data.fields.forEach((field) => {
					const th = document.createElement("th");
					th.textContent = field;
					tr.appendChild(th);
				});
				thead.appendChild(tr);

				data.results.forEach((row) => {
					const tr = document.createElement("tr");
					row.forEach((col) => {
						const td = document.createElement("td");
						td.textContent = col;
						tr.appendChild(td);
					});
					tbody.appendChild(tr);
				});

				table.appendChild(thead);
				table.appendChild(tbody);

				const lastTime = new Date(data.last_time);
				const datetimeFormatter = new Intl.DateTimeFormat(currentLanguage, {
					dateStyle: "short",
					timeStyle: "short",
				});

				const paginator = document.querySelector(".paginator");
				paginator.textContent = translate("Return ");
				paginator.textContent += data.results.length + translate(" rows, ");
				paginator.textContent +=
					translate("Last execution has ") + datetimeFormatter.format(lastTime);
				paginator.textContent +=
					translate(" in ") + data.delta_time + translate(" seconds");
			})
			.catch((error) => {
				console.error(error);
			});
	});

	const submitRow = document.querySelector(".submit-row");
	submitRow.insertBefore(formatButton, submitRow.firstChild);
	submitRow.insertBefore(executeButton, formatButton);
});
