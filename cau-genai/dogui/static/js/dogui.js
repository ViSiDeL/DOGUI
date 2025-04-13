// global sound play
window.playSound = function(soundId) {
    const audio = document.getElementById(soundId);
    if (audio) {
        audio.currentTime = 0; // restart if already playing
        audio.play();
    }
};

// click handling
document.addEventListener('DOMContentLoaded', function() {
    document.body.addEventListener('click', function(e) {
        const link = e.target.closest('a[href]');
        if (!link) return;
        
        // dogui links
        const href = link.getAttribute('href');
        if (href.startsWith('/') && !href.startsWith('//') && !href.startsWith('/#')) {
            e.preventDefault();
            
            // play sound if sound specified
            const soundId = link.getAttribute('data-sound');
            if (soundId) playSound(soundId);
            
            // load page
            loadPage(href);
            
            // history
            history.pushState({}, '', href);
        }
    });
    
    // back/forward navigation
    window.addEventListener('popstate', function() {
        loadPage(window.location.pathname);
    });
});

async function loadPage(url) {
    try {
        // loading class
        document.body.classList.add('page-transition');
        
        
        
    } catch (error) {
        console.error('Page load error:', error);
        window.location.href = url; // traditional navigation if error
    } finally {
        document.body.classList.remove('page-transition');
    }
}