/**
 * Created by gahan on 28/3/16.
 */

var cinput = document.getElementById("cselect");
var cEditor = CodeMirror.fromTextArea(document.getElementById("ccode"), {
    lineNumbers: true,
    matchBrackets: true,
    mode: "text/x-csrc"
});

var cmac = CodeMirror.keyMap.default == CodeMirror.keyMap.macDefault;
CodeMirror.keyMap.default[(cmac ? "Cmd" : "Ctrl") + "-Space"] = "autocomplete";
function cselectTheme() {
    var ctheme = cinput.options[cinput.selectedIndex].textContent;
    cEditor.setOption("theme", ctheme);
    location.hash = "#" + ctheme;
}

var choice = (location.hash && location.hash.slice(1)) ||
    (document.location.search &&
    decodeURIComponent(document.location.search.slice(1)));
if (choice) {
    cinput.value = choice;
    cEditor.setOption("theme", choice);
}

CodeMirror.on(window, "hashchange", function () {
    var theme = location.hash.slice(1);
    if (theme) {
        cinput.value = theme;
        cselectTheme();
    }
});

$(document).ready(function () {
    var str =   "#include <stdio.h> \n" +
                "int main(void) { \n" +
                "   // your code goes here \n" +
                "   return 0; \n" +
                "}";
    cEditor.setValue(str)
});