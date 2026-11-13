import React from 'react';
import {Composition} from 'remotion';
import {linearTiming, TransitionSeries} from '@remotion/transitions';
import {slide} from '@remotion/transitions/slide';
import {DURACAO, SLIDES} from './manifesto/Slides';
import {VandalSchool, VS_DUR} from './fuieu/VandalSchool';
import {ABAS_DUR, AbasRenata} from './reels/AbasRenata';
import {DUR7, DUR8, Reel7, Reel8} from './reels/Reels2';
import {DUR1, DUR2, DUR3, DUR4, DUR5, DUR6, Reel1, Reel2, Reel3, Reel4, Reel5, Reel6} from './reels/Reels';

const REELS: [React.FC, number][] = [[Reel1, DUR1], [Reel2, DUR2], [Reel3, DUR3], [Reel4, DUR4], [Reel5, DUR5], [Reel6, DUR6], [Reel7, DUR7], [Reel8, DUR8]];

const TRANS = 12; // quadros de transição entre slides na versão contínua

/** os 10 slides em sequência, um deslizando por cima do outro, como se fosse o carrossel passando sozinho */
const ManifestoCompleto: React.FC = () => (
  <TransitionSeries>
    {SLIDES.map((S, i) => (
      <React.Fragment key={i}>
        <TransitionSeries.Sequence durationInFrames={DURACAO[i]}><S /></TransitionSeries.Sequence>
        {i < SLIDES.length - 1 ? (
          <TransitionSeries.Transition presentation={slide({direction: 'from-right'})} timing={linearTiming({durationInFrames: TRANS})} />
        ) : null}
      </React.Fragment>
    ))}
  </TransitionSeries>
);

export const Root: React.FC = () => (
  <>
    {SLIDES.map((S, i) => (
      <Composition key={i} id={`Manifesto-${String(i + 1).padStart(2, '0')}`} component={S} durationInFrames={DURACAO[i]} fps={30} width={1080} height={1350} />
    ))}
    <Composition
      id="Manifesto-Completo" component={ManifestoCompleto} fps={30} width={1080} height={1350}
      durationInFrames={DURACAO.reduce((a, b) => a + b, 0) - TRANS * (SLIDES.length - 1)}
    />
    <Composition id="Carrossel-Renata-Abas" component={AbasRenata} durationInFrames={ABAS_DUR} fps={30} width={1080} height={1350} />
    <Composition id="FUIEU-VandalSchool-4x5" component={VandalSchool} defaultProps={{formato: '4x5' as const}} durationInFrames={VS_DUR} fps={30} width={1080} height={1350} />
    <Composition id="FUIEU-VandalSchool-9x16" component={VandalSchool} defaultProps={{formato: '9x16' as const}} durationInFrames={VS_DUR} fps={30} width={1080} height={1920} />
    {REELS.map(([R, d], i) => (
      <Composition key={`r${i}`} id={`Reel-0${i + 1}`} component={R} durationInFrames={d} fps={30} width={1080} height={1920} />
    ))}
  </>
);
