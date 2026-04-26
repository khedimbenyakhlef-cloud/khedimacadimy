import axios from 'axios'
import type {
  TokenResponse, Recommandation, RequeteOrientation,
  Filiere, SerieOption, InteretOption, Universite, Temoignage,
  Utilisateur, ProfilBac,
} from '@/types'

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

// Injecter le token JWT automatiquement
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('token')
    if (token) config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Rediriger vers /auth si 401
api.interceptors.response.use(
  (r) => r,
  (err) => {
    if (err.response?.status === 401 && typeof window !== 'undefined') {
      localStorage.removeItem('token')
      window.location.href = '/auth'
    }
    return Promise.reject(err)
  }
)

// ─── Auth ──────────────────────────────────────────────────────
export const authApi = {
  inscrire: (data: {
    nom: string; prenom: string; email: string
    password: string; num_dossier_bac?: string; wilaya_id?: number
  }) => api.post<TokenResponse>('/users/inscription', data).then(r => r.data),

  login: (email: string, password: string) => {
    const form = new URLSearchParams()
    form.append('username', email)
    form.append('password', password)
    return api.post<TokenResponse>('/users/login', form, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    }).then(r => r.data)
  },

  moi: () => api.get<Utilisateur>('/users/moi').then(r => r.data),

  updateProfil: (data: Partial<Utilisateur>) =>
    api.put<Utilisateur>('/users/moi', data).then(r => r.data),

  saveProfil: (data: Omit<ProfilBac, 'id'>) =>
    api.post<ProfilBac>('/users/moi/profil-bac', data).then(r => r.data),
}

// ─── Orientation ───────────────────────────────────────────────
export const orientationApi = {
  recommander: (req: RequeteOrientation) =>
    api.post<Recommandation[]>('/orientation/recommander', req).then(r => r.data),

  series: () =>
    api.get<SerieOption[]>('/orientation/series').then(r => r.data),

  interets: () =>
    api.get<InteretOption[]>('/orientation/interets').then(r => r.data),
}

// ─── Filieres ──────────────────────────────────────────────────
export const filieresApi = {
  liste: (params?: { domaine?: string; moyenne_min?: number }) =>
    api.get<Filiere[]>('/filieres', { params }).then(r => r.data),

  detail: (id: string) =>
    api.get<Filiere>(`/filieres/${id}`).then(r => r.data),

  universites: (id: string, annee?: number) =>
    api.get<Universite[]>(`/filieres/${id}/universites`, { params: { annee } }).then(r => r.data),

  temoignages: (id: string) =>
    api.get<{ note_moyenne: number; total: number; temoignages: Temoignage[] }>(
      `/filieres/${id}/temoignages`
    ).then(r => r.data),

  ajouterTemoignage: (id: string, data: { contenu: string; note: number }) =>
    api.post(`/filieres/${id}/temoignages`, data).then(r => r.data),
}

export default api
