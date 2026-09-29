import Nav from '@/components/Nav'
import Hero from '@/components/Hero'
import Research from '@/components/Research'
import Publications from '@/components/Publications'
import Experience from '@/components/Experience'
import CVSection from '@/components/CVSection'
import Footer from '@/components/Footer'

export default function Home() {
  return (
    <>
      <Nav />
      <main>
        <Hero />
        <Research />
        <Publications />
        <Experience />
        <CVSection />
      </main>
      <Footer />
    </>
  )
}
