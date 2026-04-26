import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Orientation DZ — Trouve ta filière',
  description: "Plateforme d'orientation universitaire pour les bacheliers algériens, fondée par KHEDIM BENYAKHLEF dit Beny-Joe",
  keywords: ['orientation', 'université', 'algérie', 'baccalauréat', 'filière', 'MESRS'],
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="fr">
      <body className={inter.className}>
        <Navbar />
        <main className="min-h-screen bg-gray-50">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  )
}
