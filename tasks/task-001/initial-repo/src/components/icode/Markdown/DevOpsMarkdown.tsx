import {useMemo} from 'react';

/**
 * 修复代码块标记前的空格问题
 * 将 ``` 前面的空格移除，确保代码块能正确解析
 */
const fixCodeBlockMarkers = (content: string): string => {
    return content.replace(/^[ \t]+(```)/gm, '$1');
};

export const DevOpsMarkdown = ({content = ''}: {content?: string}) => {
    const processedContent = useMemo(
        () => fixCodeBlockMarkers(content),
        [content]
    );

    return <div>{processedContent}</div>;
};

