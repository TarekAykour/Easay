document.addEventListener('DOMContentLoaded', () => {
  // Create the convert form and button
  const convertForm = document.createElement('form');
  convertForm.classList.add('convert-form');
  convertForm.action = '/convert';
  convertForm.method = 'POST';

  const convertBtn = document.createElement('input');
  convertBtn.classList.add('convert-btn');
  convertBtn.type = 'submit';
  convertBtn.value = 'Convert';

  convertForm.appendChild(convertBtn);

  // onchange event listener for the file upload input
  document.getElementById('fileUpload').addEventListener('change', ()=> {
    // append the list of uploaded files inside the box
    const container = document.querySelector('.uploaded-files-container') || createFileListContainer();
    const ul = document.getElementById('list') || createFileList(container);
    const files = document.getElementById('fileUpload').files;
    container.classList.remove('empty');
    // handleFileUpload();
    //     files.forEach(file => {
    //     if (!document.querySelector(`#file-${file.name}`)) {
    //     addFileToList(file.name, ul);
        
    // }
    // })
    
  });




  // Fetch the list of files and populate the UI
fetch('/files')
    .then(response => response.json())
    .then(files => {
        const container = document.querySelector('.uploaded-files-container') || createFileListContainer();
        const ul = document.getElementById('list') || createFileList(container);
        if (files.length === 0) {
            container.classList.add('empty');
        }

        files.forEach(file => {
            if (!document.querySelector(`#file-${file}`)) {
                addFileToList(file, ul);
                container.classList.remove('empty');
            }
        });

        // Check if files were uploaded during the last session
        if (localStorage.getItem('filesUploaded') === 'true') {
            alert('Files have been uploaded successfully!');
            localStorage.removeItem('filesUploaded');
        }
    })
    .catch(error => alert('Error fetching files:', error));

  // Add event listener for file upload changes
  document.getElementById('fileUpload').addEventListener('change', handleFileUpload);

  // Add event listener for form submission
  document.getElementById('uploadForm').addEventListener('submit', handleFileSubmit);

  // Add event listener for file conversion
  convertForm.addEventListener('submit',handleFileConversion);

  function createFileListContainer() {
      const container = document.createElement('div');
      container.classList.add('uploaded-files-container');
      document.querySelector('.upload-file').appendChild(container);

      const h2 = document.createElement('h2');
      h2.innerText = 'Uploaded files';
      h2.classList.add = 'list-title';	
      container.appendChild(h2);

      container.appendChild(convertForm);

      return container;
  }

  function createFileList(container) {
      const list = document.createElement('ul');
      list.setAttribute('id', 'list');
      list.classList.add('list');
      container.appendChild(list);
      return list;
  }

  function addFileToList(file, ul) {
      const li = document.createElement('li');
      li.id = `file-${file}`;

      const deleteForm = document.createElement('form');
      deleteForm.classList.add('delete-form');
      deleteForm.method = 'POST';
      deleteForm.action = `/delete/${file}`;

      const deleteBtn = document.createElement('input');
      deleteBtn.classList.add('delete-btn');
      deleteBtn.type = 'submit';
      deleteBtn.value = 'Delete';

      deleteForm.appendChild(deleteBtn);
      deleteForm.addEventListener('submit', handleFileDelete);

      li.appendChild(document.createTextNode(file));
      li.appendChild(deleteForm);
      ul.appendChild(li);
      alert(`${file} added to List. Press on 'Upload' if you are ready to merge documents!`)
  }

  function handleFileUpload() {
      const files = Array.from(document.getElementById('fileUpload').files);
      const ul = document.getElementById('list');
      const existingFiles = Array.from(ul.children).map(item => item.textContent);
      
      files.forEach(file => {
          if (!existingFiles.includes(file.name)) {
              addFileToList(file.name, ul);
              // location.reload();
          } else {
              None
          }
      });
  }

  function handleFileSubmit(event) {
      event.preventDefault();

      const fileInput = document.getElementById('fileUpload');
      const files = fileInput.files;

      if (files.length === 0) {
          alert('No files selected');
          return;
      }

      const formData = new FormData();
      for (let i = 0; i < files.length; i++) {
          formData.append('files', files[i]);
      }

      axios.post('/upload', formData, {
          headers: {
              'Content-Type': 'multipart/form-data'
          }
      })
      .then(response => {
          alert(`Files uploaded successfully!`, response.status);
      })
      .catch(error => {
          alert('Error uploading files:', error.message);
      });
  }

  function handleFileConversion(event) {
      event.preventDefault();

      const ul = document.getElementById('list');
      const files = Array.from(ul.children).map(item => item.textContent);
    //   alert(files, 'being converted')
      fetch('/convert', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ files })
      })
      .then(response => {
        response.json() 
        location.reload()})
      .then(data => {
          alert('converted the files. Click on "Download Final.doc to download!"');
          
      })
      .catch(error => alert('Error converting files:', error));
  }

  function handleFileDelete(event) {
      event.preventDefault();

      const form = event.target;
      const fileName = form.action.split('/').pop();

      fetch(`/delete/${fileName}`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          }
      })
      .then(response => {
          if (response.ok) {
              const ul = document.getElementById('list');
              const li = document.getElementById(`file-${fileName}`);
              ul.removeChild(li);
              location.reload()
          } else {
              alert('Error deleting file:', response.statusText);
          }
      })
      .catch(error => alert('Error deleting file:', error));
  }
});
