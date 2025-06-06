function updateFileUploadButton(element, text_element, upload_element) {
  console.log(element)
  console.log(text_element)
  console.log(upload_element)
  const drop_zone = document.getElementById(element);
  drop_zone.classList.add('disabled');
  const text = document.getElementById(text_element);
  text.innerHTML = "File uploaded.";
  const upload = document.getElementById(upload_element);
  upload.style.display = "none";
}


function dropHandler(ev, file_input, element, text_element, upload_element) {
    ev.preventDefault();
    if (ev.dataTransfer.items) {
      [...ev.dataTransfer.items].forEach((item, i) => {
        if (item.kind === "file") {
          const file = item.getAsFile();

          const input = document.getElementById(file_input);
          const dataTransfer = new DataTransfer();
          dataTransfer.items.add(file);
          input.files = dataTransfer.files;
        }
      });
    }
    updateFileUploadButton(element, text_element, upload_element);
}
  
function dragOverHandler(ev) {
    console.log("File(s) in drop zone");
    ev.preventDefault();
}

function addFile(ev, file_input, element, text_element, upload_element) {
  const input = document.createElement('input');
  input.type = 'file';
  input.onchange = e => { 
    const file = e.target.files[0]; 
    
    const input = document.getElementById(file_input);
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    input.files = dataTransfer.files;

    updateFileUploadButton(element, text_element, upload_element);
  }

  input.click();
}

function resetFiles(ev) {
  const drop_zone1 = document.getElementById("drop_zone1");
  const drop_zone2 = document.getElementById("drop_zone2");
  drop_zone1.classList.remove("disabled");
  drop_zone2.classList.remove("disabled");
  const text1 = document.getElementById("text1");
  const text2 = document.getElementById("text1");
  text1.innerHTML = "Drag your original file here.";
  text2.innerHTML = "Drag your new file here.";
  const upload1 = document.getElementById("upload1");
  const upload2 = document.getElementById("upload2");
  upload1.style.display = "block";
  upload2.style.display = "block";
}
