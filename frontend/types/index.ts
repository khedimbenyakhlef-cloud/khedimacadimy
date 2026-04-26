// ─── Utilisateur ───────────────────────────────────────────────
export interface ProfilBac {
  id: string
  serie: string
  moyenne: number
  annee_bac: number | null
  interets: string[]
}

export interface Utilisateur {
  id: string
  nom: string
  prenom: string
  email: string
  num_dossier_bac: string | null
  wilaya_id: number | null
  profil: ProfilBac | null
}

export interface TokenResponse {
  access_token: string
  token_type: string
  utilisateur: Utilisateur
}

// ─── Filières ──────────────────────────────────────────────────
export interface Filiere {
  id: string
  nom: string
  domaine: string
  duree_annees: number
  moyenne_min: number
  series_compatibles: string[]
  interets_associes: string[]
  debouches: string | null
  taux_emploi: number | null
  description: string | null
}

// ─── Orientation ───────────────────────────────────────────────
export interface DetailsScore {
  serie: number
  interets: number
  moyenne: number
  emploi: number
}

export interface Recommandation {
  offre_id: string
  filiere_nom: string
  universite_nom: string
  wilaya_nom: string
  score: number
  rang: number
  accessible: boolean
  confortable: boolean
  details_score: DetailsScore
}

export interface RequeteOrientation {
  moyenne: number
  serie: string
  interets: string[]
  wilaya_id?: number
  top_n?: number
}

// ─── Refs ──────────────────────────────────────────────────────
export interface SerieOption {
  code: string
  label: string
}

export interface InteretOption {
  code: string
  label: string
}

export interface Wilaya {
  id: number
  nom: string
  code: string
  region: string
}

export interface Universite {
  universite_id: string
  nom: string
  wilaya: string | null
  capacite: number | null
  moyenne_derniere: number | null
  latitude: number | null
  longitude: number | null
}

export interface Temoignage {
  id: string
  contenu: string
  note: number
  date: string | null
}
