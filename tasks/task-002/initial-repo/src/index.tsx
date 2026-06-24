import {ensureHiddenFrameworkHeaderInCurrentUrl} from './utils/comatemobile/url';

const isComatemobile = window.location.pathname.includes('/comatemobile');

if (isComatemobile) {
    ensureHiddenFrameworkHeaderInCurrentUrl();
}

export {isComatemobile};

