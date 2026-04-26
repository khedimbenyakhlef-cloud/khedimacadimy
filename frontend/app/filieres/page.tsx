'use client'
import { useEffect, useState } from 'react'
import { filieresApi } from '@/lib/api'
import type { Filiere } from '@/types'
import Link from 'next/link'
import { Search, BookOpen, Clock, TrendingUp, ChevronRight } from 'lucide-react'

const DOMAINES = ['Tous', 'Santé', 'Informatique', 'Ingénierie', 'Droit', 'Économie', 'Agriculture', 'Architecture']

export default function FilieresPage() {
  const [filieres, setFilieres] = useState<Filiere[]>([])
  const [loading, setLoading] = useState(true)
  const [recherche, setRecherche] = useState('')
  const [domaine, setDomaine] = useState('Tous')

  useEffect(() => {
    filieresApi.liste()
      .then(setFilieres)
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const filtrees = filieres.filter(f => {
    const matchSearch = f.nom.toLowerCase().includes(recherche.toLowerCase()) ||
      f.domaine.toLowerCase().includes(recherche.toLowerCase())
    const matchDomaine = domaine === 'Tous' || f.domaine === domaine
    return matchSearch && matchDomaine
  })

  return (
    <div className="max-w-5xl mx-auto px-4 py-10">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Toutes les filières</h1>
        <p className="text-gray-500 mt-1">Explorez les formations disponibles dans les universités algériennes.</p>
      </div>

      {/* Filtres */}
      <div className="flex flex-col sm:flex-row gap-3 mb-6">
        <div className="relative flex-1">
          <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Rechercher une filière..."
            value={recherche}
            onChange={e => setRecherche(e.target.value)}
            className="w-full pl-9 pr-4 py-2.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-green-400"
          />
        </div>
        <select
          value={domaine}
          onChange={e => setDomaine(e.target.value)}
          className="border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-400"
        >
          {DOMAINES.map(d => <option key={d}>{d}</option>)}
        </select>
      </div>

      {loading ? (
        <div className="text-center py-20 text-gray-400">Chargement des filières...</div>
      ) : (
        <>
          <p className="text-sm text-gray-400 mb-4">{filtrees.length} filières trouvées</p>
          <div className="grid sm:grid-cols-2 gap-4">
            {filtrees.map(f => (
              <Link
                key={f.id}
                href={`/filieres/${f.id}`}
                className="bg-white rounded-2xl border border-gray-200 p-5 hover:border-green-400 hover:shadow-sm transition group"
              >
                <div className="flex items-start justify-between">
                  <div>
                    <span className="text-xs font-medium text-green-700 bg-green-50 px-2 py-0.5 rounded-full">
                      {f.domaine}
                    </span>
                    <h3 className="font-semibold text-gray-900 mt-2 group-hover:text-green-700 transition">
                      {f.nom}
                    </h3>
                  </div>
                  <ChevronRight size={18} className="text-gray-300 group-hover:text-green-600 transition mt-1 shrink-0" />
                </div>

                <div className="flex items-center gap-4 mt-4 text-sm text-gray-500">
                  <span className="flex items-center gap-1">
                    <Clock size={13} /> {f.duree_annees} ans
                  </span>
                  <span className="flex items-center gap-1">
                    <BookOpen size={13} /> Moy. min : {f.moyenne_min}/20
                  </span>
                  {f.taux_emploi && (
                    <span className="flex items-center gap-1">
                      <TrendingUp size={13} /> {f.taux_emploi}%
                    </span>
                  )}
                </div>
              </Link>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
