"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.useTypewriter = useTypewriter;
var react_1 = require("react");
function useTypewriter(text, options) {
    var _a = options || {}, _b = _a.delay, delay = _b === void 0 ? 30 : _b, onDone = _a.onDone;
    var onDoneRef = (0, react_1.useRef)(onDone); // <- עטיפה
    (0, react_1.useEffect)(function () {
        onDoneRef.current = onDone; // <- עדכון רפרנס אם היא משתנה
    }, [onDone]);
    var _c = (0, react_1.useState)(""), displayed = _c[0], setDisplayed = _c[1];
    (0, react_1.useEffect)(function () {
        setDisplayed(""); // אפס
        var i = 0;
        var interval = setInterval(function () {
            setDisplayed(function (prev) { return prev + text.charAt(i); });
            i++;
            if (i >= text.length) {
                clearInterval(interval);
                if (onDoneRef.current)
                    onDoneRef.current(); // <- שימוש ביציבה
            }
        }, delay);
        return function () { return clearInterval(interval); };
    }, [text, delay]); // <- onDone הוסר מהתלויות
    return displayed;
}
