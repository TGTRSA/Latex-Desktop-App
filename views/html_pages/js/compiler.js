
let backend = null;

function saveContent(){
    const inputText = document.getElementById("inputField").value;
    if(backend){
        backend.saveContent(inputText);
    }else {
        let error = "[JS:saveContent] Cannot call backend"
        backend.logToPython(error);
    }
}

function logToPython(message) {
    if (backend) {
        backend.logToPython(message);
    } else {
        console.log(message);
    }
}

(function() {
            const compileBtn = document.getElementById('compileBtn');
            const inputField = document.getElementById('inputField');
            const displayField = document.getElementById('displayField');

            function compile() {
                const content = inputField.value;
                if (!content.trim()) {
                    showStatus('Empty input', '#c92a2a');
                    return;
                }
                
                // Your PDF generation logic here
                // For demo: update fallback text to show it worked
                const fallback = displayField.querySelector('p');
                if (fallback && (!displayField.data || displayField.data === '')) {
                    fallback.innerHTML = `Compiled: "${content.substring(0, 100)}${content.length > 100 ? '...' : ''}"`;
                }
                
                showStatus('Compiled successfully', '#2b8c4a');
            }

            function showStatus(msg, color) {
                const existing = document.querySelector('.status-toast');
                if (existing) existing.remove();
                
                const toast = document.createElement('div');
                toast.className = 'status-toast';
                toast.textContent = msg;
                toast.style.cssText = `
                    position: fixed;
                    bottom: 20px;
                    left: 50%;
                    transform: translateX(-50%);
                    background: ${color};
                    color: white;
                    padding: 8px 16px;
                    font-size: 13px;
                    font-family: monospace;
                    z-index: 1000;
                    pointer-events: none;
                `;
                document.body.appendChild(toast);
                setTimeout(() => toast.remove(), 2000);
            }

            compileBtn.addEventListener('click', compile);
            
            // Ctrl+Enter shortcut
            inputField.addEventListener('keydown', (e) => {
                if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                    e.preventDefault();
                    compile();
                }
            });
        })();

document.addEventListener('DOMContentLoaded', function() {
    let fileName = localStorage.getItem('fileName');
    let tex_input = localStorage.getItem('texInput');
    document.getElementById("inputField").value = tex_input;
    document.getElementById("fileName").innerText   = fileName;
    // Initialize Qt bridge
    logToPython('[init] Checking for Qt WebChannel');
    if (typeof qt !== 'undefined' && qt.webChannelTransport) {
        logToPython('[init] Qt WebChannel detected, initializing...');
        new QWebChannel(qt.webChannelTransport, function(channel) {
            backend = channel.objects.backend;
            logToPython('[init] Backend connected successfully');
        });
    } else {
        logToPython('[init] WARNING: Qt WebChannel not available');
}

});

