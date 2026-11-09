(function(){
  // Mobile menu
  var toggle=document.querySelector('.menu-toggle'),nav=document.querySelector('.nav');
  if(toggle&&nav){
    toggle.addEventListener('click',function(){var o=nav.classList.toggle('open');toggle.setAttribute('aria-expanded',o)});
    nav.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){nav.classList.remove('open');toggle.setAttribute('aria-expanded','false')})});
  }
  // Lightbox
  var box=document.querySelector('.lightbox');if(!box)return;
  var items=[].slice.call(document.querySelectorAll('.gallery button'));
  var img=box.querySelector('img'),cap=box.querySelector('figcaption'),i=0;
  function show(n){i=(n+items.length)%items.length;var b=items[i];img.src=b.dataset.full;img.alt=b.dataset.caption;cap.textContent=b.dataset.caption+'  ('+(i+1)+'/'+items.length+')'}
  items.forEach(function(b,n){b.addEventListener('click',function(){show(n);if(box.showModal)box.showModal();else box.setAttribute('open','')})});
  box.querySelector('.lb-close').addEventListener('click',function(){box.close()});
  box.querySelector('.lb-prev').addEventListener('click',function(){show(i-1)});
  box.querySelector('.lb-next').addEventListener('click',function(){show(i+1)});
  box.addEventListener('keydown',function(e){if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1)});
  box.addEventListener('click',function(e){if(e.target===box||e.target.tagName==='FIGURE')box.close()});
  var x0=null;box.addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});
  box.addEventListener('touchend',function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>50)show(dx<0?i+1:i-1);x0=null});
})();
