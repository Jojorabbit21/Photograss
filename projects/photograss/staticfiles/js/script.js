let snapExpanded = false;
let phrase = document.querySelector(".phrase-box");
let snapContainer = document.querySelector(".masonry-container");
let snaps = document.querySelectorAll(".masonry-content");

/* Phrase toggle event listener */
snapContainer.addEventListener("mouseenter", function() {
  phrase.className += " blur";
});
snapContainer.addEventListener("mouseleave", function() {
  if(!snapExpanded) { // if expanded image exists, not working
    phrase.className = "phrase-box";
  }
});

/* Menu Hovering event listener */
// let dirs = document.querySelectorAll('.nav-links');
// [].forEach.call(dirs, function(dir) {
//   dir.addEventListener("mouseover", function(e) {
    
//   });
// });

/* Masonry Detail page creation */ 
[].forEach.call(snaps, function(snap) {
  snap.addEventListener("click", function(e) {
    const src = e.target.getAttribute('src');
    const navbar = document.querySelector('.navbar-container');
    const expand = document.createElement('div');
    const expandImgs = document.createElement('img');
    let phraseBox = document.querySelector('.phrase-box');
    expand.className = 'expand-bg';
    expandImgs.className = 'expand-img';
    expandImgs.src = src;

    // create expanded imgs
    expand.appendChild(expandImgs);
    document.body.prepend(expand);

    // Hide navigation
    navbar.style.visibility = 'hidden';

    phraseBox.className += " blur";
    expand.className += " visible";
    snapExpanded = true;

    // Deactivate scroll when expanded
    document.body.style.overflowY = 'hidden';

    // Remove created expanded imgs
    expand.addEventListener("click", function(e) {
      if(snapExpanded) {
        phraseBox.className = "phrase-box";
        // show navigation
        navbar.style.visibility = 'visible';
        // remove snap expanded
        e.target.remove();
        // activate scroll
        document.body.style.overflowY = 'auto';
        snapExpanded = false;
      }
    });
  });
});


//////////////// AJAX to Django API using Fetch API
// function SnapshotDetail(e) {
//   const href = e.getAttribute('href');
//   fetch("{% url 'main:snap' %}", {
//     method: 'POST',
//     credentials: 'same-origin',
//     headers: {
//       'Accept': 'application/json',
//       'X-Requested-With': 'XMLHttpRequest',
//     },
//     body: JSON.stringify({}) // Javascript Object of data to POST
//   })
//   .then(response => {
//     return response.json() // Convert response to JSON.
//   })
//   .then(data => {
//     // Do something with returned data.
//   })
// }

/* Smooth page transition */
// barba.js 사용하는 듯?
document.addEventListener('DOMContentLoaded', ()=> {
  // Do something here
});



