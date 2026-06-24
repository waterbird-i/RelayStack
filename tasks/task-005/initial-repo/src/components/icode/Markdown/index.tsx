import {useMemo} from 'react';
import {useCurrentUserName} from '@/hooks/useCurrentUserName';
import {MarkdownFrontMatter} from './MarkdownFrontMatter';
import {DevOpsMarkdown} from './DevOpsMarkdown';
import {parseMarkdownFrontMatter} from '@/utils/icode/markdownFrontMatter';

const enableFrontMatterPreview = (username?: string) => [
    'alice',
    'bob',
].includes(username || '');

export function Markdown({content}: {content: string}) {
    const username = useCurrentUserName();
    const parsed = useMemo(
        () => enableFrontMatterPreview(username)
            ? parseMarkdownFrontMatter(content)
            : {frontMatter: null, bodyContent: content},
        [content, username]
    );

    return (
        <>
            {parsed.frontMatter && <MarkdownFrontMatter data={parsed.frontMatter} />}
            <DevOpsMarkdown content={parsed.bodyContent} />
        </>
    );
}
