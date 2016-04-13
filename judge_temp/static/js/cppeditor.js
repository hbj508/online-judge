/**
 * Created by gahan on 28/3/16.
 */
var cppinput = document.getElementById("cppselect");

var cppEditor = CodeMirror.fromTextArea(document.getElementById("cppcode"),
    {
        lineNumbers: true,
        matchBrackets: true,
        mode: "text/x-c++src"
    });

var cppmac = CodeMirror.keyMap.default == CodeMirror.keyMap.macDefault;
CodeMirror.keyMap.default[(cppmac ? "Cmd" : "Ctrl") + "-Space"] = "autocomplete";

function cppselectTheme() {
    var cpptheme = cppinput.options[cppinput.selectedIndex].textContent;
    cppEditor.setOption("theme", cpptheme);
    location.hash = "#" + cpptheme;
}

var choice = (location.hash && location.hash.slice(1)) ||
    (document.location.search &&
    decodeURIComponent(document.location.search.slice(1)));

if (choice) {
    cppinput.value = choice;
    cppEditor.setOption("theme", choice);
}

CodeMirror.on(window, "hashchange", function () {
    var theme = location.hash.slice(1);
    if (theme) {
        cinput.value = theme;
        cselectTheme();
    }
});

$(document).ready(function () {
    var str =   "#include <iostream> \n" +
                "using namespace std; \n" +
                "int main() { \n" +
                "   // your code goes here \n" +
                "   return 0; \n" +
                "}";
    cppEditor.setValue(str)
});