document.addEventListener('DOMContentLoaded', function() {
    const greetButton = document.getElementById('greetButton');
    const messageArea = document.getElementById('messageArea');

    new QWebChannel(qt.webChannelTransport, function(channel) {
        window.backend = channel.objects.backend;
    });

    greetButton.addEventListener('click', function() {
        const greeting = "🌊 hiiii! Button clicked! 🌊";
        messageArea.innerHTML = greeting;

        if (window.backend) {
            backend.home_btn(greeting);
        }
    });
});
