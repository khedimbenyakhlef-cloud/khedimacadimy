'use client'
import Link from 'next/link'
import { ArrowRight, BookOpen, MapPin, Users, Search, Star } from 'lucide-react'

const stats = [
  { label: 'Filières disponibles', value: '200+', icon: BookOpen },
  { label: 'Universités', value: '107', icon: MapPin },
  { label: 'Wilayas couvertes', value: '58', icon: MapPin },
  { label: 'Bacheliers aidés', value: '12k+', icon: Users },
]

const etapes = [
  { num: '01', titre: 'Entrez votre profil', desc: "Moyenne, série du bac et centres d'intérêt" },
  { num: '02', titre: 'Obtenez vos recommandations', desc: 'Notre algorithme analyse 200+ filières et 107 universités' },
  { num: '03', titre: 'Comparez et choisissez', desc: "Débouchés, taux d'emploi, témoignages d'étudiants" },
]

// SVG logo : toque de diplômé + étoile de réussite
function LogoSVG({ size = 64 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Toque de diplômé */}
      <polygon points="50,18 92,38 50,58 8,38" fill="#15803d" opacity="0.95"/>
      <rect x="66" y="38" width="4" height="22" rx="2" fill="#15803d"/>
      <circle cx="68" cy="62" r="5" fill="#f59e0b"/>
      {/* Corps de la toque */}
      <path d="M28 42 Q28 68 50 72 Q72 68 72 42" fill="#166534"/>
      {/* Étoile de réussite */}
      <polygon
        points="50,26 52.5,33.5 60,33.5 54,38.5 56.5,46 50,41 43.5,46 46,38.5 40,33.5 47.5,33.5"
        fill="#fbbf24"
        opacity="0.9"
      />
      {/* Ruban sous la toque */}
      <rect x="36" y="70" width="28" height="6" rx="3" fill="#15803d" opacity="0.7"/>
    </svg>
  )
}

export default function HomePage() {
  return (
    <div>
      {/* ── HERO ── */}
      <section className="bg-gradient-to-br from-green-700 to-green-900 text-white py-24 px-4">
        <div className="max-w-4xl mx-auto text-center">
          {/* Logo toque */}
          <div className="flex justify-center mb-5">
            <div className="bg-white/10 p-5 rounded-3xl shadow-lg">
              <LogoSVG size={72} />
            </div>
          </div>

          <h1 className="text-4xl md:text-5xl font-black mb-2 leading-tight tracking-tight">
            Orientation DZ
          </h1>
          <p className="text-green-200 text-sm mb-4 font-medium">
            Fondé par <span className="text-white font-bold">KHEDIM BENYAKHLEF dit Beny-Joe</span>
          </p>
          <p className="text-xl text-green-100 mb-10 max-w-2xl mx-auto">
            La plateforme d&apos;orientation universitaire pour les bacheliers algériens.
            Recommandations personnalisées selon ta moyenne, ta série et tes passions.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/orientation"
              className="bg-white text-green-800 font-bold px-8 py-3.5 rounded-xl hover:bg-green-50 transition flex items-center justify-center gap-2 shadow-md"
            >
              <Search size={20} />
              Commencer l&apos;orientation
            </Link>
            <Link
              href="/filieres"
              className="border border-white/40 text-white font-semibold px-8 py-3.5 rounded-xl hover:bg-white/10 transition flex items-center justify-center gap-2"
            >
              <BookOpen size={20} />
              Explorer les filières
            </Link>
          </div>
        </div>
      </section>

      {/* ── STATS ── */}
      <section className="bg-white border-b border-gray-100 py-10">
        <div className="max-w-5xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-6">
          {stats.map(({ label, value, icon: Icon }) => (
            <div key={label} className="text-center">
              <Icon size={24} className="text-green-600 mx-auto mb-2" />
              <div className="text-3xl font-black text-gray-900">{value}</div>
              <div className="text-sm text-gray-500 mt-1">{label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* ── COMMENT ÇA MARCHE ── */}
      <section className="py-20 px-4">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">Comment ça marche ?</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {etapes.map(({ num, titre, desc }) => (
              <div key={num} className="text-center">
                <div className="text-5xl font-black text-green-100 mb-4">{num}</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{titre}</h3>
                <p className="text-gray-500">{desc}</p>
              </div>
            ))}
          </div>
          <div className="text-center mt-12">
            <Link
              href="/orientation"
              className="inline-flex items-center gap-2 bg-green-700 text-white font-semibold px-8 py-3 rounded-xl hover:bg-green-800 transition"
            >
              Démarrer maintenant <ArrowRight size={18} />
            </Link>
          </div>
        </div>
      </section>

      {/* ── KINSTA BANNER ── */}
      <section className="max-w-5xl mx-auto px-4 mb-10">
        <a
          href="https://kinsta.com/?kaid=HUFPGOMPMRPI"
          target="_blank"
          rel="noopener noreferrer"
          className="flex flex-col sm:flex-row items-center justify-between gap-4 bg-gradient-to-r from-[#1a1a2e] to-[#16213e] text-white rounded-2xl p-6 hover:shadow-xl transition group"
        >
          <div className="flex items-center gap-4">
            {/* Kinsta logo SVG inline */}
            <div className="bg-white rounded-xl p-2.5 shrink-0">
              <svg width="36" height="36" viewBox="0 0 100 100" fill="none">
                <rect width="100" height="100" rx="16" fill="#1a1a2e"/>
                <path d="M20 20 L20 80 L38 80 L38 55 L62 80 L84 80 L56 48 L82 20 L60 20 L38 45 L38 20 Z" fill="#ffffff"/>
              </svg>
            </div>
            <div>
              <div className="text-xs text-gray-400 mb-0.5">Hébergez votre projet avec</div>
              <div className="text-xl font-black tracking-wide">Kinsta</div>
              <div className="text-sm text-gray-300 mt-0.5">
                Hébergement cloud ultra-rapide pour Next.js &amp; Python — recommandé par Beny-Joe
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2 bg-[#FF6B35] text-white font-bold px-5 py-2.5 rounded-xl group-hover:bg-orange-500 transition shrink-0">
            Découvrir Kinsta <ArrowRight size={16} />
          </div>
        </a>
      </section>

      {/* ── CTA AUTH ── */}
      <section className="bg-green-50 border border-green-100 mx-4 rounded-2xl py-14 px-6 mb-16 max-w-5xl md:mx-auto text-center">
        <div className="flex justify-center mb-4">
          <LogoSVG size={48} />
        </div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Sauvegarde ton profil et tes recommandations
        </h2>
        <p className="text-gray-500 mb-6">
          Crée un compte gratuit pour retrouver tes résultats, laisser un témoignage et suivre l&apos;actualité des inscriptions.
        </p>
        <Link
          href="/auth"
          className="inline-flex items-center gap-2 bg-green-700 text-white font-semibold px-6 py-3 rounded-xl hover:bg-green-800 transition"
        >
          Créer un compte gratuit <ArrowRight size={18} />
        </Link>
      </section>
    </div>
  )
}
