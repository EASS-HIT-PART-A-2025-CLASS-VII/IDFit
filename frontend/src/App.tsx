import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import SidebarIcons from "./SidebarIcons";
import { Toaster } from 'react-hot-toast';
import toast from 'react-hot-toast';


const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export default function App() {
  const [name, setName] = useState("");
  const [age, setAge] = useState(14);
  const [gender, setGender] = useState("זכר");
  const [fitness, setFitness] = useState(3);
  const [technicalSkills, setTechnicalSkills] = useState("");
  const [languages, setLanguages] = useState("");
  const [description, setDescription] = useState("");
  const [result, setResult] = useState<any[]>([]);
  const [summary, setSummary] = useState<string | null>(null);
  const [typedSummary, setTypedSummary] = useState("");
  const [isTypingDone, setIsTypingDone] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [contactName, setContactName] = useState("");
  const [contactEmail, setContactEmail] = useState("");
  const [contactPhone, setContactPhone] = useState("");
  const [contactMessage, setContactMessage] = useState("");


  useEffect(() => {
    if (summary) {
      let index = 0;
      setTypedSummary("");
      setIsTypingDone(false);

      const interval = setInterval(() => {
        setTypedSummary((prev) => prev + summary[index]);
        index++;

        if (index >= summary.length) {
          clearInterval(interval);
          setIsTypingDone(true);
        }
      }, 20);

      return () => clearInterval(interval);
    }
  }, [summary]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!name || age <= 0 || !description.trim()) {
      setError("יש למלא לפחות את השם, גיל, ותיאור חופשי.");
      setLoading(false);
      return;
    }
    setLoading(true);
    setError(null);
    setResult([]);
    setSummary(null);
    setTypedSummary("");
    setIsTypingDone(false);

    const profileData = {
      name,
      age,
      gender,
      physical_fitness: fitness,
      technical_skills: technicalSkills.split(",").map((s) => s.trim()),
      personality_traits: [],
      languages: languages.split(",").map((s) => s.trim()),
      description,
    };

    try {
      const res = await fetch(`${API_BASE}/profiles/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(profileData),
      });

      if (!res.ok) throw new Error("שגיאה ביצירת פרופיל");

      const data = await res.json();
      const pid = data.id;

      const recRes = await fetch(`${API_BASE}/profiles/${pid}/recommendations/`);
      const recData = await recRes.json();

      console.log("🎯 recData:", recData);

      if (!recData || !recData.recommendations) {
        throw new Error(recData?.detail || "שגיאה בקבלת המלצות");
      }

      setSummary(recData.summary || null);
      setResult(recData.recommendations);
    } catch (err: any) {
      console.error("❌ Error:", err);
      setError(err.message || "שגיאה בלתי צפויה");
    } finally {
      setLoading(false);
    }
  };

  const handleContactSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);

    const name = formData.get("name") as string;
    const email = formData.get("email") as string;
    const phone = formData.get("phone") as string;
    const message = formData.get("message") as string;

    try {
      const res = await fetch(`${API_BASE}/contact/`, {
        method: "POST",
        body: new URLSearchParams({ name, email, phone, message }), // כמו FormData אך URL-encoded
      });

      if (!res.ok) {
        const error = await res.json();
        throw new Error(error.detail || "שליחה נכשלה");
      }

      toast.success("הפנייה נשלחה בהצלחה!");
    } catch (err: any) {
      toast.error(err.message || "שגיאה בשליחת הפנייה");
    }
  };


  return (
    <>
      <Toaster position="top-center" />
      <SidebarIcons />

      {/* ✅ וידאו רקע קבוע למסך כולו */}
      <div className="fixed top-0 left-0 w-full h-full -z-10">
        <video
          src="/Sol_Flag.mov"
          autoPlay
          loop
          muted
          playsInline
          className="w-full h-full object-cover opacity-60"
        />
        {/* שכבת הצללה עדינה מעל הווידאו */}
        <div className="absolute inset-0 bg-white/20" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.6 }}
        className="w-full max-w-5xl bg-white/80 backdrop-blur-md rounded-xl shadow-xl p-6 space-y-6"
      >
        <div className="w-full bg-transparent py-2 mb-1 shadow-sm">
          <div className="container mx-auto flex flex-col md:flex-row items-center justify-center gap-4 relative">
            <img
              src="/logoWeb3.png"
              alt="IDFit Logo"
              className="w-full max-w-4xl h-auto"
            />
          </div>
        </div>

        <form onSubmit={handleSubmit} className="bg-white shadow-md rounded-lg p-6 space-y-4 mb-8">
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="font-semibold">שם:</label>
              <input value={name} onChange={(e) => setName(e.target.value)} className="input" />
            </div>
            <div>
              <label className="font-semibold">גיל:</label>
              <input type="number" min={14} max={19} value={age} onChange={(e) => setAge(Number(e.target.value))} className="input" />
            </div>
            <div>
              <label className="font-semibold">מין:</label>
              <select value={gender} onChange={(e) => setGender(e.target.value)} className="input">
                <option value="זכר">זכר</option>
                <option value="נקבה">נקבה</option>
              </select>
            </div>
            <div>
              <label className="font-semibold">רמת כושר גופני (כאשר 1 הינו הרמה הנמוכה ביותר):</label>
              <input
                type="number" min={1} max={5}
                value={fitness}
                onChange={(e) => setFitness(Number(e.target.value))}
                className="input"
              />
            </div>
          </div>

          <div>
            <label className="font-semibold">כישורים טכניים (הפרד באמצעות פסיקים):</label>
            <input value={technicalSkills} onChange={(e) => setTechnicalSkills(e.target.value)} className="input" />
          </div>

          <div>
            <label className="font-semibold">דובר שפות (הפרד באמצעות פסיקים):</label>
            <input value={languages} onChange={(e) => setLanguages(e.target.value)} className="input" />
          </div>

          <div>
            <label className="font-semibold">תיאור חופשי:</label>
            <input
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="input"
              placeholder="תאר את עצמך במשפט או שניים"
            />
            <small className="text-sm text-gray-500 block mt-1">
              כתוב מי אתה – נזהה עבורך תכונות אישיות
            </small>
          </div>

          <div className="text-center">
            <button
              type="submit"
              disabled={loading}
              className="bg-blue-600 hover:bg-blue-700 text-white py-2 px-6 rounded transition"
            >
              {loading ? "🔄 מחשבים המלצות..." : "שלח"}
            </button>
          </div>
        </form>

        {error && (
          <div className="bg-red-100 text-red-700 p-4 rounded mb-6 border border-red-300">
            ❗ {error}
          </div>
        )}

        {typedSummary && typeof typedSummary === "string" && typedSummary.trim() !== "" && (
          <div
            key={typedSummary}
            className="bg-blue-50 border border-blue-300 text-blue-800 p-4 rounded mb-6 whitespace-pre-wrap"
          >
             {typedSummary.replace("undefined", "")}
          </div>
        )}

        {!loading && !error && result.length === 0 && (
          <p className="text-gray-500 text-center">טרם התקבלו המלצות</p>
        )}

        {isTypingDone && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 justify-center">
            {result.map((r, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="bg-white shadow rounded-lg p-6 border border-gray-200"
              >
                <h3 className="text-xl font-semibold mb-2 text-blue-700">{r.role.name}</h3>
                <p className="text-gray-700 mb-3">{r.role.description}</p>
                <ul className="text-sm text-gray-600 space-y-1">
                  <li>📋 פרופיל רפואי: {r.role.requirements?.profile ?? "לא נדרש"}</li>
                  <li>🧠 דפ"ר: {r.role.requirements?.dapar ?? "לא נדרש"}</li>
                  <li>📈 קב"א: {r.role.requirements?.kaba ?? "לא נדרש"}</li>
                  <li>🎯 תכונות: {r.role.requirements?.traits?.join(", ") ?? "לא צוין"}</li>
                  <li>🛠 כישורים טכניים: {r.role.requirements?.tech?.join(", ") ?? "לא צוין"}</li>
                </ul>
              </motion.div>
            ))}
          </div>
        )}
      </motion.div>
    </>
  );
}
