/**
 * Created by gahan on 28/3/16.
 */
var input = document.getElementById("select");

var Editor = CodeMirror.fromTextArea(document.getElementById("code"),
    {
        lineNumbers: true,
        matchBrackets: true,
        mode: "text/x-java"
    });

var mac = CodeMirror.keyMap.default == CodeMirror.keyMap.macDefault;
CodeMirror.keyMap.default[(mac ? "Cmd" : "Ctrl") + "-Space"] = "autocomplete";
function selectTheme() {
    var theme = input.options[input.selectedIndex].textContent;
    Editor.setOption("theme", theme);
    location.hash = "#" + theme;
}

var choice = (location.hash && location.hash.slice(1)) ||
    (document.location.search &&
    decodeURIComponent(document.location.search.slice(1)));
if (choice) {
    input.value = choice;
    Editor.setOption("theme", choice);
}

CodeMirror.on(window, "hashchange", function () {
    var theme = location.hash.slice(1);
    if (theme) {
        input.value = theme;
        selectTheme();
    }
});

$(document).ready(function () {
    var str = "/*package codepro; // don't place package name! */ \n" +
                "import java.util.*; \n" +
                "import java.lang.*; \n" +
                "import java.io.*; \n" +
                "/* Name of the class has to be \"Solution\" only if the class is public. */ \n"  +
                "public class Solution \n" +
                "{ \n" +
                "   public static void main (String[] args) throws java.lang.Exception \n" +
                "   { \n" +
                "       // your code goes here \n" +
                "   } \n" +
                "}";
    Editor.setValue(str)
});