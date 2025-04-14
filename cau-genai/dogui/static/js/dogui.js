// global sound play
window.playSound = function(soundId) {
    const audio = document.getElementById(soundId);
    if (audio) {
        audio.currentTime = 0;
        audio.play().catch(e => console.log("Audio play prevented:", e));
    }
};

// click handling
document.addEventListener('DOMContentLoaded', function() {
    document.body.addEventListener('click', function(e) {
        const link = e.target.closest('a[href]');
        if (!link) return;
        
        const href = link.getAttribute('href');
        if (href.startsWith('/') && !href.startsWith('//') && !href.startsWith('/#')) {
            e.preventDefault();
            
            // play sound
            const soundId = link.getAttribute('data-sound');
            if (soundId) playSound(soundId);
            
            // navigate after (delay)
            setTimeout(() => {
                window.location.href = href;
            }, 500);
        }
    });
});