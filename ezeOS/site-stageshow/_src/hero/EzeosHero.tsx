import { Stage } from '../kit/stage'
import type { Act } from '../kit/act'
import { Window, Bar, Text } from '../kit/window'
import { Phone, LockScreen, Notification } from '../kit/phone'
import { Roll, Collapse } from '../kit/motion'
import { Button } from '../kit/controls'
import { WhatsApp } from './whatsapp'
// ezeos.css is linked by the page (assets/demo-ezeos.css), apart from the kit's CSS

// ezeOS hero: the business gets found, its site opens, the message lands on
// the owner's phone. A device pair on the dark page: the browser pinned
// top-left and off the bottom, the clinic's phone straddling its right edge
// over the window's filler margin, present from frame one.
// Real words: the query (in the omnibox, as Chrome shows search terms), the
// clinic, its status and three actions; then the site's headline and its
// button; then the message. Everything else is bars.

type S = { page: 'busca' | 'site'; msg: boolean }

const initial: S = { page: 'busca', msg: false }
const POSTER: S = { page: 'site', msg: true }

const QUERY = 'harmonização facial centro'
const NOME = 'Clínica Aurora'
const DOMINIO = 'clinicaaurora.com.br'

const REST = { wide: { x: 600, y: 300 }, compact: { x: 312, y: 226 } }

async function script(a: Act<S>) {
  const rest = a.layout === 'compact' ? REST.compact : REST.wide
  await a.wait(1000)

  // 1. Found: the clinic's card, its Site button
  await a.move({ at: 'site-btn', x: 0.8, y: 0.62 })
  await a.wait(250)
  await a.click()
  await a.set({ page: 'site' })
  await a.wait(1500)

  // 2. Its own site, its WhatsApp button
  await a.move({ at: 'whats', x: 0.86, y: 0.62 })
  await a.wait(300)
  await a.click()
  await a.wait(450)

  // 3. Payoff: the message on the owner's phone
  await a.set({ msg: true })
  await a.move(rest)
  await a.wait(2600)

  // Reset in place, last change first: the message leaves, then the page
  await a.set({ msg: false })
  await a.wait(420)
  await a.set({ page: 'busca' })
  await a.wait(900)
}

const ORGANIC = [
  { url: 46, title: 182, lines: [420, 340] },
  { url: 58, title: 156, lines: [396, 300] },
  { url: 40, title: 170, lines: [410, 260] },
]

// A dark lock screen with a hint of the house blue, instead of the stock lilac
const WALL = 'radial-gradient(120% 80% at 30% 0%, #23394a 0%, #142029 45%, #0b0f12 100%)'

export default function EzeosHero() {
  return (
    <Stage
      width={1080}
      height={500}
      compact={{ below: 700, width: 358, height: 580 }}
      theme="dark"
      initial={initial}
      poster={POSTER}
      script={script}
      cursor={{ at: REST }}
      className="ezeos"
    >
      {(s, _rect, layout) => (
        <>
          <Window url={<Roll>{s.page === 'site' ? DOMINIO : QUERY}</Roll>} urlShape="pill" className="ez-window">
            <div className="ez-body">
              {/* Search results */}
              <div className="ez-page ez-busca" data-show={s.page === 'busca' || undefined}>
                <div className="ez-tabs">
                  {[34, 28, 44, 36].map((w, i) => (
                    <Bar key={i} w={w} h={6} tone={i === 0 ? 4 : 2} />
                  ))}
                </div>

                <div className="ez-local">
                  <div className="ez-local__text">
                    <Text className="ez-local__name">{NOME}</Text>
                    <Text className="ez-local__kind">Harmonização facial · Centro</Text>
                    <Text className="ez-local__open">Aberto agora</Text>
                    <div className="ez-local__actions">
                      <Button size="small" data-target="site-btn">Site</Button>
                      <Button size="small">Rotas</Button>
                      <Button size="small">Ligar</Button>
                    </div>
                  </div>
                  <div className="ez-map" aria-hidden>
                    <span className="ez-map__pin" />
                  </div>
                </div>

                {ORGANIC.map((r, i) => (
                  <div key={i} className="ez-organic">
                    <Bar w={r.url} h={5} tone={2} />
                    <Bar w={r.title} h={8} tone={3} />
                    {r.lines.map((w, j) => (
                      <Bar key={j} w={w} h={5} tone={2} />
                    ))}
                  </div>
                ))}
              </div>

              {/* The clinic's own site */}
              <div className="ez-page ez-site" data-show={s.page === 'site' || undefined}>
                <div className="ez-site__nav">
                  <Text className="ez-site__brand">{NOME}</Text>
                  <div className="ez-site__links">
                    <Bar w={38} h={5} tone={2} />
                    <Bar w={44} h={5} tone={2} />
                    <Bar w={34} h={5} tone={2} />
                  </div>
                </div>
                <div className="ez-site__hero">
                  <Bar w={92} h={5} tone={2} />
                  <Text className="ez-site__title" wrap>Harmonização facial no Centro.</Text>
                  <div className="ez-site__lines">
                    <Bar w={320} h={6} tone={2} />
                    <Bar w={268} h={6} tone={2} />
                  </div>
                  <Button variant="primary" size="large" className="ez-cta" data-target="whats" icon={<WhatsApp size={16} tile={false} />}>
                    Agendar pelo WhatsApp
                  </Button>
                </div>
                <div className="ez-site__cards">
                  {[0, 1, 2].map((i) => (
                    <div key={i} className="ez-site__card">
                      <Bar w={22} h={22} r={6} tone={2} />
                      <Bar w={[76, 64, 82][i]} h={6} tone={3} />
                      <Bar w={[112, 96, 104][i]} h={5} tone={2} />
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </Window>

          <Phone width={layout === 'compact' ? 326 : 284} frame="pro" dark wallpaper={WALL} className="ez-phone">
            <LockScreen size="satellite" stack="top" date="Sexta-feira, 13 de novembro">
              <Collapse open={s.msg} reveal="drop">
                <Notification
                  icon={<WhatsApp size={22} tile={false} />}
                  title="Mariana"
                  body="Oi! Vi o site e quero agendar uma avaliação."
                  time="agora"
                />
              </Collapse>
            </LockScreen>
          </Phone>
        </>
      )}
    </Stage>
  )
}
