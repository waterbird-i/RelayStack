import {SkillStatusTag} from './SkillStatusTag';

export function SkillHeader({skill}: {skill: object}) {
    return (
        <SkillStatusTag
            skill={skill}
        />
    );
}

