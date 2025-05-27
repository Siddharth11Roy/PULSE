window.addEventListener('DOMContentLoaded', () => {
    if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
            async position => {
                const { latitude, longitude } = position.coords;

                // Call your backend to get events
                const response = await fetch(`/events/nearby?lat=${latitude}&lng=${longitude}`);
                const html = await response.text();  // or .json() if using JSON

                // Inject events into a div
                document.getElementById('nearby-events').innerHTML = html;
            },
            error => {
                console.error('Geolocation error:', error);
            }
        );
    } else {
        console.warn('Geolocation not supported');
    }
});
