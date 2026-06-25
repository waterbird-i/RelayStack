import { Composition } from "remotion";
import { RelayStackIntro } from "./RelayStackIntro";

export const RemotionRoot = () => {
  return (
    <Composition
      id="RelayStackIntro"
      component={RelayStackIntro}
      durationInFrames={3960}
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
