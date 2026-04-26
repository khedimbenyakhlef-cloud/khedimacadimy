'use client'
import { useState, useEffect } from 'react'
import { orientationApi } from '@/lib/api'
import type { Recommandation, SerieOption, InteretOption } from '@/types'
import { Search, Loader2, Trophy, TrendingUp, MapPin, Clock, ChevronDown, ChevronUp } from 'lucide-react'

const SERIES_FALLBACK: SerieOption[] = [
  { code: 'sciences', label: 'Sciences de la nature et de la vie' },
  { code: 'maths', label: 'Mathématiques' },
  { code: 'technique', label: 'Technique mathématique' },
  { code: 'lettres', label: 'Lettres et philosophie' },
  { code: 'gestion', label: 'Gestion et économie' },
  { code: 'langues', label: 'Langues étrangères' },
]

const INTERETS_FALLBACK: InteretOption[] = [
  { code: 'tech', label: '💻 Technologie' },
  { code: 'sante', label: '🏥 Santé' },
  { code: 'business', label: '💼 Business' },
  { code: 'art', label: '🎨 Art & Design' },
  { code: 'sciences', label: '🔬 Sciences' },
  { code: 'social', label: '🤝 Sciences sociales' },
  { code: 'droit', label: '⚖️ Droit' },
  { code: 'agri', label: '🌾 Agriculture' },
]

function ScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
  return (
    <div className="flex items-center gap-3 text-xs">
      <span className="text-gray-500 w-20 shrink-0">{label}</span>
      <div className="flex-1 bg-gray-100 rounded-full h-1.5 overflow-hidden">
        <div className={`h-full rounded-full ${color}`} style={{ width: `${Math.min(value, 100)}%` }} />
      </div>
      <span className="text-gray-400 w-8 text-right">{value.toFixed(0)}</span>
    </div>
  )
}

function CarteReco({ r, rang }: { r: Recommandation; rang: number }) {
  const [open, setOpen] = useState(false)
  const isTop = rang === 1

  return (
    <div className={`bg-white rounded-2xl border ${isTop ? 'border-green-400 shadow-md' : 'border-gray-200'} p-5`}>
      <div className="flex items-start justify-between gap-2">
        <div className="flex items-center gap-3">
          <div className={`text-xl font-black ${isTop ? 'text-green-700' : 'text-gray-300'}`}>
            #{rang}
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 text-base">{r.filiere_nom}</h3>
            <div className="flex items-center gap-1 text-sm text-gray-500 mt-0.5">
              <MapPin size={13} /> {r.universite_nom} — {r.wilaya_nom}
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2 shrink-0">
          {r.confortable && (
            <span className="text-xs bg-green-50 text-green-700 border border-green-200 px-2 py-0.5 rounded-full">
              Confortable
            </span>
          )}
          {!r.confortable && r.accessible && (
            <span className="text-xs bg-orange-50 text-orange-700 border border-orange-200 px-2 py-0.5 rounded-full">
              Juste accessible
            </span>
          )}
          <span className="text-lg font-bold text-green-700">{r.score.toFixed(0)}%</span>
        </div>
      </div>

      <button
        onClick={() => setOpen(!open)}
        className="mt-4 flex items-center gap-1 text-xs text-gray-400 hover:text-gray-600 transition"
      >
        {open ? <><ChevronUp size={14} /> Masquer détails</> : <><ChevronDown size={14} /> Voir détails du score</>}
      </button>

      {open && (
        <div className="mt-3 space-y-2 pt-3 border-t border-gray-100">
          <ScoreBar label="Série" value={(r.details_score.serie / 35) * 100} color="bg-blue-400" />
          <ScoreBar label="Intérêts" value={(r.details_score.interets / 30) * 100} color="bg-purple-400" />
          <ScoreBar label="Moyenne" value={(r.details_score.moyenne / 25) * 100} color="bg-green-400" />
          <ScoreBar label="Emploi" value={(r.details_score.emploi / 10) * 100} color="bg-amber-400" />
        </div>
      )}
    </div>
  )
}

export default function OrientationPage() {
  const [series, setSeries] = useState<SerieOption[]>(SERIES_FALLBACK)
  const [interets, setInterets] = useState<InteretOption[]>(INTERETS_FALLBACK)
  const [moyenne, setMoyenne] = useState(13)
  const [serie, setSerie] = useState('')
  const [selectedInterets, setSelectedInterets] = useState<string[]>([])
  const [resultats, setResultats] = useState<Recommandation[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [searched, setSearched] = useState(false)

  useEffect(() => {
    orientationApi.series().then(setSeries).catch(() => {})
    orientationApi.interets().then(setInterets).catch(() => {})
  }, [])

  const toggleInteret = (code: string) =>
    setSelectedInterets(p => p.includes(code) ? p.filter(x => x !== code) : [...p, code])

  const chercher = async () => {
    if (!serie) { setError('Veuillez sélectionner votre série.'); return }
    setError('')
    setLoading(true)
    try {
      const data = await orientationApi.recommander({ moyenne, serie, interets: selectedInterets, top_n: 10 })
      setResultats(data)
      setSearched(true)
    } catch (e: any) {
      setError(e.response?.data?.detail ?? 'Erreur lors de la recherche.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Orientation universitaire</h1>
        <p className="text-gray-500 mt-1">Remplis ton profil pour obtenir des recommandations personnalisées.</p>
      </div>

      {/* Formulaire */}
      <div className="bg-white rounded-2xl border border-gray-200 p-6 mb-8 space-y-6">

        {/* Moyenne */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Moyenne du baccalauréat
          </label>
          <div className="flex items-center gap-4">
            <input
              type="range" min="9" max="20" step="0.25" value={moyenne}
              onChange={e => setMoyenne(parseFloat(e.target.value))}
              className="flex-1 accent-green-600"
            />
            <span className="text-2xl font-bold text-green-700 min-w-[56px] text-right">
              {moyenne.toFixed(2)}
            </span>
            <span className="text-gray-400 text-sm">/20</span>
          </div>
        </div>

        {/* Série */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Série du bac</label>
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
            {series.map(s => (
              <button
                key={s.code}
                onClick={() => setSerie(s.code)}
                className={`p-2.5 rounded-xl border text-sm transition text-left ${
                  serie === s.code
                    ? 'border-green-500 bg-green-50 text-green-800 font-medium'
                    : 'border-gray-200 text-gray-600 hover:border-green-300'
                }`}
              >
                {s.label}
              </button>
            ))}
          </div>
        </div>

        {/* Intérêts */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Centres d&apos;intérêt <span className="text-gray-400 font-normal">(plusieurs choix)</span>
          </label>
          <div className="flex flex-wrap gap-2">
            {interets.map(i => (
              <button
                key={i.code}
                onClick={() => toggleInteret(i.code)}
                className={`px-3 py-1.5 rounded-full border text-sm transition ${
                  selectedInterets.includes(i.code)
                    ? 'border-green-500 bg-green-50 text-green-800 font-medium'
                    : 'border-gray-200 text-gray-600 hover:border-green-300'
                }`}
              >
                {i.label}
              </button>
            ))}
          </div>
        </div>

        {error && <p className="text-red-500 text-sm">{error}</p>}

        <button
          onClick={chercher}
          disabled={loading}
          className="w-full bg-green-700 text-white font-semibold py-3 rounded-xl hover:bg-green-800 transition flex items-center justify-center gap-2 disabled:opacity-60"
        >
          {loading ? <Loader2 size={18} className="animate-spin" /> : <Search size={18} />}
          {loading ? 'Analyse en cours...' : 'Trouver mes filières'}
        </button>
      </div>

      {/* Résultats */}
      {searched && (
        <div>
          <div className="flex items-center gap-2 mb-4">
            <Trophy size={20} className="text-green-600" />
            <h2 className="text-xl font-semibold text-gray-900">
              {resultats.length} filières recommandées
            </h2>
          </div>
          {resultats.length === 0 ? (
            <div className="text-center py-12 text-gray-400">
              Aucune filière trouvée. Essaie une moyenne plus haute ou change de série.
            </div>
          ) : (
            <div className="space-y-4">
              {resultats.map((r, i) => (
                <CarteReco key={r.offre_id} r={r} rang={i + 1} />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
