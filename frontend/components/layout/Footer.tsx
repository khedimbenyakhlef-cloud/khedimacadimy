import Link from 'next/link'

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300 py-12 mt-16">
      <div className="max-w-6xl mx-auto px-4">
        <div className="grid md:grid-cols-3 gap-8 mb-8">

          {/* Colonne 1 - Brand */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <svg width="28" height="28" viewBox="0 0 100 100" fill="none">
                <polygon points="50,18 92,38 50,58 8,38" fill="#22c55e"/>
                <path d="M28 42 Q28 68 50 72 Q72 68 72 42" fill="#16a34a"/>
                <polygon points="50,26 52.5,33.5 60,33.5 54,38.5 56.5,46 50,41 43.5,46 46,38.5 40,33.5 47.5,33.5" fill="#fbbf24"/>
              </svg>
              <span className="text-white font-black text-lg">Orientation DZ</span>
            </div>
            <p className="text-sm text-gray-400 leading-relaxed">
              Plateforme d&apos;orientation universitaire pour les bacheliers algériens.
            </p>
            <p className="text-xs text-gray-500 mt-3">
              Fondé par{' '}
              <span className="text-green-400 font-semibold">
                KHEDIM BENYAKHLEF dit Beny-Joe
              </span>
            </p>
          </div>

          {/* Colonne 2 - Liens */}
          <div>
            <h4 className="text-white font-semibold mb-3 text-sm">Navigation</h4>
            <div className="space-y-2 text-sm">
              <div><Link href="/orientation" className="hover:text-green-400 transition">Orientation</Link></div>
              <div><Link href="/filieres" className="hover:text-green-400 transition">Filières</Link></div>
              <div><Link href="/auth" className="hover:text-green-400 transition">Mon compte</Link></div>
            </div>
          </div>

          {/* Colonne 3 - Kinsta */}
          <div>
            <h4 className="text-white font-semibold mb-3 text-sm">Hébergement recommandé</h4>
            <a
              href="https://kinsta.com/?kaid=HUFPGOMPMRPI"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-3 bg-[#1a1a2e] border border-gray-700 rounded-xl p-3 hover:border-orange-500 transition group"
            >
              <div className="bg-white rounded-lg p-1.5">
                <svg width="24" height="24" viewBox="0 0 100 100" fill="none">
                  <rect width="100" height="100" rx="12" fill="#1a1a2e"/>
                  <path d="M20 20 L20 80 L38 80 L38 55 L62 80 L84 80 L56 48 L82 20 L60 20 L38 45 L38 20 Z" fill="#ffffff"/>
                </svg>
              </div>
              <div>
                <div className="text-white font-bold text-sm group-hover:text-orange-400 transition">Kinsta</div>
                <div className="text-gray-400 text-xs">Cloud ultra-rapide</div>
              </div>
            </a>
            <p className="text-xs text-gray-500 mt-2">
              Lien affilié — supporte le projet en t&apos;inscrivant
            </p>
          </div>
        </div>

        <div className="border-t border-gray-800 pt-6 text-center text-xs text-gray-500">
          © 2025 Orientation DZ — Fondé par{' '}
          <span className="text-gray-300">KHEDIM BENYAKHLEF dit Beny-Joe</span>
          {' '}· Données MESRS Algérie
        </div>
      </div>
    </footer>
  )
}
