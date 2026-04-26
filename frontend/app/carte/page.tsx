'use client'
import { useState } from 'react'
import { MapPin, University, Search } from 'lucide-react'

const UNIVERSITES = [
  { nom: "USTHB", wilaya: "Alger", lat: 36.7067, lng: 3.1778, type: "univ", filieres: ["Informatique", "Mathématiques", "Physique"] },
  { nom: "UMBB Boumerdes", wilaya: "Boumerdes", lat: 36.7567, lng: 3.4775, type: "univ", filieres: ["Génie civil", "Génie électrique"] },
  { nom: "Université Oran 1", wilaya: "Oran", lat: 35.6969, lng: -0.6331, type: "univ", filieres: ["Médecine", "Droit", "Sciences"] },
  { nom: "Université Constantine 1", wilaya: "Constantine", lat: 36.3650, lng: 6.6147, type: "univ", filieres: ["Médecine", "Architecture"] },
  { nom: "Université Annaba", wilaya: "Annaba", lat: 36.9000, lng: 7.7667, type: "univ", filieres: ["Génie des mines", "Informatique"] },
  { nom: "Université Sétif 1", wilaya: "Sétif", lat: 36.1898, lng: 5.4108, type: "univ", filieres: ["Médecine", "Génie mécanique"] },
  { nom: "Université Batna", wilaya: "Batna", lat: 35.5561, lng: 6.1744, type: "univ", filieres: ["Architecture", "Sciences"] },
  { nom: "Université Tlemcen", wilaya: "Tlemcen", lat: 34.8828, lng: -1.3153, type: "univ", filieres: ["Médecine", "Droit"] },
  { nom: "Université Béjaïa", wilaya: "Béjaïa", lat: 36.7508, lng: 5.0564, type: "univ", filieres: ["Génie civil", "Économie"] },
  { nom: "Université Biskra", wilaya: "Biskra", lat: 34.8500, lng: 5.7333, type: "univ", filieres: ["Architecture", "Génie civil"] },
  { nom: "Université Blida", wilaya: "Blida", lat: 36.4800, lng: 2.8289, type: "univ", filieres: ["Aéronautique", "Médecine"] },
  { nom: "Université Tizi Ouzou", wilaya: "Tizi Ouzou", lat: 36.7167, lng: 4.0500, type: "univ", filieres: ["Génie électrique", "Droit"] },
  { nom: "ESI Alger", wilaya: "Alger", lat: 36.7525, lng: 3.0422, type: "ecole", filieres: ["Informatique", "IA"] },
  { nom: "École Polytechnique", wilaya: "Alger", lat: 36.7100, lng: 3.1800, type: "ecole", filieres: ["Génie", "Sciences"] },
  { nom: "Université M'sila", wilaya: "M'sila", lat: 35.7044, lng: 4.5439, type: "univ", filieres: ["Sciences", "Lettres"] },
]

const REGIONS = ["Toutes", "Nord", "Est", "Ouest", "Centre", "Sud"]

export default function CartePage() {
  const [recherche, setRecherche] = useState('')
  const [selected, setSelected] = useState<typeof UNIVERSITES[0] | null>(null)
  const [region, setRegion] = useState('Toutes')

  const filtrees = UNIVERSITES.filter(u =>
    u.nom.toLowerCase().includes(recherche.toLowerCase()) ||
    u.wilaya.toLowerCase().includes(recherche.toLowerCase())
  )

  return (
    <div className="max-w-6xl mx-auto px-4 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">🗺️ Carte des universités</h1>
        <p className="text-gray-500 mt-1">Explorez les universités algériennes par wilaya</p>
      </div>

      <div className="relative mb-6">
        <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
        <input
          type="text"
          placeholder="Rechercher une université ou wilaya..."
          value={recherche}
          onChange={e => setRecherche(e.target.value)}
          className="w-full pl-9 pr-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-400"
        />
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Carte SVG Algérie */}
        <div className="lg:col-span-2 bg-white rounded-2xl border border-gray-200 p-4 relative overflow-hidden" style={{minHeight: '500px'}}>
          <svg viewBox="0 0 800 700" className="w-full h-full" style={{minHeight: '450px'}}>
            {/* Fond Algérie simplifié */}
            <rect width="800" height="700" fill="#f0fdf4" rx="12"/>

            {/* Forme approximative de l'Algérie */}
            <path d="M 120 80 L 680 80 L 720 150 L 750 300 L 700 500 L 600 620 L 400 680 L 200 650 L 100 500 L 80 300 L 100 150 Z"
              fill="#dcfce7" stroke="#16a34a" strokeWidth="2"/>

            {/* Lignes de régions */}
            <line x1="120" y1="320" x2="750" y2="320" stroke="#86efac" strokeWidth="1" strokeDasharray="5,5"/>
            <text x="760" y="325" fontSize="12" fill="#6b7280">Sahara</text>

            {/* Points des universités */}
            {UNIVERSITES.map((u, i) => {
              const x = ((u.lng + 8) / 17) * 680 + 60
              const y = ((37 - u.lat) / 15) * 600 + 50
              const isSelected = selected?.nom === u.nom
              return (
                <g key={i} onClick={() => setSelected(u)} style={{cursor: 'pointer'}}>
                  <circle
                    cx={x} cy={y}
                    r={isSelected ? 14 : 10}
                    fill={u.type === 'ecole' ? '#f59e0b' : '#16a34a'}
                    stroke="white" strokeWidth="2"
                    opacity={isSelected ? 1 : 0.85}
                  />
                  {isSelected && (
                    <circle cx={x} cy={y} r={20} fill="none" stroke="#16a34a" strokeWidth="2" opacity="0.4"/>
                  )}
                  <text x={x} y={y + 4} textAnchor="middle" fontSize="9" fill="white" fontWeight="bold">
                    {u.type === 'ecole' ? 'E' : 'U'}
                  </text>
                  {isSelected && (
                    <text x={x} y={y - 18} textAnchor="middle" fontSize="10" fill="#15803d" fontWeight="bold">
                      {u.nom.substring(0, 15)}
                    </text>
                  )}
                </g>
              )
            })}

            {/* Légende */}
            <g transform="translate(20, 20)">
              <rect width="140" height="60" fill="white" rx="8" opacity="0.9"/>
              <circle cx="20" cy="20" r="8" fill="#16a34a"/>
              <text x="35" y="25" fontSize="11" fill="#374151">Université</text>
              <circle cx="20" cy="42" r="8" fill="#f59e0b"/>
              <text x="35" y="47" fontSize="11" fill="#374151">Grande école</text>
            </g>
          </svg>
        </div>

        {/* Liste des universités */}
        <div className="bg-white rounded-2xl border border-gray-200 overflow-hidden">
          <div className="p-4 border-b border-gray-100">
            <h2 className="font-semibold text-gray-900">{filtrees.length} établissements</h2>
          </div>
          <div className="overflow-y-auto" style={{maxHeight: '480px'}}>
            {filtrees.map((u, i) => (
              <button
                key={i}
                onClick={() => setSelected(u)}
                className={`w-full text-left p-4 border-b border-gray-50 hover:bg-green-50 transition ${selected?.nom === u.nom ? 'bg-green-50 border-l-4 border-l-green-500' : ''}`}
              >
                <div className="flex items-start gap-3">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-xs font-bold shrink-0 ${u.type === 'ecole' ? 'bg-amber-500' : 'bg-green-600'}`}>
                    {u.type === 'ecole' ? 'E' : 'U'}
                  </div>
                  <div>
                    <p className="font-medium text-gray-900 text-sm">{u.nom}</p>
                    <p className="text-xs text-gray-500 flex items-center gap-1 mt-0.5">
                      <MapPin size={10}/> {u.wilaya}
                    </p>
                  </div>
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Détail université sélectionnée */}
      {selected && (
        <div className="mt-6 bg-white rounded-2xl border border-green-200 p-6">
          <div className="flex items-start justify-between">
            <div>
              <h2 className="text-xl font-bold text-gray-900">{selected.nom}</h2>
              <p className="text-green-700 flex items-center gap-1 mt-1">
                <MapPin size={14}/> {selected.wilaya}
              </p>
            </div>
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${selected.type === 'ecole' ? 'bg-amber-100 text-amber-700' : 'bg-green-100 text-green-700'}`}>
              {selected.type === 'ecole' ? '🏛️ Grande école' : '🎓 Université'}
            </span>
          </div>
          <div className="mt-4">
            <p className="text-sm font-medium text-gray-700 mb-2">Filières disponibles :</p>
            <div className="flex flex-wrap gap-2">
              {selected.filieres.map((f, i) => (
                <span key={i} className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full text-sm">
                  {f}
                </span>
              ))}
            </div>
          </div>
          <div className="mt-4 text-xs text-gray-400">
            📍 Coordonnées : {selected.lat}°N, {selected.lng}°E
          </div>
        </div>
      )}
    </div>
  )
}
