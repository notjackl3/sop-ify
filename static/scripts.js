function dropHandler(ev, file_input, element) {
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
    const drop_zone = document.getElementById(element);
    drop_zone.textContent = "Dropped file.";
    drop_zone.classList.add('disabled');
}
  
function dragOverHandler(ev) {
    console.log("File(s) in drop zone");
    ev.preventDefault();
}

function addFile(ev, file_input, element) {
  const input = document.createElement('input');
  input.type = 'file';
  input.onchange = e => { 
    const file = e.target.files[0]; 
    
    const input = document.getElementById(file_input);
    const dataTransfer = new DataTransfer();
    dataTransfer.items.add(file);
    input.files = dataTransfer.files;

    const drop_zone = document.getElementById(element);
    drop_zone.textContent = "Dropped file.";
    drop_zone.classList.add('disabled');
  }

  input.click();
}

function resetFiles(ev) {
  const drop_zone1 = document.getElementById("drop_zone1");
  const drop_zone2 = document.getElementById("drop_zone2");
  drop_zone1.classList.remove("disabled");
  drop_zone2.classList.remove("disabled");
  drop_zone1.textContent = "Drag your original file here.";
  drop_zone2.textContent = "Drag your new file here.";
}
