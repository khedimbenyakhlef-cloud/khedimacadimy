'use client'
import { useEffect, useState } from 'react'
import { filieresApi } from '@/lib/api'
import type { Filiere, Universite, Temoignage } from '@/types'
import { Clock, TrendingUp, MapPin, Star, BookOpen, ChevronLeft, Send } from 'lucide-react'
import Link from 'next/link'
import { useAuthStore } from '@/lib/store'

function Etoiles({ note }: { note: number }) {
  return (
    <div className="flex gap-0.5">
      {[1, 2, 3, 4, 5].map(i => (
        <Star key={i} size={14} className={i <= note ? 'text-amber-400 fill-amber-400' : 'text-gray-200'} />
      ))}
    </div>
  )
}

export default function DetailFilierePage({ params }: { params: { id: string } }) {
  const [filiere, setFiliere] = useState<Filiere | null>(null)
  const [universites, setUniversites] = useState<Universite[]>([])
  const [temos, setTemos] = useState<{ note_moyenne: number; total: number; temoignages: Temoignage[] } | null>(null)
  const [onglet, setOnglet] = useState<'info' | 'univ' | 'temos'>('info')
  const [contenu, setContenu] = useState('')
  const [note, setNote] = useState(5)
  const [submitting, setSubmitting] = useState(false)
  const { isAuthenticated } = useAuthStore()

  useEffect(() => {
    filieresApi.detail(params.id).then(setFiliere).catch(console.error)
    filieresApi.universites(params.id).then(setUniversites).catch(console.error)
    filieresApi.temoignages(params.id).then(setTemos).catch(console.error)
  }, [params.id])

  const envoyerTemoignage = async () => {
    if (contenu.length < 50) return
    setSubmitting(true)
    try {
      await filieresApi.ajouterTemoignage(params.id, { contenu, note })
      setContenu('')
      alert('Témoignage envoyé, en attente de validation.')
    } catch (e) {
      alert('Erreur lors de l\'envoi.')
    } finally {
      setSubmitting(false)
    }
  }

  if (!filiere) return <div className="text-center py-20 text-gray-400">Chargement...</div>

  return (
    <div className="max-w-4xl mx-auto px-4 py-10">
      <Link href="/filieres" className="flex items-center gap-1 text-sm text-gray-400 hover:text-green-700 mb-6 transition">
        <ChevronLeft size={16} /> Retour aux filières
      </Link>

      {/* En-tête */}
      <div className="bg-white rounded-2xl border border-gray-200 p-6 mb-6">
        <span className="text-xs font-medium text-green-700 bg-green-50 px-2 py-0.5 rounded-full">
          {filiere.domaine}
        </span>
        <h1 className="text-3xl font-bold text-gray-900 mt-3 mb-2">{filiere.nom}</h1>
        {filiere.description && <p className="text-gray-500">{filiere.description}</p>}

        <div className="flex flex-wrap gap-4 mt-5 text-sm text-gray-600">
          <span className="flex items-center gap-1.5">
            <Clock size={15} className="text-green-600" /> {filiere.duree_annees} ans
          </span>
          <span className="flex items-center gap-1.5">
            <BookOpen size={15} className="text-green-600" /> Moyenne min : {filiere.moyenne_min}/20
          </span>
          {filiere.taux_emploi && (
            <span className="flex items-center gap-1.5">
              <TrendingUp size={15} className="text-green-600" /> Taux d&apos;emploi : {filiere.taux_emploi}%
            </span>
          )}
        </div>

        {filiere.debouches && (
          <div className="mt-4 p-3 bg-gray-50 rounded-xl text-sm text-gray-600">
            <span className="font-medium text-gray-800">Débouchés : </span>
            {filiere.debouches}
          </div>
        )}
      </div>

      {/* Onglets */}
      <div className="flex gap-1 bg-gray-100 rounded-xl p-1 mb-6">
        {([['info', 'Informations'], ['univ', `Universités (${universites.length})`], ['temos', `Témoignages (${temos?.total ?? 0})`]] as const).map(([key, label]) => (
          <button
            key={key}
            onClick={() => setOnglet(key)}
            className={`flex-1 py-2 text-sm rounded-lg transition font-medium ${
              onglet === key ? 'bg-white text-green-700 shadow-sm' : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {label}
          </button>
        ))}
      </div>

      {/* Contenu onglet */}
      {onglet === 'info' && (
        <div className="bg-white rounded-2xl border border-gray-200 p-6">
          <h2 className="font-semibold text-gray-900 mb-3">Séries compatibles</h2>
          <div className="flex flex-wrap gap-2">
            {filiere.series_compatibles.map(s => (
              <span key={s} className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm border border-blue-200">{s}</span>
            ))}
          </div>
          <h2 className="font-semibold text-gray-900 mt-5 mb-3">Centres d&apos;intérêt associés</h2>
          <div className="flex flex-wrap gap-2">
            {filiere.interets_associes.map(i => (
              <span key={i} className="px-3 py-1 bg-purple-50 text-purple-700 rounded-full text-sm border border-purple-200">{i}</span>
            ))}
          </div>
        </div>
      )}

      {onglet === 'univ' && (
        <div className="space-y-3">
          {universites.length === 0
            ? <p className="text-center text-gray-400 py-10">Aucune université trouvée pour cette filière.</p>
            : universites.map(u => (
              <div key={u.universite_id} className="bg-white rounded-2xl border border-gray-200 p-4 flex items-center justify-between">
                <div>
                  <h3 className="font-medium text-gray-900">{u.nom}</h3>
                  <div className="flex items-center gap-1 text-sm text-gray-500 mt-1">
                    <MapPin size={13} /> {u.wilaya}
                    {u.capacite && <span className="ml-3">· {u.capacite} places</span>}
                  </div>
                </div>
                {u.moyenne_derniere && (
                  <div className="text-right">
                    <div className="text-xs text-gray-400">Dernier admis</div>
                    <div className="font-semibold text-green-700">{u.moyenne_derniere}/20</div>
                  </div>
                )}
              </div>
            ))
          }
        </div>
      )}

      {onglet === 'temos' && (
        <div className="space-y-4">
          {temos?.note_moyenne && (
            <div className="bg-amber-50 border border-amber-200 rounded-2xl p-4 flex items-center gap-3">
              <Etoiles note={Math.round(temos.note_moyenne)} />
              <span className="font-semibold text-amber-800">{temos.note_moyenne.toFixed(1)}/5</span>
              <span className="text-amber-600 text-sm">({temos.total} avis)</span>
            </div>
          )}

          {temos?.temoignages.map(t => (
            <div key={t.id} className="bg-white rounded-2xl border border-gray-200 p-4">
              <div className="flex items-center gap-2 mb-2">
                <Etoiles note={t.note} />
                <span className="text-xs text-gray-400">{t.date ? new Date(t.date).toLocaleDateString('fr-DZ') : ''}</span>
              </div>
              <p className="text-gray-700 text-sm leading-relaxed">{t.contenu}</p>
            </div>
          ))}

          {/* Formulaire témoignage */}
          {isAuthenticated() ? (
            <div className="bg-white rounded-2xl border border-gray-200 p-5">
              <h3 className="font-semibold text-gray-900 mb-3">Laisser un témoignage</h3>
              <div className="flex gap-1 mb-3">
                {[1, 2, 3, 4, 5].map(i => (
                  <button key={i} onClick={() => setNote(i)}>
                    <Star size={20} className={i <= note ? 'text-amber-400 fill-amber-400' : 'text-gray-200'} />
                  </button>
                ))}
              </div>
              <textarea
                value={contenu}
                onChange={e => setContenu(e.target.value)}
                placeholder="Partage ton expérience dans cette filière (min. 50 caractères)..."
                className="w-full border border-gray-200 rounded-xl p-3 text-sm resize-none h-28 focus:outline-none focus:ring-2 focus:ring-green-400"
              />
              <button
                onClick={envoyerTemoignage}
                disabled={submitting || contenu.length < 50}
                className="mt-3 flex items-center gap-2 bg-green-700 text-white px-4 py-2 rounded-xl text-sm font-medium hover:bg-green-800 transition disabled:opacity-50"
              >
                <Send size={15} /> Envoyer
              </button>
            </div>
          ) : (
            <div className="text-center text-gray-400 py-6 text-sm">
              <Link href="/auth" className="text-green-600 underline">Connecte-toi</Link> pour laisser un témoignage.
            </div>
          )}
        </div>
      )}
    </div>
  )
}
