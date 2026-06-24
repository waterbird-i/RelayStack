enum SkillStatus {
    DRAFT = 'draft',
    PUBLISHING = 'publishing',
    PUBLISHED_HUB = 'published_hub',
    PUBLISHED_WORKSPACE = 'published_workspace',
}

export function getMoreMenuItems(skill: {status: SkillStatus}, hasEditPermission: boolean) {
    const items = [];

    if (hasEditPermission && ![
        SkillStatus.PUBLISHED_HUB,
        SkillStatus.PUBLISHED_WORKSPACE,
        SkillStatus.DRAFT,
    ].includes(skill.status)) {
        items.push({
            key: 'publish',
            label: '发布',
        });
    }

    return items;
}

