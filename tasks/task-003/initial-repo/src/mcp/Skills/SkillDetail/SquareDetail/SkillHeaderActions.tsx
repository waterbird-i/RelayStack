type Skill = {
    isHiddenWorkspace?: boolean;
};

const ActionButton = ({children, onClick}: {children: string; onClick: () => void}) => (
    <button onClick={onClick}>{children}</button>
);

export function SkillHeaderActions({skill}: {skill: Skill}) {
    const handleShare = () => {
        window.alert('share');
    };

    return (
        <ActionButton onClick={handleShare}>
            分享
        </ActionButton>
    );
}

