import React, { useState } from "react";
import { Home } from "lucide-react";
import { FaWhatsapp } from "react-icons/fa";
import { MdEmail } from "react-icons/md";
import toast from "react-hot-toast";

export default function Sidebar() {
    const [showModal, setShowModal] = useState(false);
    const [hoveredHome, setHoveredHome] = useState(false);
    const [hoveredWhatsapp, setHoveredWhatsapp] = useState(false);


    // שדות טופס
    const [name, setName] = useState("");
    const [age, setAge] = useState("");
    const [prefix, setPrefix] = useState("");
    const [phone, setPhone] = useState("");
    const [email, setEmail] = useState("");
    const [message, setMessage] = useState("");

    return (
        <>
            {/* סרגל צד */}
            <div className="fixed top-8 left-0 z-50 flex flex-col items-start space-y-2">
                {/* כפתור ראשי עם טקסט נפתח */}
                <div
                    className="relative flex items-center"
                    onMouseEnter={() => setHoveredHome(true)}
                    onMouseLeave={() => setHoveredHome(false)}
                >
                    <div className="w-12 h-12 rounded-full bg-white/20 backdrop-blur shadow-md flex items-center justify-center hover:bg-white/30 transition cursor-pointer z-10">
                        <Home className="w-6 h-6 text-gray-700" />
                    </div>

                    <div
                        className={`absolute right-[-360px] top-1/2 -translate-y-1/2 bg-white/90 rounded-2xl shadow-lg px-4 py-3 text-sm text-gray-800 leading-snug text-right transition-all duration-500 transform ${hoveredHome
                            ? "opacity-100 scale-100"
                            : "opacity-0 scale-95 pointer-events-none"
                            }`}
                        style={{ width: "330px" }}
                    >
                        שלום מלש"ב יקר, אנחנו צוות מאבחנים פסיכוטכניים בצה"ל וייעודנו
                        לעזור לך להבין מהם התפקידים שיתאימו לך לשירות משמעותי, מהנה,
                        שמתאים בדיוק לך!
                    </div>
                </div>

                {/* ווטסאפ עם טקסט צף */}
                <div
                    className="relative flex items-center"
                    onMouseEnter={() => setHoveredWhatsapp(true)}
                    onMouseLeave={() => setHoveredWhatsapp(false)}
                >
                    <div className="w-12 h-12 rounded-full bg-white/20 backdrop-blur shadow-md flex items-center justify-center hover:bg-white/30 transition cursor-pointer z-10">
                        <FaWhatsapp className="w-6 h-6 text-gray-700" />
                    </div>

                    <div
                        className={`absolute right-[-260px] top-1/2 -translate-y-1/2 bg-white/90 rounded-2xl shadow-lg px-4 py-3 text-sm text-gray-800 leading-snug text-right transition-all duration-500 transform ${hoveredWhatsapp
                            ? "opacity-100 scale-100"
                            : "opacity-0 scale-95 pointer-events-none"
                            }`}
                        style={{ width: "230px" }}
                    >
                        אפשר גם לפנות אלינו בוואטסאפ
                        <br />
                        <strong>050-2651948</strong>
                    </div>
                </div>


                {/* אימייל */}
                <button
                    onClick={() => setShowModal(true)}
                    className="w-12 h-12 flex items-center justify-center rounded-full bg-white/20 hover:bg-white/30 shadow-md backdrop-blur cursor-pointer"
                >
                    <MdEmail className="w-6 h-6 text-gray-700" />
                </button>
            </div>

            {/* מודאל */}
            {showModal && (
                <div className="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50">
                    <div className="bg-white p-6 rounded-xl shadow-lg w-full max-w-md space-y-4 relative text-right">
                        <button
                            onClick={() => setShowModal(false)}
                            className="absolute top-3 left-3 text-gray-500 hover:text-red-500 text-xl"
                        >
                            ×
                        </button>

                        <h2 className="text-lg font-semibold text-gray-800">
                            לקביעת פגישת ייעוץ טלפוני, השאר פרטים!
                        </h2>

                        <form
                            className="space-y-3"
                            onSubmit={async (e) => {
                                e.preventDefault();

                                if (!name || !age || !prefix || !phone || !email || !message) {
                                    toast.error("נא למלא את כל השדות");
                                    return;
                                }

                                try {
                                    const res = await fetch(`${import.meta.env.VITE_API_URL}/contact/`, {
                                        method: "POST",
                                        headers: {
                                            "Content-Type": "application/json",
                                        },
                                        body: JSON.stringify({
                                            name,
                                            age: Number(age),
                                            phone: `${prefix}${phone}`,
                                            email,
                                            message,
                                        }),
                                    });

                                    if (!res.ok) throw new Error("שליחה נכשלה");

                                    toast.success("הפנייה נשלחה בהצלחה!");
                                    setShowModal(false);

                                    // איפוס שדות
                                    setName("");
                                    setAge("");
                                    setPrefix("");
                                    setPhone("");
                                    setEmail("");
                                    setMessage("");
                                } catch (err) {
                                    console.error(err);
                                    toast.error("שגיאה בשליחה. נסה שוב.");
                                }
                            }}
                        >
                            <input
                                type="text"
                                placeholder="שם מלא"
                                required
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                className="w-full h-10 px-3 border rounded-md focus:outline-none focus:ring"
                            />

                            <input
                                type="number"
                                placeholder="גיל"
                                min={14}
                                max={19}
                                required
                                value={age}
                                onChange={(e) => setAge(e.target.value)}
                                className="w-full h-10 px-3 border rounded-md focus:outline-none focus:ring"
                            />

                            {/* טלפון */}
                            <div className="flex flex-row-reverse gap-2">
                                <select
                                    required
                                    value={prefix}
                                    onChange={(e) => setPrefix(e.target.value)}
                                    className="w-24 p-2 border rounded-md focus:outline-none focus:ring bg-white text-black text-right"
                                >
                                    <option value="" disabled hidden>
                                        קידומת
                                    </option>
                                    <option value="050">050</option>
                                    <option value="052">052</option>
                                    <option value="053">053</option>
                                    <option value="054">054</option>
                                    <option value="055">055</option>
                                    <option value="058">058</option>
                                </select>

                                <input
                                    type="tel"
                                    pattern="[0-9]{7}"
                                    maxLength={7}
                                    required
                                    value={phone}
                                    onChange={(e) => setPhone(e.target.value)}
                                    placeholder="מספר טלפון"
                                    className="flex-1 p-2 border rounded-md focus:outline-none focus:ring text-right"
                                />
                            </div>

                            <input
                                type="email"
                                required
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                placeholder="מייל"
                                pattern="^[^@\s]+@[^@\s]+\.[^@\s]+$"
                                className="w-full h-10 px-3 border rounded-md focus:outline-none focus:ring"
                            />

                            <textarea
                                rows={3}
                                required
                                value={message}
                                onChange={(e) => setMessage(e.target.value)}
                                placeholder="תוכן הפנייה"
                                className="w-full p-2 border rounded-md focus:outline-none focus:ring resize-none"
                            ></textarea>

                            <button
                                type="submit"
                                className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-md transition"
                            >
                                שלח פנייה
                            </button>
                        </form>
                    </div>
                </div>
            )}
        </>
    );
}
