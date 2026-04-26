'use client'
import Link from 'next/link'
import { GraduationCap, Search, MapPin, Star, ArrowRight, BookOpen, Users, TrendingUp } from 'lucide-react'

const stats = [
  { label: 'Filières disponibles', value: '200+', icon: BookOpen },
  { label: 'Universités', value: '107', icon: MapPin },
  { label: 'Wilayas couvertes', value: '58', icon: MapPin },
  { label: 'Bacheliers aidés', value: '12k+', icon: Users },
]

const etapes = [
  { num: '01', titre: 'Entrez votre profil', desc: 'Moyenne, série du bac et centres d\'intérêt' },
  { num: '02', titre: 'Obtenez vos recommandations', desc: 'Notre algorithme analyse 200+ filières et 107 universités' },
  { num: '03', titre: 'Comparez et choisissez', desc: 'Débouchés, taux d\'emploi, témoignages d\'étudiants' },
]

export default function HomePage() {
  return (
    <div>
      {/* Hero */}
      <section className="bg-gradient-to-br from-green-700 to-green-900 text-white py-24 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <div className="flex justify-center mb-6">
            <div className="bg-white/10 p-4 rounded-2xl">
              <GraduationCap size={48} className="text-white" />
            </div>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-4 leading-tight">
            Trouve ta filière universitaire
          </h1>
          <p className="text-xl text-green-100 mb-8 max-w-2xl mx-auto">
            La plateforme d&apos;orientation pour les bacheliers algériens.
            Recommandations personnalisées selon ta moyenne, ta série et tes passions.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              href="/orientation"
              className="bg-white text-green-800 font-semibold px-8 py-3 rounded-xl hover:bg-green-50 transition flex items-center justify-center gap-2"
            >
              <Search size={20} />
              Commencer l&apos;orientation
            </Link>
            <Link
              href="/filieres"
              className="border border-white/40 text-white font-semibold px-8 py-3 rounded-xl hover:bg-white/10 transition flex items-center justify-center gap-2"
            >
              <BookOpen size={20} />
              Explorer les filières
            </Link>
          </div>
        </div>
      </section>

      {/* Stats */}
      <section className="bg-white border-b border-gray-100 py-10">
        <div className="max-w-5xl mx-auto px-4 grid grid-cols-2 md:grid-cols-4 gap-6">
          {stats.map(({ label, value, icon: Icon }) => (
            <div key={label} className="text-center">
              <Icon size={24} className="text-green-600 mx-auto mb-2" />
              <div className="text-3xl font-bold text-gray-900">{value}</div>
              <div className="text-sm text-gray-500 mt-1">{label}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Comment ça marche */}
      <section className="py-20 px-4">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
            Comment ça marche ?
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            {etapes.map(({ num, titre, desc }) => (
              <div key={num} className="text-center">
                <div className="text-5xl font-black text-green-100 mb-4">{num}</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{titre}</h3>
                <p className="text-gray-500">{desc}</p>
              </div>
            ))}
          </div>
          <div className="text-center mt-12">
            <Link
              href="/orientation"
              className="inline-flex items-center gap-2 bg-green-700 text-white font-semibold px-8 py-3 rounded-xl hover:bg-green-800 transition"
            >
              Démarrer maintenant <ArrowRight size={18} />
            </Link>
          </div>
        </div>
      </section>

      {/* CTA Auth */}
      <section className="bg-green-50 border border-green-100 mx-4 rounded-2xl py-14 px-6 mb-16 max-w-5xl md:mx-auto text-center">
        <Star size={32} className="text-green-600 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-900 mb-2">
          Sauvegarde ton profil et tes recommandations
        </h2>
        <p className="text-gray-500 mb-6">
          Crée un compte gratuit pour retrouver tes résultats, laisser un témoignage et suivre l&apos;actualité des inscriptions.
        </p>
        <Link
          href="/auth"
          className="inline-flex items-center gap-2 bg-green-700 text-white font-semibold px-6 py-3 rounded-xl hover:bg-green-800 transition"
        >
          Créer un compte gratuit <ArrowRight size={18} />
        </Link>
      </section>
    </div>
  )
}
