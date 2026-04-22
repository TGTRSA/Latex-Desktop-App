const FILE_LIST_CONTAINER_ID = 'fileList';
const FILE_ITEM_CLASS = 'file-item';
const NO_FILES_MESSAGE = 'No files found';

let backend = null;

function readFile(fileName) {
    if(backend){
        backend.readFile(fileName);
        backend.sendtex.connect(function(tex){
            // let slice = tex.slice(0,20);
            backend.logToPython(tex);
            localStorage.setItem('texInput', tex);
            localStorage.setItem('fileName', fileName);
            window.location ="compiler.html";
            window.location.href = "compiler.html";
        });
    }else {
        str = "[JS:readFile] Cannot connect to python";
        backend.logToPython(str);
        
        // localStorage.setItem('tex', );
        // window.location = 'compiler.html'
    }
}

function logToPython(message) {
    if (backend) {
        backend.logToPython(message);
    } else {
        console.log(message);
    }
}

function displayFiles(files) {
    logToPython('[displayFiles] Starting with ' + (files ? files.length : 0) + ' files');
    
    const container = document.getElementById(FILE_LIST_CONTAINER_ID);
    if (!container) {
        logToPython('[displayFiles] ERROR: Container element not found');
        return;
    }
    
    container.innerHTML = '';
    
    if (!files || files.length === 0) {
        logToPython('[displayFiles] No files to display');
        container.innerHTML = `<div class="${FILE_ITEM_CLASS}">${NO_FILES_MESSAGE}</div>`;
        return;
    }
    
    logToPython('[displayFiles] Displaying ' + files.length + ' files');
    
    files.forEach(file => {
        const fileElement = document.createElement('div');
        fileElement.className = FILE_ITEM_CLASS;
        fileElement.textContent = file;
        
        fileElement.addEventListener('click', () => {
            logToPython('[click] User selected file: ' + file);
            readFile(file);
        });
        
        container.appendChild(fileElement);
    });
    
    logToPython('[displayFiles] Completed rendering');
}

async function loadFiles() {
    logToPython('[loadFiles] Attempting to load files');
    
    if (!backend) {
        logToPython('[loadFiles] ERROR: Backend not available');
        return;
    }
    
    logToPython('[loadFiles] Calling getFileList()');
    
    try {
        // Use await to get the actual result instead of a Promise
        const resultJson = await backend.getFileList();
        logToPython('[loadFiles] Raw result: ' + resultJson);
        
        const result = JSON.parse(resultJson);
        
        if (result.error) {
            logToPython('[loadFiles] ERROR: ' + result.error);
            displayFiles([]);
            return;
        }
        
        logToPython('[loadFiles] Success - found ' + result.files.length + ' files');
        displayFiles(result.files);
    } catch (err) {
        logToPython('[loadFiles] EXCEPTION: ' + err.message);
        displayFiles([]);
    }
}

// Initialize Qt bridge
logToPython('[init] Checking for Qt WebChannel');
if (typeof qt !== 'undefined' && qt.webChannelTransport) {
    logToPython('[init] Qt WebChannel detected, initializing...');
    new QWebChannel(qt.webChannelTransport, function(channel) {
        backend = channel.objects.backend;
        logToPython('[init] Backend connected successfully');
        loadFiles();
    });
} else {
    logToPython('[init] WARNING: Qt WebChannel not available');
}