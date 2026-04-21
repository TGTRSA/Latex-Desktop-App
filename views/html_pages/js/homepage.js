const DIRECTORY_PATH = '../../texfiles';
const FILE_LIST_CONTAINER_ID = 'fileList';
const FILE_ITEM_CLASS = 'file-item';
const NO_FILES_MESSAGE = 'No files found';

let backend = null;

function displayFiles(files) {
    const container = document.getElementById(FILE_LIST_CONTAINER_ID);
    if (!container) return;
    
    container.innerHTML = '';
    
    if (!files || files.length === 0) {
        container.innerHTML = `<div class="${FILE_ITEM_CLASS}">${NO_FILES_MESSAGE}</div>`;
        return;
    }
    
    files.forEach(file => {
        const fileElement = document.createElement('div');
        fileElement.className = FILE_ITEM_CLASS;
        fileElement.textContent = file;
        
        fileElement.addEventListener('click', () => {
            console.log('Selected:', file);
            if (backend) backend.logToPython(file);
        });
        
        container.appendChild(fileElement);
    });
}

function loadFiles() {
    if (!backend) {
        console.log('Waiting for backend...');
        return;
    }
    
    const result = backend.listFilesInDirectory(DIRECTORY_PATH);
    const data = JSON.parse(result);
    
    if (data.error) {
        console.error(data.error);
        displayFiles([]);
        return;
    }
    
    displayFiles(data.files);
}

if (typeof qt !== 'undefined' && qt.webChannelTransport) {
    new QWebChannel(qt.webChannelTransport, function(channel) {
        backend = channel.objects.backend;
        loadFiles();
    });
}