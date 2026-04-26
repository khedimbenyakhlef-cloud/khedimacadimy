import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { Utilisateur } from '@/types'

interface AuthState {
  token: string | null
  utilisateur: Utilisateur | null
  setAuth: (token: string, utilisateur: Utilisateur) => void
  logout: () => void
  isAuthenticated: () => boolean
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      token: null,
      utilisateur: null,

      setAuth: (token, utilisateur) => {
        localStorage.setItem('token', token)
        set({ token, utilisateur })
      },

      logout: () => {
        localStorage.removeItem('token')
        set({ token: null, utilisateur: null })
      },

      isAuthenticated: () => !!get().token,
    }),
    { name: 'orientation-dz-auth' }
  )
)
