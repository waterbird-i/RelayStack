import {
  AbsoluteFill,
  Audio,
  Easing,
  interpolate,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

const sceneFrames = 495;
const safe = 96;

const colors = {
  bg: "#101413",
  panel: "#1b211f",
  text: "#f6f1e8",
  muted: "#b6c2b8",
  green: "#8ee6b1",
  blue: "#86b7ff",
  amber: "#ffd166",
  coral: "#ff8a7a",
};

const scenes = [
  {
    title: "AI 完成任务，不等于工作能交接",
    subtitle: "真正丢失的是现场：目标、进度、原因、风险和验证。",
  },
  {
    title: "RelayStack 把现场变成快照",
    subtitle: "聊天线索、Git 证据、项目文档和 agent records 汇成 handoff snapshot。",
  },
  {
    title: "接手者先回答 7 个问题",
    subtitle: "当前目标、已完成、改动文件、原因、风险、下一步和验证方式。",
  },
  {
    title: "多 agent 并行也能合流",
    subtitle: "职责、写入范围、采纳状态、冲突和验证结果都进入交接证据。",
  },
  {
    title: "工作流是 skill-first",
    subtitle: "在现有 coding agent 里触发，不建重平台，不要求迁移工作方式。",
  },
  {
    title: "证据来自本地工作区",
    subtitle: "读取 Git 状态、owner docs 和可选 AgentRecord，输出 Markdown。",
  },
  {
    title: "衡量方式很直接",
    subtitle: "handoff success rate：接手者能正确回答多少交接问题。",
  },
  {
    title: "亮点不是总结更漂亮",
    subtitle: "而是证明 AI 工作可交接、可验证、可继续。",
  },
];

const totalFrames = sceneFrames * scenes.length;

const Pill = ({
  children,
  color,
  delay = 0,
}: {
  children: React.ReactNode;
  color: string;
  delay?: number;
}) => {
  const frame = useCurrentFrame();

  return (
    <div
      style={{
        borderRadius: 8,
        border: `2px solid ${color}`,
        color,
        padding: "18px 24px",
        fontSize: 34,
        fontWeight: 700,
        letterSpacing: 0,
        opacity: interpolate(frame, [delay, delay + 22], [0, 1], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: Easing.bezier(0.16, 1, 0.3, 1),
        }),
        translate: `0px ${interpolate(frame, [delay, delay + 22], [24, 0], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: Easing.bezier(0.16, 1, 0.3, 1),
        })}px`,
      }}
    >
      {children}
    </div>
  );
};

const Header = ({ index }: { index: number }) => {
  const frame = useCurrentFrame();
  const scene = scenes[index];

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 22,
        width: "100%",
        maxWidth: 1080,
        minWidth: 0,
        opacity: interpolate(frame, [0, 24, sceneFrames - 30, sceneFrames], [0, 1, 1, 0], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
          easing: Easing.bezier(0.16, 1, 0.3, 1),
        }),
      }}
    >
      <div style={{ color: colors.green, fontSize: 34, fontWeight: 800 }}>
        RelayStack
      </div>
      <div
        style={{
          color: colors.text,
          fontSize: 74,
          lineHeight: 1.06,
          fontWeight: 900,
          letterSpacing: 0,
        }}
      >
        {scene.title}
      </div>
      <div
        style={{
          color: colors.muted,
          fontSize: 36,
          lineHeight: 1.35,
          fontWeight: 600,
          letterSpacing: 0,
          maxWidth: 1120,
        }}
      >
        {scene.subtitle}
      </div>
    </div>
  );
};

const Background = () => {
  const frame = useCurrentFrame();
  const slow = interpolate(frame, [0, totalFrames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(circle at ${20 + slow * 60}% 15%, rgba(142,230,177,0.20), transparent 30%), linear-gradient(135deg, #101413, #191410 54%, #10201c)`,
      }}
    >
      <div
        style={{
          position: "absolute",
          inset: safe,
          border: "1px solid rgba(246,241,232,0.10)",
          borderRadius: 28,
        }}
      />
    </AbsoluteFill>
  );
};

const SceneShell = ({
  index,
  children,
}: {
  index: number;
  children: React.ReactNode;
}) => {
  return (
    <AbsoluteFill
      style={{
        padding: `${safe + 8}px ${safe + 36}px`,
        display: "grid",
        gridTemplateColumns: "minmax(0, 1.12fr) minmax(0, 0.88fr)",
        gap: 64,
        alignItems: "center",
        fontFamily:
          '-apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", sans-serif',
      }}
    >
      <Header index={index} />
      <div
        style={{
          minHeight: 620,
          minWidth: 0,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        {children}
      </div>
    </AbsoluteFill>
  );
};

const ScatteredContext = () => (
  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
    {[
      ["聊天", colors.coral],
      ["Git diff", colors.blue],
      ["决策", colors.amber],
      ["风险", colors.green],
      ["验证", colors.text],
      ["下一步", colors.muted],
    ].map(([label, color], index) => (
      <Pill key={label} color={color} delay={index * 10}>
        {label}
      </Pill>
    ))}
  </div>
);

const SnapshotFlow = () => {
  const frame = useCurrentFrame();
  const width = interpolate(frame, [40, 120], [0, 520], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.16, 1, 0.3, 1),
  });

  return (
    <div style={{ width: 720, display: "flex", flexDirection: "column", gap: 34 }}>
      <div style={{ display: "flex", gap: 20, justifyContent: "center" }}>
        {["Git", "Docs", "Agent"].map((label, index) => (
          <Pill key={label} color={[colors.blue, colors.green, colors.amber][index]} delay={index * 12}>
            {label}
          </Pill>
        ))}
      </div>
      <div
        style={{
          alignSelf: "center",
          height: 8,
          width,
          borderRadius: 8,
          background: colors.green,
        }}
      />
      <div
        style={{
          borderRadius: 14,
          background: colors.panel,
          border: `3px solid ${colors.green}`,
          padding: 42,
          color: colors.text,
          fontSize: 44,
          fontWeight: 900,
          textAlign: "center",
          opacity: interpolate(frame, [90, 128], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
        }}
      >
        handoff/snapshot.md
      </div>
    </div>
  );
};

const HandoffQuestions = () => (
  <div style={{ display: "flex", flexDirection: "column", gap: 18, width: 680 }}>
    {["当前目标", "已完成", "改动文件", "改动原因", "风险阻塞", "下一步", "验证方式"].map(
      (label, index) => (
        <Pill key={label} color={[colors.green, colors.blue, colors.amber, colors.coral, colors.text, colors.muted, colors.green][index]} delay={index * 12}>
          {label}
        </Pill>
      ),
    )}
  </div>
);

const AgentBoundaries = () => (
  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18 }}>
    {["职责", "写入范围", "采纳状态", "显式冲突", "验证结果", "文件重叠"].map(
      (label, index) => (
        <Pill key={label} color={index % 2 === 0 ? colors.green : colors.blue} delay={index * 8}>
          {label}
        </Pill>
      ),
    )}
  </div>
);

const AgentRelay = () => {
  const frame = useCurrentFrame();

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "1fr 180px 1fr",
        gap: 26,
        alignItems: "center",
        width: 760,
      }}
    >
      <Pill color={colors.blue}>Agent A</Pill>
      <div
        style={{
          height: 10,
          borderRadius: 10,
          background: colors.green,
          scale: interpolate(frame, [40, 120], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
        }}
      />
      <Pill color={colors.amber} delay={78}>
        Agent B
      </Pill>
      <div />
      <div
        style={{
          borderRadius: 10,
          border: `2px solid ${colors.green}`,
          color: colors.text,
          padding: 22,
          textAlign: "center",
          fontSize: 30,
          fontWeight: 900,
          opacity: interpolate(frame, [70, 110], [0, 1], {
            extrapolateLeft: "clamp",
            extrapolateRight: "clamp",
            easing: Easing.bezier(0.16, 1, 0.3, 1),
          }),
        }}
      >
        snapshot
      </div>
      <div />
    </div>
  );
};

const SkillBoundary = () => (
  <div style={{ width: 700, display: "flex", flexDirection: "column", gap: 18 }}>
    {[
      ["仓库内 skills", colors.green],
      ["人工字段 + 本地证据", colors.blue],
      ["handoff/snapshot.md", colors.amber],
    ].map(([label, color], index) => (
      <Pill key={label} color={color} delay={index * 14}>
        {label}
      </Pill>
    ))}
  </div>
);

const EvidenceSources = () => (
  <div style={{ display: "flex", flexDirection: "column", gap: 26, width: 720 }}>
    <Pill color={colors.green}>Git 状态 / diff</Pill>
    <Pill color={colors.blue} delay={18}>稳定项目文档</Pill>
    <Pill color={colors.amber} delay={36}>AgentRecord</Pill>
    <div
      style={{
        color: colors.muted,
        fontSize: 28,
        fontWeight: 700,
        textAlign: "center",
      }}
    >
      缺失来源写明，不靠猜
    </div>
  </div>
);

const HandoffScore = () => (
  <div style={{ width: 720, display: "flex", flexDirection: "column", gap: 24 }}>
    <Pill color={colors.green}>答对的问题</Pill>
    <Pill color={colors.blue} delay={18}>/</Pill>
    <Pill color={colors.amber} delay={36}>全部交接问题</Pill>
    <div style={{ color: colors.text, fontSize: 38, fontWeight: 900, textAlign: "center" }}>
      handoff success rate
    </div>
  </div>
);

const FinalFrame = () => (
  <div
    style={{
      borderRadius: 18,
      background: colors.panel,
      border: `3px solid ${colors.green}`,
      boxSizing: "border-box",
      padding: 46,
      width: 660,
      color: colors.text,
      display: "flex",
      flexDirection: "column",
      gap: 30,
    }}
  >
    <div style={{ fontSize: 56, fontWeight: 950, lineHeight: 1.05 }}>
      可交接
      <br />
      可验证
      <br />
      可继续
    </div>
    <div style={{ fontSize: 30, lineHeight: 1.35, color: colors.muted, fontWeight: 700 }}>
      能被交接的最小证据，胜过没人读的流程档案。
    </div>
  </div>
);

const visuals = [
  <ScatteredContext />,
  <SnapshotFlow />,
  <HandoffQuestions />,
  <AgentBoundaries />,
  <SkillBoundary />,
  <EvidenceSources />,
  <HandoffScore />,
  <FinalFrame />,
];

export const RelayStackIntro = () => {
  const { width, height } = useVideoConfig();

  return (
    <AbsoluteFill style={{ width, height, backgroundColor: colors.bg }}>
      <Audio src={staticFile("voiceover.wav")} />
      <Background />
      {scenes.map((_, index) => (
        <Sequence key={index} from={index * sceneFrames} durationInFrames={sceneFrames}>
          <SceneShell index={index}>{visuals[index]}</SceneShell>
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
