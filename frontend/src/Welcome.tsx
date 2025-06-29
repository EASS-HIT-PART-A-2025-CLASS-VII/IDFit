import { useNavigate } from "react-router-dom";
import SidebarIcons from "./SidebarIcons"; // ודא שהנתיב נכון

export default function Welcome() {
  const navigate = useNavigate();

  return (
    <div className="relative flex flex-col items-center justify-center h-screen bg-[#e7edf6] overflow-hidden">
      {/* 🎥 דגל מתנופף */}
      <video
        src="/Sol_Flag.mov"
        autoPlay
        loop
        muted
        playsInline
        className="fixed top-0 left-0 w-full h-full object-cover z-0 opacity-80 pointer-events-none"
      />

      {/* כפתורי הצד */}
      <SidebarIcons />

      {/* לוגו לחיץ */}
      <img
        src="/logoGlow.png"
        alt="IDFit Logo"
        className="w-100 h-100 z-10 cursor-pointer transition-transform hover:scale-110"
        onClick={() => navigate("/app")}
      />

      {/* כפתור התחלה */}
      <button
        onClick={() => navigate("/app")}
        className="mt-6 font-gveret z-10 group relative inline-flex items-center justify-center px-8 py-3 overflow-hidden font-bold text-white transition-all duration-300 bg-gradient-to-r from-purple-600 to-blue-600 rounded-xl shadow-lg hover:from-purple-700 hover:to-blue-700 hover:scale-105"
      >
        <span className="absolute inset-0 w-full h-full bg-white opacity-10 blur-sm"></span>
        <span className="relative z-10 flex items-center gap-2">
          התחל עכשיו
        </span>
      </button>
    </div>
  );
}
