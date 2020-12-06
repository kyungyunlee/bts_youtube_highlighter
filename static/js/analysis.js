// /* When the user clicks on the button,
// toggle between hiding and showing the dropdown content */
// function myFunction() {
//     document.getElementById("myDropdown").classList.toggle("show");
//   }
  
//   // Close the dropdown menu if the user clicks outside of it
//   window.onclick = function(event) {
//     if (!event.target.matches('.dropbtn')) {
//       var dropdowns = document.getElementsByClassName("dropdown-content");
//       var i;
//       for (i = 0; i < dropdowns.length; i++) {
//         var openDropdown = dropdowns[i];
//         if (openDropdown.classList.contains('show')) {
//           openDropdown.classList.remove('show');
//         }
//       }
//     }
//   }


  function toggleClass(elem,className){
    if (elem.className.indexOf(className) !== -1){
      elem.className = elem.className.replace(className,'');
    }
    else{
      elem.className = elem.className.replace(/\s+/g,' ') + 	' ' + className;
    }
    
    return elem;
  }
  
  function toggleDisplay(elem){
    const curDisplayStyle = elem.style.display;			
          
    if (curDisplayStyle === 'none' || curDisplayStyle === ''){
      elem.style.display = 'block';
    }
    else{
      elem.style.display = 'none';
    }
  }
  
  
  function toggleMenuDisplay(e){
    const dropdown = e.currentTarget.parentNode;
    const menu = dropdown.querySelector('.menu');
    const icon = dropdown.querySelector('.fa-angle-right');
  
    toggleClass(menu,'hide');
    toggleClass(icon,'rotate-90');
  }



  function handleOptionSelected(e){
    toggleClass(e.target.parentNode, 'hide');			
  
    const id = e.target.id;
    // console.log(e.target.grretElementsByTagName("a"));
    // const newValue = e.target.getElementsByTagName("a")[0].textContent;
    // console.log(newValue);
    console.log(e.target);
    const newValue = e.target.textContent + ' ';
    const titleElem = document.querySelector('.dropdown .title');
    const icon = document.querySelector('.dropdown .title .fa');
  
  
    titleElem.textContent = newValue;
    titleElem.appendChild(icon);
    
    //trigger custom event
    document.querySelector('.dropdown .title').dispatchEvent(new Event('change'));
    //setTimeout is used so transition is properly shown
    setTimeout(() => toggleClass(icon,'rotate-90',0));

   // Display none 
   console.log(e.target.id);
   if (e.target.id == 'option1') {
     document.getElementById("keywords").style.display = "none";
     document.getElementById("popular_frames").style.display = "initial";

   } else {
     document.getElementById("keywords").style.display = "initial";
     document.getElementById("popular_frames").style.display = "none"; 
   }



  }


  function handleTitleChange(e){
    const result = document.getElementById('result');
    result.innerHTML = e.target.textContent;

    // // Display none 
    // console.log(e.target);
    // if (e.target.id == 'option1') {
    //   document.getElementById("keywords").style.display = "none";
    //   document.getElementById("popular_frames").style.display = "initial";

    // } else {
    //   document.getElementById("keywords").style.display = "initial";
    //   document.getElementById("popular_frames").style.display = "none"; 
    // }

  }


  //get elements
const dropdownTitle = document.querySelector('.dropdown .title');
const dropdownOptions = document.querySelectorAll('.dropdown .option');

//bind listeners to these elements
dropdownTitle.addEventListener('click', toggleMenuDisplay);
dropdownOptions.forEach(option => option.addEventListener('click',handleOptionSelected));
document.querySelector('.dropdown .title').addEventListener('change',handleTitleChange);