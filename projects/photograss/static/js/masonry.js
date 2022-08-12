function SetGridItemHeight(){
  let grid = document.getElementsByClassName('grid')[0];
  let rowHeight = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-auto-rows'));
  let rowGap = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-row-gap'));

  let item = grid.getElementsByClassName('item');
  for(let i =0; i < item.length;++i){
      item[i].style.gridRowEnd = `span ${Math.floor((item[i].children[0].offsetHeight)/25)}`
      // Math.ceil -> Math.floor
      // item[i].offsetHeight -> item[i].children[0].offsetHeight
  }
}

window.addEventListener("load", SetGridItemHeight);
window.addEventListener("resize", SetGridItemHeight);