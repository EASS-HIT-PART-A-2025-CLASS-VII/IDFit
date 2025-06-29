import { useEffect, useState, useRef } from "react";

export interface UseTypewriterOptions {
  delay?: number;
  onDone?: () => void;
}

export function useTypewriter(text: string, options?: UseTypewriterOptions) {
  const { delay = 30, onDone } = options || {};
  const onDoneRef = useRef(onDone); // <- עטיפה

  useEffect(() => {
    onDoneRef.current = onDone; // <- עדכון רפרנס אם היא משתנה
  }, [onDone]);

  const [displayed, setDisplayed] = useState("");

  useEffect(() => {
    setDisplayed(""); // אפס
    let i = 0;

    const interval = setInterval(() => {
      setDisplayed((prev) => prev + text.charAt(i));
      i++;
      if (i >= text.length) {
        clearInterval(interval);
        if (onDoneRef.current) onDoneRef.current(); // <- שימוש ביציבה
      }
    }, delay);

    return () => clearInterval(interval);
  }, [text, delay]); // <- onDone הוסר מהתלויות

  return displayed;
}
