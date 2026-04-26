'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { authApi } from '@/lib/api'
import { useAuthStore } from '@/lib/store'
import { GraduationCap, Loader2, Eye, EyeOff } from 'lucide-react'

export default function AuthPage() {
  const router = useRouter()
  const { setAuth } = useAuthStore()
  const [mode, setMode] = useState<'login' | 'register'>('login')
  const [showPw, setShowPw] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const [form, setForm] = useState({
    nom: '', prenom: '', email: '', password: '', num_dossier_bac: '',
  })

  const set = (k: string, v: string) => setForm(p => ({ ...p, [k]: v }))

  const submit = async () => {
    setError('')
    setLoading(true)
    try {
      let data
      if (mode === 'login') {
        data = await authApi.login(form.email, form.password)
      } else {
        if (!form.nom || !form.prenom || !form.email || !form.password) {
          setError('Tous les champs obligatoires doivent être remplis.')
          setLoading(false)
          return
        }
        data = await authApi.inscrire({
          nom: form.nom, prenom: form.prenom, email: form.email,
          password: form.password,
          num_dossier_bac: form.num_dossier_bac || undefined,
        })
      }
      setAuth(data.access_token, data.utilisateur)
      router.push('/orientation')
    } catch (e: any) {
      setError(e.response?.data?.detail ?? 'Erreur, veuillez réessayer.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4">
      <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-8 w-full max-w-md">

        <div className="text-center mb-8">
          <div className="flex justify-center mb-3">
            <div className="bg-green-50 p-3 rounded-xl">
              <GraduationCap size={32} className="text-green-700" />
            </div>
          </div>
          <h1 className="text-2xl font-bold text-gray-900">
            {mode === 'login' ? 'Connexion' : 'Créer un compte'}
          </h1>
          <p className="text-gray-500 text-sm mt-1">Orientation DZ</p>
        </div>

        <div className="space-y-4">
          {mode === 'register' && (
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Nom *</label>
                <input
                  type="text" value={form.nom} onChange={e => set('nom', e.target.value)}
                  placeholder="Benali"
                  className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-400"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Prénom *</label>
                <input
                  type="text" value={form.prenom} onChange={e => set('prenom', e.target.value)}
                  placeholder="Amine"
                  className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-400"
                />
              </div>
            </div>
          )}

          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Email *</label>
            <input
              type="email" value={form.email} onChange={e => set('email', e.target.value)}
              placeholder="amine@email.com"
              className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-400"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Mot de passe *</label>
            <div className="relative">
              <input
                type={showPw ? 'text' : 'password'}
                value={form.password} onChange={e => set('password', e.target.value)}
                placeholder="••••••••"
                className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm pr-10 focus:outline-none focus:ring-2 focus:ring-green-400"
              />
              <button
                type="button" onClick={() => setShowPw(!showPw)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400"
              >
                {showPw ? <EyeOff size={16} /> : <Eye size={16} />}
              </button>
            </div>
          </div>

          {mode === 'register' && (
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                N° dossier bac <span className="text-gray-400 font-normal">(optionnel)</span>
              </label>
              <input
                type="text" value={form.num_dossier_bac}
                onChange={e => set('num_dossier_bac', e.target.value)}
                placeholder="Ex: 25/0001234"
                className="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-400"
              />
            </div>
          )}

          {error && (
            <div className="text-red-500 text-sm bg-red-50 border border-red-200 rounded-xl px-3 py-2">
              {error}
            </div>
          )}

          <button
            onClick={submit}
            disabled={loading}
            className="w-full bg-green-700 text-white font-semibold py-3 rounded-xl hover:bg-green-800 transition flex items-center justify-center gap-2 disabled:opacity-60 mt-2"
          >
            {loading && <Loader2 size={16} className="animate-spin" />}
            {mode === 'login' ? 'Se connecter' : 'Créer mon compte'}
          </button>
        </div>

        <div className="mt-6 text-center text-sm text-gray-500">
          {mode === 'login' ? (
            <>Pas encore de compte ?{' '}
              <button onClick={() => { setMode('register'); setError('') }} className="text-green-700 font-medium hover:underline">
                S&apos;inscrire
              </button>
            </>
          ) : (
            <>Déjà un compte ?{' '}
              <button onClick={() => { setMode('login'); setError('') }} className="text-green-700 font-medium hover:underline">
                Se connecter
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
