import { createRoot } from 'react-dom/client'
import EzeosHero from './hero/EzeosHero'

// Mount after the page fonts settle, so the address pill never jumps when
// Inter Tight arrives. The poster frame shows for reduced motion (the kit
// handles that) and the loop pauses off screen.
const el = document.getElementById('demo')
if (el) {
  const mount = () => createRoot(el).render(<EzeosHero />)
  const fonts = (document as Document & { fonts?: FontFaceSet }).fonts
  if (fonts?.ready) fonts.ready.then(mount, mount)
  else mount()
}
