const HIDE_FRAMEWORK_HEADER_PARAM = 'hideFrameworkHeader';
const HIDE_FRAMEWORK_HEADER_VALUE = 'true';

export function ensureHiddenFrameworkHeaderInCurrentUrl() {
    const url = new URL(window.location.href);

    if (!url.pathname.includes('/comatemobile')) {
        return;
    }

    if (url.searchParams.get(HIDE_FRAMEWORK_HEADER_PARAM) === HIDE_FRAMEWORK_HEADER_VALUE) {
        return;
    }

    url.searchParams.set(HIDE_FRAMEWORK_HEADER_PARAM, HIDE_FRAMEWORK_HEADER_VALUE);
    window.history.replaceState(window.history.state, '', `${url.pathname}${url.search}${url.hash}`);
}

