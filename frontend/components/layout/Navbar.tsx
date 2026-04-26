'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Menu, X, LogOut, User } from 'lucide-react'
import { useState } from 'react'
import { useAuthStore } from '@/lib/store'

function LogoSVG({ size = 32 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
      <polygon points="50,20 95,45 50,55 5,45" fill="#15803d"/>
      <rect x="44" y="10" width="12" height="22" rx="3" fill="#166534"/>
      <rect x="38" y="8" width="24" height="8" rx="4" fill="#166534"/>
      <rect x="70" y="45" width="4" height="24" rx="2" fill="#15803d"/>
      <circle cx="72" cy="70" r="6" fill="#f59e0b"/>
      <path d="M25 48 Q25 78 50 82 Q75 78 75 48" fill="#166534"/>
    </svg>
  )
}

const liens = [
  { href: '/orientation', label: 'Orientation' },
  { href: '/filieres', label: 'Filières' },
  { href: '/carte', label: '🗺️ Carte' },
]

export default function Navbar() {
  const pathname = usePathname()
  const [open, setOpen] = useState(false)
  const { utilisateur, logout, isAuthenticated } = useAuthStore()

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
      <div className="max-w-6xl mx-auto px-4 flex items-center justify-between h-16">
        <Link href="/" className="flex items-center gap-2.5 font-black text-green-800 text-lg">
          <LogoSVG size={32} />
          <span>Orientation DZ</span>
        </Link>
        <div className="hidden md:flex items-center gap-6">
          {liens.map(({ href, label }) => (
            <Link key={href} href={href}
              className={`text-sm font-medium transition ${pathname.startsWith(href) ? 'text-green-700 border-b-2 border-green-700 pb-1' : 'text-gray-600 hover:text-green-700'}`}>
              {label}
            </Link>
          ))}
          <a href="https://kinsta.com/?kaid=HUFPGOMPMRPI" target="_blank" rel="noopener noreferrer"
            className="text-xs font-semibold bg-[#1a1a2e] text-white px-3 py-1.5 rounded-lg hover:bg-[#16213e] transition">
            ⚡ Kinsta
          </a>
          {isAuthenticated() ? (
            <div className="flex items-center gap-3">
              <Link href="/profil" className="flex items-center gap-1 text-sm text-gray-600 hover:text-green-700">
                <User size={16}/> {utilisateur?.prenom}
              </Link>
              <button onClick={logout} className="flex items-center gap-1 text-sm text-red-500 hover:text-red-700">
                <LogOut size={16}/> Déconnexion
              </button>
            </div>
          ) : (
            <Link href="/auth" className="bg-green-700 text-white text-sm font-medium px-4 py-2 rounded-lg hover:bg-green-800 transition">
              Connexion
            </Link>
          )}
        </div>
        <button className="md:hidden" onClick={() => setOpen(!open)}>
          {open ? <X size={24}/> : <Menu size={24}/>}
        </button>
      </div>
      {open && (
        <div className="md:hidden border-t border-gray-100 bg-white px-4 py-4 flex flex-col gap-4">
          {liens.map(({ href, label }) => (
            <Link key={href} href={href} onClick={() => setOpen(false)} className="text-gray-700 font-medium">{label}</Link>
          ))}
          <a href="https://kinsta.com/?kaid=HUFPGOMPMRPI" target="_blank" rel="noopener noreferrer"
            className="text-sm font-semibold text-[#1a1a2e]">⚡ Hébergement Kinsta</a>
          {isAuthenticated() ? (
            <button onClick={() => { logout(); setOpen(false) }} className="text-red-500 text-left">Déconnexion</button>
          ) : (
            <Link href="/auth" onClick={() => setOpen(false)} className="text-green-700 font-medium">Connexion / Inscription</Link>
          )}
        </div>
      )}
    </nav>
  )
}
