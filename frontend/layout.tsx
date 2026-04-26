import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Navbar from '@/components/layout/Navbar'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Orientation DZ — Trouve ta filière',
  description: 'Plateforme d\'orientation universitaire pour les bacheliers algériens',
  keywords: ['orientation', 'université', 'algérie', 'baccalauréat', 'filière'],
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body className={inter.className}>
        <Navbar />
        <main className="min-h-screen bg-gray-50">
          {children}
        </main>
        <footer className="bg-white border-t border-gray-200 py-8 mt-16">
          <div className="max-w-6xl mx-auto px-4 text-center text-sm text-gray-500">
            <p>© 2025 Orientation DZ — Plateforme d&apos;aide à l&apos;orientation universitaire en Algérie</p>
            <p className="mt-1">Données basées sur les informations du MESRS</p>
          </div>
        </footer>
      </body>
    </html>
  )
}
