import {
  AbsoluteFill,
  Audio,
  Easing,
  Img,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
} from 'remotion';
import type {ReactNode} from 'react';
import {scenes} from './script';

const colors = {
  bg: '#02070c',
  panel: 'rgba(7, 18, 27, 0.82)',
  orange: '#ff8a24',
  orangeSoft: 'rgba(255, 138, 36, 0.2)',
  green: '#83de79',
  greenSoft: 'rgba(131, 222, 121, 0.18)',
  blue: '#65b9ff',
  blueSoft: 'rgba(101, 185, 255, 0.18)',
  text: '#f6f7f8',
  muted: '#c8d0d6',
};

const sceneDurations = [181, 249, 353, 420, 242, 570, 251, 270];
const totalFrames = sceneDurations.reduce((sum, duration) => sum + duration, 0);
const fade = 24;

const fadeValue = (frame: number, duration: number) => {
  return interpolate(frame, [0, fade, duration - fade, duration], [0, 1, 1, 0], {
    easing: Easing.bezier(0.16, 1, 0.3, 1),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
};

const Shell = ({children}: {children: ReactNode}) => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      style={{
        background:
          'radial-gradient(circle at 68% 47%, rgba(255,138,36,0.2), transparent 24%), radial-gradient(circle at 18% 24%, rgba(101,185,255,0.12), transparent 26%), #02070c',
        color: colors.text,
        fontFamily:
          'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
        overflow: 'hidden',
      }}
    >
      <div
        style={{
          inset: 0,
          opacity: 0.2,
          position: 'absolute',
          backgroundImage:
            'linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px)',
          backgroundSize: '80px 80px',
          translate: `${interpolate(frame, [0, totalFrames], [0, -80])}px 0`,
        }}
      />
      <div
        style={{
          position: 'absolute',
          inset: 72,
          border: `1px solid rgba(255, 138, 36, 0.22)`,
          boxShadow: 'inset 0 0 80px rgba(255, 138, 36, 0.08)',
        }}
      />
      {children}
    </AbsoluteFill>
  );
};

const Brand = () => {
  return (
    <div
      style={{
        alignItems: 'center',
        display: 'flex',
        gap: 22,
        left: 120,
        position: 'absolute',
        top: 84,
      }}
    >
      <div
        style={{
          alignItems: 'center',
          background: `linear-gradient(135deg, ${colors.orange}, #ff6f2c)`,
          borderRadius: 20,
          color: '#061018',
          display: 'flex',
          fontSize: 38,
          fontWeight: 900,
          height: 72,
          justifyContent: 'center',
          width: 72,
        }}
      >
        RS
      </div>
      <div style={{fontSize: 46, fontWeight: 780, letterSpacing: 0}}>
        RelayStack
      </div>
    </div>
  );
};

const IntroScene = ({duration}: {duration: number}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [duration - fade, duration], [1, 0], {
    easing: Easing.bezier(0.16, 1, 0.3, 1),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <Shell>
      <Img
        src={staticFile('assets/opening.png')}
        style={{
          height: '100%',
          inset: 0,
          objectFit: 'cover',
          opacity,
          position: 'absolute',
          width: '100%',
        }}
      />
    </Shell>
  );
};

const ProblemScene = ({duration, index}: {duration: number; index: number}) => {
  const frame = useCurrentFrame();
  const scene = scenes[index];
  const opacity = fadeValue(frame, duration);
  const points = ['决策留在聊天里', 'diff 看不到为什么', '风险和验证状态丢失'];

  return (
    <Shell>
      <Brand />
      <div
        style={{
          alignItems: 'center',
          display: 'grid',
          gap: 70,
          gridTemplateColumns: '1fr 1fr',
          inset: '210px 120px 140px',
          opacity,
          position: 'absolute',
        }}
      >
        <div>
          <div style={{color: colors.blue, fontSize: 30, fontWeight: 760}}>
            {scene.kicker}
          </div>
          <div style={{fontSize: 82, fontWeight: 900, lineHeight: 1.08, marginTop: 22}}>
            {scene.title}
          </div>
          <div style={{color: colors.muted, fontSize: 34, lineHeight: 1.5, marginTop: 34}}>
            {scene.body}
          </div>
        </div>
        <div style={{display: 'flex', flexDirection: 'column', gap: 26}}>
          {points.map((point, itemIndex) => (
            <div
              key={point}
              style={{
                alignItems: 'center',
                background: colors.panel,
                border: `1px solid ${itemIndex === 1 ? colors.orange : colors.blue}`,
                boxShadow: `0 0 42px ${itemIndex === 1 ? colors.orangeSoft : colors.blueSoft}`,
                display: 'flex',
                fontSize: 34,
                fontWeight: 720,
                gap: 26,
                minHeight: 120,
                opacity: interpolate(frame, [itemIndex * 18, itemIndex * 18 + 24], [0, 1], {
                  extrapolateRight: 'clamp',
                }),
                padding: '0 38px',
                translate: `${interpolate(frame, [itemIndex * 18, itemIndex * 18 + 24], [38, 0], {
                  easing: Easing.bezier(0.16, 1, 0.3, 1),
                  extrapolateRight: 'clamp',
                })}px 0`,
              }}
            >
              <span style={{color: colors.orange, fontSize: 52}}>×</span>
              {point}
            </div>
          ))}
        </div>
      </div>
    </Shell>
  );
};

const SnapshotScene = ({duration, index}: {duration: number; index: number}) => {
  const frame = useCurrentFrame();
  const scene = scenes[index];
  const opacity = fadeValue(frame, duration);
  const items = ['current goal', 'what changed', 'why this path', 'risks', 'next action', 'validation plan'];

  return (
    <Shell>
      <Brand />
      <div
        style={{
          alignItems: 'center',
          display: 'grid',
          gap: 72,
          gridTemplateColumns: '0.9fr 1.1fr',
          inset: '210px 120px 130px',
          opacity,
          position: 'absolute',
        }}
      >
        <div>
          <div style={{color: colors.orange, fontSize: 30, fontWeight: 760}}>
            {scene.kicker}
          </div>
          <div style={{fontSize: 78, fontWeight: 900, lineHeight: 1.1, marginTop: 22}}>
            {scene.title}
          </div>
          <div style={{color: colors.muted, fontSize: 34, lineHeight: 1.5, marginTop: 34}}>
            {scene.body}
          </div>
        </div>
        <div
          style={{
            background: colors.panel,
            border: `2px solid ${colors.orange}`,
            boxShadow: '0 0 80px rgba(255, 138, 36, 0.24)',
            padding: 48,
          }}
        >
          <div style={{color: colors.orange, fontSize: 32, fontWeight: 820}}>
            handoff/snapshot-&lt;timestamp&gt;.md
          </div>
          <div style={{display: 'grid', gap: 18, marginTop: 34}}>
            {items.map((item, itemIndex) => (
              <div
                key={item}
                style={{
                  alignItems: 'center',
                  color: colors.text,
                  display: 'flex',
                  fontSize: 31,
                  gap: 18,
                  opacity: interpolate(frame, [20 + itemIndex * 10, 44 + itemIndex * 10], [0, 1], {
                    extrapolateRight: 'clamp',
                  }),
                }}
              >
                <span style={{color: colors.orange}}>•</span>
                {item}
              </div>
            ))}
          </div>
        </div>
      </div>
    </Shell>
  );
};

const Metric = ({label, value, color}: {label: string; value: string; color: string}) => {
  return (
    <div
      style={{
        background: colors.panel,
        border: `1px solid ${color}`,
        boxShadow: `0 0 46px ${color === colors.green ? colors.greenSoft : colors.orangeSoft}`,
        display: 'flex',
        flexDirection: 'column',
        gap: 12,
        justifyContent: 'center',
        minHeight: 185,
        padding: '34px 40px',
      }}
    >
      <div style={{color: colors.muted, fontSize: 28}}>{label}</div>
      <div style={{color, fontSize: 62, fontWeight: 900}}>{value}</div>
    </div>
  );
};

const dialCenters = [156, 388, 620, 852];

const AnimatedDialImage = ({
  asset,
  frame,
  values,
}: {
  asset: string;
  frame: number;
  values: number[];
}) => {
  const progress = interpolate(frame, [22, 116], [0, 1], {
    easing: Easing.bezier(0.16, 1, 0.3, 1),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div
      style={{
        border: `1px solid rgba(131, 222, 121, 0.22)`,
        boxShadow: '0 0 70px rgba(101, 185, 255, 0.12)',
        height: 560,
        overflow: 'hidden',
        position: 'relative',
        width: 995,
      }}
    >
      <Img
        src={staticFile(`assets/${asset}`)}
        style={{
          filter: 'grayscale(1) brightness(0.42)',
          height: '100%',
          objectFit: 'cover',
          opacity: 0.7,
          position: 'absolute',
          width: '100%',
        }}
      />
      <Img
        src={staticFile(`assets/${asset}`)}
        style={{
          height: '100%',
          objectFit: 'cover',
          opacity: 0.42,
          position: 'absolute',
          width: '100%',
        }}
      />
      <svg height="560" style={{inset: 0, position: 'absolute'}} viewBox="0 0 995 560" width="995">
        {values.map((value, itemIndex) => (
          <circle
            cx={dialCenters[itemIndex]}
            cy={263}
            fill="none"
            key={itemIndex}
            pathLength={100}
            r={67}
            stroke={itemIndex === 3 && asset === 'continuation-cost-dials.svg' ? colors.blue : colors.green}
            strokeDasharray={`${value * progress} ${100 - value * progress}`}
            strokeLinecap="round"
            strokeWidth={18}
            style={{
              filter: `drop-shadow(0 0 12px ${
                itemIndex === 3 && asset === 'continuation-cost-dials.svg'
                  ? colors.blueSoft
                  : colors.greenSoft
              })`,
            }}
            transform={`rotate(-90 ${dialCenters[itemIndex]} 263)`}
          />
        ))}
      </svg>
    </div>
  );
};

const BenchmarkScene = ({duration, index}: {duration: number; index: number}) => {
  const frame = useCurrentFrame();
  const scene = scenes[index];
  const opacity = fadeValue(frame, duration);

  return (
    <Shell>
      <Brand />
      <div
        style={{
          alignItems: 'center',
          display: 'grid',
          gap: 54,
          gridTemplateColumns: '0.7fr 1.3fr',
          inset: '210px 120px 110px',
          opacity,
          position: 'absolute',
        }}
      >
        <div>
          <div style={{color: colors.green, fontSize: 30, fontWeight: 760}}>
            {scene.kicker}
          </div>
          <div style={{fontSize: 78, fontWeight: 900, lineHeight: 1.08, marginTop: 18}}>
            {scene.title}
          </div>
          <div style={{color: colors.muted, fontSize: 32, lineHeight: 1.5, marginTop: 34}}>
            {scene.body}
          </div>
        </div>
        <AnimatedDialImage asset="continuation-cost-dials.svg" frame={frame} values={[75.9, 77, 0, 88.3]} />
      </div>
    </Shell>
  );
};

const EvidenceScene = ({duration, index}: {duration: number; index: number}) => {
  const frame = useCurrentFrame();
  const scene = scenes[index];
  const opacity = fadeValue(frame, duration);
  const metricProgress = interpolate(frame, [22, 112], [0, 1], {
    easing: Easing.bezier(0.16, 1, 0.3, 1),
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <Shell>
      <Brand />
      <div
        style={{
          alignItems: 'center',
          display: 'grid',
          gap: 72,
          gridTemplateColumns: '1fr 1fr',
          inset: '210px 120px 120px',
          opacity,
          position: 'absolute',
        }}
      >
        <div>
          <div style={{color: colors.green, fontSize: 30, fontWeight: 760}}>
            {scene.kicker}
          </div>
          <div style={{fontSize: 82, fontWeight: 900, lineHeight: 1.08, marginTop: 22}}>
            {scene.title}
          </div>
          <div style={{color: colors.muted, fontSize: 34, lineHeight: 1.5, marginTop: 34}}>
            {scene.body}
          </div>
        </div>
        <div
          style={{
            alignItems: 'center',
            background: colors.panel,
            border: `1px solid ${colors.green}`,
            boxShadow: '0 0 64px rgba(131, 222, 121, 0.18)',
            display: 'grid',
            gap: 28,
            gridTemplateRows: '1fr 1fr',
            minHeight: 500,
            padding: 50,
          }}
        >
          <div
            style={{
              alignItems: 'center',
              border: `1px solid ${colors.blue}`,
              display: 'grid',
              gap: 28,
              gridTemplateColumns: '180px 1fr',
              padding: '28px 32px',
            }}
          >
            <svg height="154" viewBox="0 0 154 154" width="154">
              <circle cx="77" cy="77" fill="none" r="57" stroke="rgba(255,255,255,0.18)" strokeWidth="20" />
              <circle
                cx="77"
                cy="77"
                fill="none"
                pathLength={100}
                r="57"
                stroke={colors.blue}
                strokeDasharray={`${88.3 * metricProgress} ${100 - 88.3 * metricProgress}`}
                strokeLinecap="round"
                strokeWidth="20"
                transform="rotate(-90 77 77)"
              />
              <text fill={colors.text} fontSize="34" fontWeight="900" textAnchor="middle" x="77" y="73">
                53/60
              </text>
              <text fill={colors.muted} fontSize="17" fontWeight="700" textAnchor="middle" x="77" y="101">
                wins
              </text>
            </svg>
            <div>
              <div style={{color: colors.blue, fontSize: 34, fontWeight: 820}}>Reviewer signal</div>
              <div style={{color: colors.muted, fontSize: 28, lineHeight: 1.42, marginTop: 10}}>
                扩展 20 题盲评中获得 53 个 reviewer 胜场
              </div>
            </div>
          </div>
          <div
            style={{
              alignItems: 'center',
              border: `1px solid ${colors.green}`,
              display: 'grid',
              gap: 28,
              gridTemplateColumns: '180px 1fr',
              padding: '28px 32px',
            }}
          >
            <div style={{alignItems: 'center', display: 'flex', gap: 18, justifyContent: 'center'}}>
              <span style={{color: colors.orange, fontSize: 76, fontWeight: 900}}>4</span>
              <span style={{color: colors.muted, fontSize: 48}}>→</span>
              <span style={{color: colors.green, fontSize: 76, fontWeight: 900}}>0</span>
            </div>
            <div>
              <div style={{color: colors.green, fontSize: 34, fontWeight: 820}}>Known-info repeats</div>
              <div style={{color: colors.muted, fontSize: 28, lineHeight: 1.42, marginTop: 10}}>
                Evidence Map 把已知事实和来源绑定到交接里
              </div>
            </div>
          </div>
        </div>
      </div>
    </Shell>
  );
};

const SmokeScene = ({duration, index}: {duration: number; index: number}) => {
  const frame = useCurrentFrame();
  const scene = scenes[index];
  const opacity = fadeValue(frame, duration);

  return (
    <Shell>
      <Brand />
      <div
        style={{
          alignItems: 'center',
          display: 'grid',
          gap: 70,
          gridTemplateColumns: '1fr 1fr',
          inset: '210px 120px 110px',
          opacity,
          position: 'absolute',
        }}
      >
        <div>
          <div style={{color: colors.blue, fontSize: 30, fontWeight: 760}}>
            {scene.kicker}
          </div>
          <div style={{fontSize: 76, fontWeight: 900, lineHeight: 1.08, marginTop: 22}}>
            {scene.title}
          </div>
          <div style={{color: colors.muted, fontSize: 32, lineHeight: 1.5, marginTop: 34}}>
            {scene.body}
          </div>
        </div>
        <AnimatedDialImage asset="project-skills-ab-dials.svg" frame={frame} values={[34.1, 81.3, 50, 55.6]} />
      </div>
    </Shell>
  );
};

const ClosingScene = ({duration, index}: {duration: number; index: number}) => {
  const frame = useCurrentFrame();
  const scene = scenes[index];
  const opacity = fadeValue(frame, duration);

  return (
    <Shell>
      <Brand />
      <div
        style={{
          alignItems: 'center',
          display: 'flex',
          flexDirection: 'column',
          gap: 34,
          inset: '250px 220px 150px',
          justifyContent: 'center',
          opacity,
          position: 'absolute',
          textAlign: 'center',
        }}
      >
        <div style={{color: colors.orange, fontSize: 34, fontWeight: 760}}>
          {scene.kicker}
        </div>
        <div style={{fontSize: 92, fontWeight: 920, lineHeight: 1.08}}>
          {scene.title}
        </div>
        <div style={{color: colors.muted, fontSize: 36, lineHeight: 1.5, maxWidth: 1080}}>
          {scene.body}
        </div>
        <div
          style={{
            background: colors.panel,
            border: `1px solid ${colors.orange}`,
            color: colors.orange,
            fontSize: 32,
            fontWeight: 800,
            marginTop: 20,
            padding: '28px 44px',
          }}
        >
          install repo-local skills → run rs-handoff → continue with evidence
        </div>
      </div>
    </Shell>
  );
};

const renderScene = (index: number, duration: number) => {
  if (index === 0) return <IntroScene duration={duration} />;
  if (index === 1 || index === 6) return <ProblemScene duration={duration} index={index} />;
  if (index === 2) return <SnapshotScene duration={duration} index={index} />;
  if (index === 3) return <BenchmarkScene duration={duration} index={index} />;
  if (index === 4) return <EvidenceScene duration={duration} index={index} />;
  if (index === 5) return <SmokeScene duration={duration} index={index} />;
  return <ClosingScene duration={duration} index={index} />;
};

export const RelayStackIntro = () => {
  return (
    <AbsoluteFill>
      {scenes.map((_scene, index) => {
        const duration = sceneDurations[index] ?? 270;
        const from = sceneDurations.slice(0, index).reduce((sum, item) => sum + item, 0);

        return (
          <Sequence durationInFrames={duration} from={from} key={index}>
            {renderScene(index, duration)}
            <Audio
              src={staticFile(`voiceover/relaystack-intro/scene-${String(index + 1).padStart(2, '0')}.mp3`)}
              volume={0.96}
            />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
