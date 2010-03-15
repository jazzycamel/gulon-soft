// Master JS File for gulon.co.uk
$(function(){
  if (navigator.appName=='Microsoft Internet Explorer' && navigator.appVersion.indexOf('MSIE 6')!=-1){
    // If IE6, don't apply rounded corners.
  } else {
    DD_roundies.addRule('.boxLink', '5px', true); 
    DD_roundies.addRule('code', '5px', true); 
  }
});
