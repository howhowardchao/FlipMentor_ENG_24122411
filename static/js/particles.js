/* particlesJS.load(@dom-id, @path-json, @callback (optional)); */
document.addEventListener("DOMContentLoaded", function() {
    particlesJS.load('particles-js', '/static/js/particles-config.json', function() {
        console.log('particles.js loaded');
    });
}); 