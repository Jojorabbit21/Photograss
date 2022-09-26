// https://codepen.io/ig_design/pen/XWXZaGb 풀스크린 메뉴 pure css
// https://front.codes/ 좋은자료 많아보임

let quoteLoaded = 0;

function InitAnimate(element, dir, start, end, duration, easing, fill) {
  if (dir==0) {
    for(let i=0; i<element.length; i++) {
      setTimeout(() => {
        TextAnimate(element[i], start, end, duration, easing, fill);
      }, 50*i);
    }
  }
  else if (dir==1) {
    for(let j=element.length-1; j>=0; j--) {
      setTimeout(() => {
        TextAnimate(element[element.length-1-j], start, end, duration, easing, fill);
      }, 50*(element.length-1-j));
    }
  }
}

function TextAnimate(element, start, end, duration, easing, fill) {
  element.animate([
    { transform: `translate(0, ${start})` },
    { transform: `translate(0, ${end})` }],
  {
    duration: duration,
    easing: easing,
    fill: fill
  });
}

document.addEventListener('DOMContentLoaded', () => {
  /* Split Texts and recreate elements */
  try {
    let splitText = document.querySelectorAll(".split-text");
    for(let i=0; i<splitText.length; i++) {
      let parent = splitText[i].parentNode;
      let target = splitText[i].innerHTML;
      parent.replaceChildren();
      let div = document.createElement('div');
      let wrap = document.createElement('div');
      let tag = splitText[i].tagName;
      wrap.className = 'quoteWrapper';
      div.className = 'quoteBox quote';
      for (let i in target) {
        let t = target[i];
        let child = document.createElement(tag);
        child.innerText = target[i];
        if (t == " ") {
          child.classList = '__blank';
        }
        div.insertAdjacentElement('beforeEnd', child);
      }
      wrap.append(div);
      div = div.cloneNode(true);
      div.className = 'quoteBox quote quote-second';
      wrap.append(div);
      parent.insertAdjacentElement('beforeEnd', wrap);
    }
  } catch(err) { }
});


window.addEventListener('load', function() {
  if (window.location.pathname.indexOf('/projects') != -1 || window.location.pathname.indexOf('/commercial') != -1)
  {
    if(quoteLoaded == 0) {
      let q = document.querySelectorAll('.quoteWrapper');
      for (let i=0; i<q.length; i++) {
        setTimeout(() => {
          q[i].animate([
            { transform: 'translate(0, 100%)' },
            { transform: 'translate(0, 0)' }
          ],
          {
            duration: 700,
            easing: "ease",
            fill: "forwards"
          });
          quoteLoaded ++;
        }, 150*i);
      }
    }
  }
});

/* Split Text Animation */
try {
  let quoteContainers = document.querySelectorAll(".quoteContainer");
  [].forEach.call(quoteContainers, (quoteContainer) => {
    quoteContainer.addEventListener("mouseenter", function() {
      if(quoteLoaded === quoteContainers.length) {
        let quoteWrapper = quoteContainer.children;
        let quoteBox = quoteWrapper[0].children;
        let Letters = quoteBox[0].children;
        let LettersAlt = quoteBox[1].children;
        InitAnimate(Letters, 1, "0", "-100%", 500, "ease", "forwards");
        InitAnimate(LettersAlt, 1, "0", "-100%", 500, "ease", "forwards");
      }
    });
    quoteContainer.addEventListener("mouseleave", function() {
      if(quoteLoaded === quoteContainers.length) {
        let quoteWrapper = quoteContainer.children;
        let quoteBox = quoteWrapper[0].children;
        let Letters = quoteBox[0].children;
        let LettersAlt = quoteBox[1].children;
        InitAnimate(Letters, 1, "-100%", "0", 500, "ease", "forwards");
        InitAnimate(LettersAlt, 1, "-100%", "0", 500, "ease", "forwards");
      }
    });
  });
} catch(err) { }

if(window.location.pathname == '/snaps') {
  let snapExpanded = false;
  let snapContainer = document.querySelector(".masonry-container");
  /* Phrase toggle event listener */
  snapContainer.addEventListener("mouseenter", function() {
    phrase.className += " blur";
  });
  snapContainer.addEventListener("mouseleave", function() {
    if(!snapExpanded) { // if expanded image exists, not working
      phrase.className = "phrase-box";
    }
  });
  let snaps = document.querySelectorAll(".masonry-content");
  let phrase = document.querySelector(".phrase-box");
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
      // navbar.style.visibility = 'hidden';
  
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
          // navbar.style.visibility = 'visible';
          // remove snap expanded
          e.target.remove();
          // activate scroll
          document.body.style.overflowY = 'auto';
          snapExpanded = false;
        }
      });
    });
  });
}

if (window.location.pathname == '/home') {
  const swiper = new Swiper('.swiper', {
    effect: "fade",
    autoplay: {
      disableOnInteraction: false,
      delay: 3000,
    },
    autoHeight: true,
    speed: 2000, // ms
    spaceBetween: 0,
    direction: "horizontal",
    mousewheel: true,
    keyboard: {
      enabled: true,
      onlyInViewport: true,
    },
    loop: true,
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    }
  });
  // const maxLength = document.querySelector(".swiper-wrapper").getAttribute("max-length");
  // swiper.on('slideNextTransitionStart', function() {
  // });
  swiper.on('slideChangeTransitionStart', () => {
  });
}


/* CUSTOM CURSOR SCRIPT */

/* Smooth page transition */
// barba.js 사용하는 듯? https://ihatetomatoes.net/page-transitions-tutorial-barba-with-css/
// https://www.youtube.com/watch?v=aMucZErEdZg&ab_channel=DesignCourse 유튜브 강의 보고 따라해보기

let progressCreated = false;
window.onscroll = function() {
  onProgress();
}

function onProgress() {
  if(window.location.pathname.indexOf('/projects/') != -1 || window.location.pathname.indexOf('/commercial/') != -1)
  {
    let headerHeight = document.querySelector('.navbar-container').offsetHeight;
    let marqueeHeight = document.querySelector('.marquee-wrap').offsetHeight;
    if(window.scrollY > headerHeight + marqueeHeight) {
      if(!progressCreated) {
        let main = document.querySelector('main');
        let progressContainer = document.createElement('div');
        let progressBar = document.createElement('div');
        progressContainer.className = 'progress-container';
        progressBar.className = 'progress-bar';
        progressContainer.appendChild(progressBar);
        main.prepend(progressContainer);
        progressCreated = true;
      }
      let progressContainer = document.querySelector('.progress-container');
      let winScroll = document.body.scrollTop || document.documentElement.scrollTop;
      let height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
      let scrolled = (winScroll/height) * 100;
      progressContainer.style.width = `${scrolled}%`;
    }
    else if(window.scrollY < headerHeight + marqueeHeight) {
      if(progressCreated) {
        let progressContainer = document.querySelector('.progress-container');
        progressContainer.remove();
        progressCreated = false;
      }
    }
  } 
  else {
    return false;
  }
}
