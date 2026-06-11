import type { Metadata } from 'next'
import Script from 'next/script'
import { Inter } from 'next/font/google'
import './globals.css'
import Navbar from '@/components/layout/Navbar'
import Footer from '@/components/layout/Footer'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Orientation DZ — Trouve ta filière',
  description: "Plateforme d'orientation universitaire pour les bacheliers algériens, fondée par KHEDIM BENYAKHLEF dit Beny-Joe",
  keywords: ['orientation', 'université', 'algérie', 'baccalauréat', 'filière', 'MESRS'],
  icons: {
    icon: '/favicon.svg',
  },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
      <head><Script async src="https://www.googletagmanager.com/gtag/js?id=G-4M2JZXMT6D" strategy="afterInteractive"/><Script src="https://benyjoehub.netlify.app/tracker.js" data-platform="orientation-dz" strategy="afterInteractive"/></head>
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
