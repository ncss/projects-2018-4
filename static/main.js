var standalone = false;

if (window.navigator.standalone){
  console.log('Running as standalone')
  document.body.webkitRequestFullScreen()
}else{
  console.log('Running as webpage')
}

// alert(window.navigator.standalone)